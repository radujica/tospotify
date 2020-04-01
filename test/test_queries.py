import pytest

from tospotify.queries import (
    QueryArtistTitle,
    QueryArtistCleanedTitle,
    QueryArtistTitleMightClean,
    QueryArtistBeginsWithThe,
    QueryArtistMightBeginWithTheTitle,
    QuerySplitMultipleArtists,
    QueryMultipleAndArtists,
    QueryMultipleAndSymbolArtists,
    QuerySplitAndArtists,
    QuerySplitAndSymbolArtists,
    QueryWildcard,
    QueryWildcardCleanTitle
)


@pytest.mark.parametrize('artist,title,query_class,expected', [
    ('Sting', 'Shape of my heart', QueryArtistTitle,
     ['artist:"Sting" AND track:"Shape of my heart"']),

    ('The Police', 'Every Breath You Take feat. Sting', QueryArtistCleanedTitle,
     ['artist:"The Police" AND track:"Every Breath You Take"']),

    ('police', 'Every Breath You Take feat. Sting', QueryArtistTitleMightClean,
     ['artist:"police" AND track:"Every Breath You Take feat. Sting"',
      'artist:"police" AND track:"Every Breath You Take"']),

    ('police', 'Every Breath You Take', QueryArtistTitleMightClean,
     ['artist:"police" AND track:"Every Breath You Take"']),

    ('the Police', 'Every Breath You Take', QueryArtistBeginsWithThe,
     ['artist:"Police" AND track:"Every Breath You Take"']),

    ('the Police', 'Every Breath You Take feat. Sting', QueryArtistBeginsWithThe,
     ['artist:"Police" AND track:"Every Breath You Take feat. Sting"',
      'artist:"Police" AND track:"Every Breath You Take"']),

    ('the police', 'Every Breath You Take', QueryArtistMightBeginWithTheTitle,
     ['artist:"the police" AND track:"Every Breath You Take"', 'artist:"police" AND track:"Every Breath You Take"']),

    ('the police', 'Every Breath You Take featuring Sting', QueryArtistMightBeginWithTheTitle,
     ['artist:"the police" AND track:"Every Breath You Take featuring Sting"',
      'artist:"the police" AND track:"Every Breath You Take"',
      'artist:"police" AND track:"Every Breath You Take featuring Sting"',
      'artist:"police" AND track:"Every Breath You Take"']),

    ('police', 'Every Breath You Take', QueryArtistMightBeginWithTheTitle,
     ['artist:"police" AND track:"Every Breath You Take"']),

    ('Sting; the Police;test', 'Every Breath You Take [Acoustic]', QuerySplitMultipleArtists,
     ['artist:"Sting" AND track:"Every Breath You Take [Acoustic]"', 'artist:"Sting" AND track:"Every Breath You Take"',
      'artist:"the Police" AND track:"Every Breath You Take [Acoustic]"', 'artist:"the Police" AND track:"Every Breath You Take"',
      'artist:"Police" AND track:"Every Breath You Take [Acoustic]"', 'artist:"Police" AND track:"Every Breath You Take"',
      'artist:"test" AND track:"Every Breath You Take [Acoustic]"', 'artist:"test" AND track:"Every Breath You Take"']),

    ('Sting and the Police and test', 'Every Breath You Take', QueryMultipleAndArtists,
     ['artist:"Sting & the Police and test" AND track:"Every Breath You Take"']),

    ('Sting and the Police and test', 'Every Breath You Take (feat. test)', QueryMultipleAndArtists,
     ['artist:"Sting & the Police and test" AND track:"Every Breath You Take (feat. test)"',
      'artist:"Sting & the Police and test" AND track:"Every Breath You Take"']),

    ('Sting & the Police', 'Every Breath You Take', QueryMultipleAndSymbolArtists,
     ['artist:"Sting and the Police" AND track:"Every Breath You Take"']),

    ('Sting & the Police', 'Every Breath You Take featuring test', QueryMultipleAndSymbolArtists,
     ['artist:"Sting and the Police" AND track:"Every Breath You Take featuring test"',
      'artist:"Sting and the Police" AND track:"Every Breath You Take"']),

    ('Sting and the Police', 'Every Breath You Take', QuerySplitAndArtists,
     ['artist:"Sting" AND track:"Every Breath You Take"', 'artist:"the Police" AND track:"Every Breath You Take"',
      'artist:"Police" AND track:"Every Breath You Take"']),

    ('Sting and the Police', 'Every Breath You Take feat. test', QuerySplitAndArtists,
     ['artist:"Sting" AND track:"Every Breath You Take feat. test"', 'artist:"Sting" AND track:"Every Breath You Take"',
      'artist:"the Police" AND track:"Every Breath You Take feat. test"', 'artist:"the Police" AND track:"Every Breath You Take"',
      'artist:"Police" AND track:"Every Breath You Take feat. test"', 'artist:"Police" AND track:"Every Breath You Take"']),

    ('Sting & the Police & test', 'Every Breath You Take', QuerySplitAndSymbolArtists,
     ['artist:"Sting" AND track:"Every Breath You Take"', 'artist:"the Police" AND track:"Every Breath You Take"',
      'artist:"Police" AND track:"Every Breath You Take"', 'artist:"test" AND track:"Every Breath You Take"']),

    ('Sting & the Police & test', 'Every Breath You Take feat. test2', QuerySplitAndSymbolArtists,
     ['artist:"Sting" AND track:"Every Breath You Take feat. test2"', 'artist:"Sting" AND track:"Every Breath You Take"',
      'artist:"the Police" AND track:"Every Breath You Take feat. test2"', 'artist:"the Police" AND track:"Every Breath You Take"',
      'artist:"Police" AND track:"Every Breath You Take feat. test2"', 'artist:"Police" AND track:"Every Breath You Take"',
      'artist:"test" AND track:"Every Breath You Take feat. test2"', 'artist:"test" AND track:"Every Breath You Take"']),

    ('Sting', 'Shape of my heart', QueryWildcard,
     ['"Sting Shape of my heart"']),

    ('Sting', 'Shape of my heart feat. test', QueryWildcardCleanTitle,
     ['"Sting Shape of my heart"'])
])
def test_query_compile(artist, title, query_class, expected):
    actual = query_class(artist, title).compile()

    assert actual == expected
