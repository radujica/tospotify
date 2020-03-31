import pytest

from tospotify.queries import QueryArtistTitle, QueryMultipleArtists, QueryTitle


@pytest.mark.parametrize("artist,title,query_class,expected", [
    ('Sting', 'Shape of my heart', QueryArtistTitle,
     ['artist:"Sting" AND track:"Shape of my heart"']),
    ('Sting;The Police', 'Shape of my heart', QueryMultipleArtists,
     ['artist:"Sting" AND track:"Shape of my heart"', 'artist:"The Police" AND track:"Shape of my heart"']),
    ('Sting', 'Shape of my heart', QueryTitle,
     ['track:"Shape of my heart"'])
])
def test_query_compile(artist, title, query_class, expected):
    actual = query_class(artist, title).compile()

    assert actual == expected
