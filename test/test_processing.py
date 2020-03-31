import pytest

from tospotify.processing import clean_name, process_song_name


@pytest.mark.parametrize('name,expected', [
    ('The Police', 'The Police'),
    (' The  Police   ', 'The Police'),
    ('St-ing;The, Police', 'Sting;The, Police'),
    ('ßtïngé', 'tng')
])
def test_clean_name(name, expected):
    assert clean_name(name) == expected


@pytest.mark.parametrize('song,expected', [
    ('Sting - Englishman in new york', ('Sting', 'Englishman in new york')),
    ('AC-DC - Hells Bells', ('AC', 'DC'))
])
def test_process_song_name(song, expected):
    assert process_song_name(song) == expected
