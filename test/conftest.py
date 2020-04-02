import pytest

from tospotify.types.artists import Artist
from tospotify.types.queries import QueryArtistTitle
from tospotify.types.titles import Title


@pytest.fixture(scope='session')
def artist_fixture():
    return Artist('artist')


@pytest.fixture(scope='session')
def title_fixture():
    return Title('title')


@pytest.fixture(scope='session')
def query_fixture(artist_fixture, title_fixture):
    return QueryArtistTitle(artist_fixture, title_fixture)
