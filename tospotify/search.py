import re
from typing import Tuple

import m3u8
from spotipy import Spotify


def get_user_id(sp: Spotify) -> str:
    return sp.current_user()['id']


# TODO: handle utf-8 properly
def clean_name(name: str) -> str:
    name = re.sub(r'[^a-zA-Z0-9\-\s]', '', name)
    name = re.sub(r'\s+', ' ', name)
    name = name.strip()

    return name


def process_song_name(song_name: str) -> Tuple[str, str]:
    song_name = str(song_name)

    # TODO: handle if artist contains '-'
    song_split = song_name.split('-', 1)

    artist = clean_name(song_split[0])
    title = clean_name(song_split[1])

    return artist, title


def prepare_search_query_component(s: str, query_type: str) -> str:
    # need to escape the quotes else requests will url-encode them
    return query_type + ':' + '\"' + s + '\"'


def prepare_search_query(artist: str, title: str) -> str:
    artist = prepare_search_query_component(artist, 'artist')
    title = prepare_search_query_component(title, 'track')

    query = ' '.join([artist, 'AND', title])

    return query


def prepare_search_query_track_only(title: str) -> str:
    query = prepare_search_query_component(title, 'track')

    return query


def create_spotify_playlist(
    sp: Spotify,
    playlist_name: str,
    public: bool = False,
    description: str = ''
) -> str:
    user_id = get_user_id(sp)
    res = sp.user_playlist_create(user_id, playlist_name, public=public, description=description)
    # TODO: validate res
    playlist_id = res['id']

    return playlist_id


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
        artist, title = process_song_name(song.title)
        query = prepare_search_query(artist, title)
        res = sp.search(query, limit=1, type='track', market=market)
        results = res['tracks']['items']
        if len(results) > 0:
            uri = results[0]['uri']
            tracks.append(uri)
            print('Found track with query={} as uri={}'.format(query, uri))
        else:
            query = prepare_search_query_track_only(title)
            res = sp.search(query, limit=1, type='track', market=market)
            results = res['tracks']['items']
            if len(results) > 0:
                uri = results[0]['uri']
                tracks.append(uri)
                print('Found track with query={} as uri={}'.format(query, uri))
            else:
                print('Not found any track with query={}'.format(query))

    user_id = get_user_id(sp)
    sp.user_playlist_add_tracks(user_id, playlist_id, tracks)
