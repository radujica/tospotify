import logging
from queue import Queue
from typing import List, Optional

import m3u8
from spotipy import Spotify

from .processing import process_song_name
from .queries import ADDITIONAL_QUERIES, DEFAULT_QUERY


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
    if len(results) > 0:
        uri = results[0]['uri']
        logging.info('Found track with query={} as uri={}'.format(query, uri))
        return uri
    else:
        logging.info('{}Could not find any track with query={}'.format('-' * iteration, query))
        return None


def _find_track(sp: Spotify, song: m3u8.Segment, market: str = None) -> Optional[str]:
    artist, title = process_song_name(song.title())

    queue = Queue()
    queue.put(DEFAULT_QUERY(artist, title).compile()[0])
    query_class_pool = list(ADDITIONAL_QUERIES)
    uri = None
    iteration = 0
    while uri is None and not queue.empty():
        query = queue.get()
        uri = _run_query(sp, query, market=market, iteration=iteration)

        if uri is None and queue.empty():
            while queue.empty():
                query = query_class_pool.pop()(artist, title)
                if query.makes_sense():
                    query_strings = query.compile()
                    for q in query_strings:
                        queue.put(q)

        iteration += 1

    return uri


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
