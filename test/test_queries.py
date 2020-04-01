import pytest

from tospotify.queries import (
    QueryArtistTitle,
    QueryArtistBeginsWithThe,
    QueryArtistMightBeginWithTheTitle,
    QuerySplitMultipleArtists,
    QueryMultipleAndArtists,
    QueryMultipleAndSymbolArtists,
    QuerySplitAndArtists,
    QuerySplitAndSymbolArtists,
    QueryWildcard
)


@pytest.mark.parametrize('artist,title,query_class,expected', [
    ('Sting', 'Shape of my heart', QueryArtistTitle,
     ['artist:"Sting" AND track:"Shape of my heart"']),

    ('the Police', 'Every Breath You Take', QueryArtistBeginsWithThe,
     ['artist:"Police" AND track:"Every Breath You Take"']),

    ('the police', 'Every Breath You Take', QueryArtistMightBeginWithTheTitle,
     ['artist:"the police" AND track:"Every Breath You Take"', 'artist:"police" AND track:"Every Breath You Take"']),

    ('Sting; the Police;test', 'Every Breath You Take', QuerySplitMultipleArtists,
     ['artist:"Sting" AND track:"Every Breath You Take"', 'artist:"the Police" AND track:"Every Breath You Take"',
      'artist:"Police" AND track:"Every Breath You Take"', 'artist:"test" AND track:"Every Breath You Take"']),

    ('Sting and the Police and test', 'Every Breath You Take', QueryMultipleAndArtists,
     ['artist:"Sting & the Police and test" AND track:"Every Breath You Take"']),

    ('Sting & the Police', 'Every Breath You Take', QueryMultipleAndSymbolArtists,
     ['artist:"Sting and the Police" AND track:"Every Breath You Take"']),

    ('Sting and the Police', 'Every Breath You Take', QuerySplitAndArtists,
     ['artist:"Sting" AND track:"Every Breath You Take"', 'artist:"the Police" AND track:"Every Breath You Take"',
      'artist:"Police" AND track:"Every Breath You Take"']),

    ('Sting & the Police & test', 'Every Breath You Take', QuerySplitAndSymbolArtists,
     ['artist:"Sting" AND track:"Every Breath You Take"', 'artist:"the Police" AND track:"Every Breath You Take"',
      'artist:"Police" AND track:"Every Breath You Take"', 'artist:"test" AND track:"Every Breath You Take"']),

    ('Sting', 'Shape of my heart', QueryWildcard,
     ['"Sting Shape of my heart"'])
])
def test_query_compile(artist, title, query_class, expected):
    actual = query_class(artist, title).compile()

    assert actual == expected
