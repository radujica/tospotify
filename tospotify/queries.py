import re
from typing import Tuple

from m3u8 import Segment


# TODO: handle utf-8 properly
def _clean_name(name: str) -> str:
    # keep only ascii and extra relevant characters: -\s,
    name = re.sub(r'[^a-zA-Z0-9\-\s,]', '', name)
    name = re.sub(r'\s+', ' ', name)
    name = name.strip()

    return name


def _process_song_name(song_name: str) -> Tuple[str, str]:
    song_name = str(song_name)

    # TODO: handle if artist contains '-' or there's no '-'
    song_split = song_name.split('-', 1)

    artist = _clean_name(song_split[0])
    title = _clean_name(song_split[1])

    return artist, title


def _prepare_search_query_component(s: str, query_type: str) -> str:
    # need to escape the quotes else requests will url-encode them
    return query_type + ':' + '\"' + s + '\"'


def _prepare_search_query(artist: str, title: str) -> str:
    artist = _prepare_search_query_component(artist, 'artist')
    title = _prepare_search_query_component(title, 'track')

    query = ' '.join([artist, 'AND', title])

    return query


def search_artist_and_title(song: Segment) -> str:
    artist, title = _process_song_name(song.title)
    query = _prepare_search_query(artist, title)

    return query


def search_title_only(song: Segment) -> str:
    artist, title = _process_song_name(song.title)
    query = _prepare_search_query_component(title, 'track')

    return query


QUERY_COMPILERS = [search_artist_and_title, search_title_only]
