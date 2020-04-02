import pytest

from tospotify.types.artists import (
    Artist,
    ArtistBeginsWithThe,
    MultipleArtist,
    MultipleTogetherArtist,
    MultipleTogetherAndArtist,
    MultipleTogetherAndSymbolArtist,
    MultipleSplitArtist,
    MultipleSplitSemicolonArtist,
    MultipleSplitAndArtist,
    MultipleSplitAndSymbolArtist,
    SEP_AND_SYMBOL,
    SEP_AND,
    SEP_SEMICOLON
)


@pytest.mark.parametrize('artist,artist_class,artist_args,expected_sense,expected_process', [
    ('Sting', Artist, (), True, ['Sting']),
    ('The Police', ArtistBeginsWithThe, (), True, ['Police']),
    ('Police', ArtistBeginsWithThe, (), False, ['ce']),
    ('Sting & The Police', MultipleArtist, (SEP_AND_SYMBOL,), True, ['Sting & The Police']),
    ('Sting and The Police', MultipleArtist, (SEP_AND_SYMBOL,), False, ['Sting and The Police']),
    ('Sting & The Police', MultipleTogetherArtist, (SEP_AND_SYMBOL, SEP_AND), True, ['Sting and The Police']),
    ('Sting and The Police', MultipleTogetherArtist, (SEP_AND_SYMBOL, SEP_AND), False, ['Sting and The Police']),
    ('Sting and The Police', MultipleTogetherAndArtist, (), True, ['Sting & The Police']),
    ('Sting & The Police', MultipleTogetherAndArtist, (), False, ['Sting & The Police']),
    ('Sting & The Police', MultipleTogetherAndSymbolArtist, (), True, ['Sting and The Police']),
    ('Sting and The Police', MultipleTogetherAndSymbolArtist, (), False, ['Sting and The Police']),
    ('Sting; The Police', MultipleSplitArtist, (SEP_SEMICOLON,), True, ['Sting', 'The Police']),
    ('Sting The Police', MultipleSplitArtist, (SEP_SEMICOLON,), False, ['Sting The Police']),
    ('Sting; The Police', MultipleSplitSemicolonArtist, (), True, ['Sting', 'The Police']),
    ('Sting The Police', MultipleSplitSemicolonArtist, (), False, ['Sting The Police']),
    ('Sting and The Police', MultipleSplitAndArtist, (), True, ['Sting', 'The Police']),
    ('Sting; The Police', MultipleSplitAndArtist, (), False, ['Sting; The Police']),
    ('Sting & The Police', MultipleSplitAndSymbolArtist, (), True, ['Sting', 'The Police']),
    ('Sting; The Police', MultipleSplitAndSymbolArtist, (), False, ['Sting; The Police']),

    ('Sting; The Police; test', MultipleSplitSemicolonArtist, (), True, ['Sting', 'The Police', 'test']),
])
def test_artists(artist, artist_class, artist_args, expected_sense, expected_process):
    actual = artist_class(artist, *artist_args)

    assert actual.makes_sense() == expected_sense
    assert list(actual.process()) == expected_process
