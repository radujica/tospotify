import logging
from typing import List, Optional

import m3u8
from spotipy import Spotify

from .generator import QueryGenerator
from .processing import process_song_name, MIN_LENGTH_NAME


def get_user_id(spot: Spotify) -> str:
    """ Return user id of this Spotify connection

    :param spot: spotipy Spotify object to use its REST API
    :type spot: Spotify
    :return: str
    :rtype: str
    """
    return spot.current_user()['id']


def create_spotify_playlist(spot: Spotify, playlist_name: str, public: bool = False) -> str:
    """ Create a playlist on Spotify

    :param spot: spotipy Spotify object to use its REST API
    :type spot: Spotify
    :param playlist_name: name of future the playlist
    :type playlist_name: str
    :param public: public or private playlist; note this assumes sp was created using the appropriate scope
    :type public: bool
    :return: the id of the just-created playlist
    :rtype: str
    """
    user_id = get_user_id(spot)
    res = spot.user_playlist_create(user_id, playlist_name, public=public)
    playlist_id = res['id']

    return playlist_id


def _run_query(spot: Spotify, query: str, market: str = None, iteration: int = 0) -> Optional[str]:
    response = spot.search(query, limit=1, type='track', market=market)
    results = response['tracks']['items']
    prepend_pretty_print = '-' * iteration
    uri = None
    if len(results) > 0:
        uri = results[0]['uri']
        logging.info('{}Found track with query={} as uri={}'.format(prepend_pretty_print, query, uri))
    else:
        logging.info('{}Could not find track with query={}'.format(prepend_pretty_print, query))

    return uri


# the code is optimized to limit the number of queries to Spotify as much as possible
def _find_track(spot: Spotify, song: m3u8.Segment, market: str = None) -> Optional[str]:
    artist, title = process_song_name(song.title())

    if len(artist) < MIN_LENGTH_NAME:
        logging.warning('Encountered artist after processing with short name={}'.format(artist))
    if len(title) < MIN_LENGTH_NAME:
        logging.warning('Encountered title after processing with short name={}'.format(title))

    query_generator = QueryGenerator(artist, title)
    iteration = 0
    for query in query_generator.generate():
        uri = _run_query(spot, query, market=market, iteration=iteration)

        if uri is not None:
            return uri

        iteration += 1

    return None


def add_tracks(spot: Spotify, playlist_id: str, tracks: List[str]) -> None:
    """ Add tracks to a Spotify playlist

    :param spot: spotipy Spotify object to use its REST API
    :type spot: Spotify
    :param playlist_id: id of the playlist
    :type playlist_id: str
    :param tracks: list of Spotify track uri's to add
    :type tracks: [str]
    :return:
    """
    user_id = get_user_id(spot)
    max_tracks_per_request = 100
    for i in range(len(tracks) // max_tracks_per_request + 1):
        tracks_subset = tracks[i * max_tracks_per_request:(i + 1) * max_tracks_per_request]
        spot.user_playlist_add_tracks(user_id, playlist_id, tracks_subset)


def update_spotify_playlist(
        spot: Spotify,
        playlist_path: str,
        playlist_id: str,
        market: str = None
) -> None:
    """ Read songs from an m3u file and update a Spotify playlist with these songs

    :param spot: spotipy Spotify object to use its REST API
    :type spot: Spotify
    :param playlist_path: absolute path of the playlist
    :type playlist_path: str
    :param playlist_id: Spotify id for the playlist to update
    :type playlist_id: str
    :param market: market to look for songs in; see Spotipy docs
    :type market: str
    :return:
    """
    playlist = m3u8.load(playlist_path)

    tracks = []
    for song in playlist.segments:
        track_uri = _find_track(spot, song.title, market)
        if track_uri:
            tracks.append(track_uri)
        else:
            logging.warning('Could not find any track for song with artist - title={}'.format(song.title))

    if len(tracks) == 0:
        logging.error('Could not find any tracks!')
    else:
        add_tracks(spot, playlist_id, tracks)
