import pytest

from tospotify.queries import (
    QueryArtistTitle,
    QueryArtistBeginsWithThe,
    QuerySplitMultipleArtists,
    QueryMultipleAndArtists,
    QueryMultipleAndSymbolArtists,
    QuerySplitAndArtists,
    QuerySplitAndSymbolArtists,
    QueryTitle,
    QueryWildcard
)


@pytest.mark.parametrize('artist,title,query_class,expected', [
    ('Sting', 'Shape of my heart', QueryArtistTitle,
     ['artist:"Sting" AND track:"Shape of my heart"']),
    ('the Police', 'Every Breath You Take', QueryArtistBeginsWithThe,
     ['artist:"Police" AND track:"Every Breath You Take"']),
    ('Sting; The Police', 'Every Breath You Take', QuerySplitMultipleArtists,
     ['artist:"Sting" AND track:"Every Breath You Take"', 'artist:"The Police" AND track:"Every Breath You Take"']),
    ('Sting and The Police', 'Every Breath You Take', QueryMultipleAndArtists,
     ['artist:"Sting & The Police" AND track:"Every Breath You Take"']),
    ('Sting & The Police', 'Every Breath You Take', QueryMultipleAndSymbolArtists,
     ['artist:"Sting and The Police" AND track:"Every Breath You Take"']),
    ('Sting and The Police', 'Every Breath You Take', QuerySplitAndArtists,
     ['artist:"Sting" AND track:"Every Breath You Take"', 'artist:"The Police" AND track:"Every Breath You Take"']),
    ('Sting & The Police', 'Every Breath You Take', QuerySplitAndSymbolArtists,
     ['artist:"Sting" AND track:"Every Breath You Take"', 'artist:"The Police" AND track:"Every Breath You Take"']),
    ('Sting', 'Shape of my heart', QueryTitle,
     ['track:"Shape of my heart"']),
    ('Sting', 'Shape of my heart', QueryWildcard,
     ['"Sting Shape of my heart"'])
])
def test_query_compile(artist, title, query_class, expected):
    actual = query_class(artist, title).compile()

    assert actual == expected
