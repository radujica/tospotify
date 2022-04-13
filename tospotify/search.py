import logging
from typing import List, Optional

import m3u8
from spotipy import Spotify

from .generator import QueryGenerator
from .parser import parse_songs, convert_utf8
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
        logging.info(f'{prepend_pretty_print}Found track with query={query} as uri={uri}')
    else:
        logging.info(f'{prepend_pretty_print}Could not find track with query={query}')

    return uri


# the code is optimized to limit the number of queries to Spotify as much as possible
def _find_track(spot: Spotify, song: m3u8.Segment, market: str = None) -> Optional[str]:
    artist, title = process_song_name(song.title())

    if len(artist) < MIN_LENGTH_NAME:
        logging.warning(f'Encountered artist after processing with short name={artist}')
    if len(title) < MIN_LENGTH_NAME:
        logging.warning(f'Encountered title after processing with short name={title}')

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
        to_convert: bool,
        market: str = None
) -> None:
    """ Read songs from an m3u file and update a Spotify playlist with these songs

    :param spot: spotipy Spotify object to use its REST API
    :type spot: Spotify
    :param playlist_path: absolute path of the playlist
    :type playlist_path: str
    :param playlist_id: Spotify id for the playlist to update
    :type playlist_id: str
    :param to_convert: whether to convert file to utf-8
    :type to_convert: bool
    :param market: market to look for songs in; see Spotipy docs
    :type market: str
    :return:
    """
    if to_convert:
        playlist_path = convert_utf8(playlist_path)

    songs = parse_songs(playlist_path)

    if len(songs) > 0:
        tracks = []
        for song in songs:
            track_uri = _find_track(spot, song.title, market)
            if track_uri:
                tracks.append(track_uri)
            else:
                logging.warning(f'Could not find any track for song with artist - title={song.title}')
        if len(tracks) == 0:
            logging.error('Could not find any tracks on Spotify!')
        else:
            add_tracks(spot, playlist_id, tracks)
    else:
        logging.info('Did not try searching on Spotify since no songs were found in the file.')
