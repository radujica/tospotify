import pytest

from tospotify.types.artists import Artist, MultipleTogetherAndArtist, MultipleSplitSemicolonArtist
from tospotify.types.queries import Query, QueryArtistTitle
from tospotify.types.titles import Title, CleanedTitle


# noinspection PyProtectedMember
def test_query__surround_with_quotes():
    assert Query._surround_with_quotes('abc') == '\"abc\"'


# noinspection PyProtectedMember
def test_query__prepare_query_component():
    assert Query._prepare_query_component('abc', 'artist') == 'artist:\"abc\"'


# noinspection PyProtectedMember
def test_query__prepare_artist_component(query_fixture):
    assert list(query_fixture._prepare_artist_component()) == ['artist:\"artist\"']


# noinspection PyProtectedMember
def test_query__prepare_title_component(query_fixture):
    assert query_fixture._prepare_title_component() == 'track:\"title\"'


@pytest.mark.parametrize('artist,title,expected_sense,expected_compile', [
    (MultipleTogetherAndArtist('Sting and The Police'), CleanedTitle('Every Breath feat. Sting'), True,
     ['artist:\"Sting & The Police\" AND track:\"Every Breath\"']),
    (MultipleTogetherAndArtist('Sting and The Police'), CleanedTitle('Every Breath'), False,
     ['artist:\"Sting & The Police\" AND track:\"Every Breath\"']),
    (MultipleTogetherAndArtist('Sting & The Police'), CleanedTitle('Every Breath feat. Sting'), False,
     ['artist:\"Sting & The Police\" AND track:\"Every Breath\"']),
    (MultipleTogetherAndArtist('Sting & The Police'), CleanedTitle('Every Breath'), False,
     ['artist:\"Sting & The Police\" AND track:\"Every Breath\"']),

    (MultipleSplitSemicolonArtist('Sting; The Police'), CleanedTitle('Every Breath feat. Sting'), True,
     ['artist:\"Sting\" AND track:\"Every Breath\"', 'artist:\"The Police\" AND track:\"Every Breath\"']),
])
def test_query_artist_title(artist, title, expected_sense, expected_compile):
    actual = QueryArtistTitle(artist, title)

    assert actual.makes_sense() == expected_sense
    assert list(actual.compile()) == expected_compile
