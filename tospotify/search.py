import logging
from typing import List, Optional

import m3u8
from spotipy import Spotify

from .generator import QueryGenerator
from .processing import process_song_name


def get_user_id(sp: Spotify) -> str:
    return sp.current_user()['id']


def create_spotify_playlist(sp: Spotify, playlist_name: str, public: bool = False) -> str:
    user_id = get_user_id(sp)
    res = sp.user_playlist_create(user_id, playlist_name, public=public)
    playlist_id = res['id']

    return playlist_id


def _run_query(sp: Spotify, query: str, market: str = None, iteration: int = 0) -> Optional[str]:
    response = sp.search(query, limit=1, type='track', market=market)
    results = response['tracks']['items']
    prepend_pretty_print = '-' * iteration
    if len(results) > 0:
        uri = results[0]['uri']
        logging.info('{}Found track with query={} as uri={}'.format(prepend_pretty_print, query, uri))
        return uri
    else:
        logging.info('{}Could not find track with query={}'.format(prepend_pretty_print, query))
        return None


# the code is optimized to limit the number of queries to Spotify as much as possible
def _find_track(sp: Spotify, song: m3u8.Segment, market: str = None) -> Optional[str]:
    artist, title = process_song_name(song.title())

    query_generator = QueryGenerator(artist, title)
    iteration = 0
    for query in query_generator.generate():
        uri = _run_query(sp, query, market=market, iteration=iteration)

        if uri is not None:
            return uri

        iteration += 1

    return None


def add_tracks(sp: Spotify, playlist_id: str, tracks: List[str]) -> None:
    user_id = get_user_id(sp)
    max_tracks_per_request = 100
    for i in range(len(tracks) // max_tracks_per_request + 1):
        tracks_subset = tracks[i * max_tracks_per_request:(i + 1) * max_tracks_per_request]
        sp.user_playlist_add_tracks(user_id, playlist_id, tracks_subset)


def update_spotify_playlist(
    sp: Spotify,
    playlist_path: str,
    playlist_id: str,
    market: str = None
) -> None:
    # TODO: can this fail besides not finding file?
    playlist = m3u8.load(playlist_path)

    tracks = []
    for song in playlist.segments:
        track_uri = _find_track(sp, song.title,  market)
        if track_uri:
            tracks.append(track_uri)
        else:
            logging.warning('Could not find any track for song with artist - title={}'.format(song.title))

    if len(tracks) == 0:
        logging.error('Could not find any tracks!')
    else:
        add_tracks(sp, playlist_id, tracks)
