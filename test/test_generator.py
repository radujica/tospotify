import pytest

from tospotify.generator import QueryGenerator


@pytest.mark.parametrize('artist,title,expected', [
    ('Sting', 'Every Breath',
     ['artist:"Sting" AND track:"Every Breath"', '"Sting Every Breath"']),

    ('The Police', 'Every Breath',
     ['artist:"The Police" AND track:"Every Breath"', 'artist:"Police" AND track:"Every Breath"',
      '"The Police Every Breath"', '"Police Every Breath"']),

    ('Sting; The Police', 'Every Breath',
     ['artist:"Sting; The Police" AND track:"Every Breath"',
      'artist:"Sting" AND track:"Every Breath"', 'artist:"The Police" AND track:"Every Breath"',
      '"Sting; The Police Every Breath"', '"Sting Every Breath"', '"The Police Every Breath"']),

    ('Sting and The Police', 'Every Breath',
     ['artist:"Sting and The Police" AND track:"Every Breath"',
      'artist:"Sting & The Police" AND track:"Every Breath"',
      'artist:"Sting" AND track:"Every Breath"', 'artist:"The Police" AND track:"Every Breath"',
      '"Sting and The Police Every Breath"', '"Sting & The Police Every Breath"',
      '"Sting Every Breath"', '"The Police Every Breath"']),

    ('The Police', 'Every Breath feat. Sting',
     ['artist:"The Police" AND track:"Every Breath feat. Sting"', 'artist:"The Police" AND track:"Every Breath"',
      'artist:"Police" AND track:"Every Breath feat. Sting"', 'artist:"Police" AND track:"Every Breath"',
      '"The Police Every Breath feat. Sting"', '"The Police Every Breath"',
      '"Police Every Breath feat. Sting"', '"Police Every Breath"']),

    ('Sting and The Police', 'Every Breath [Acoustic]',
     ['artist:"Sting and The Police" AND track:"Every Breath [Acoustic]"', 'artist:"Sting and The Police" AND track:"Every Breath"',
      'artist:"Sting & The Police" AND track:"Every Breath [Acoustic]"', 'artist:"Sting & The Police" AND track:"Every Breath"',
      'artist:"Sting" AND track:"Every Breath [Acoustic]"', 'artist:"The Police" AND track:"Every Breath [Acoustic]"',
      'artist:"Sting" AND track:"Every Breath"', 'artist:"The Police" AND track:"Every Breath"',
      '"Sting and The Police Every Breath [Acoustic]"', '"Sting and The Police Every Breath"',
      '"Sting & The Police Every Breath [Acoustic]"', '"Sting & The Police Every Breath"',
      '"Sting Every Breath [Acoustic]"', '"The Police Every Breath [Acoustic]"',
      '"Sting Every Breath"', '"The Police Every Breath"'])
])
def test_generator(artist, title, expected):
    generator = QueryGenerator(artist, title)
    actual = list(generator.generate())

    assert actual == expected
