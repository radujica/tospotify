import pytest

from tospotify.processing import clean_name, process_song_name


@pytest.mark.parametrize('name,expected', [
    ('The Police', 'the police'),
    (' The  Police   ', 'the police'),
    ('St-ing;The, Police', 'sting;the, police'),
    ('ßtïngé', 'tng')
])
def test_clean_name(name, expected):
    assert clean_name(name) == expected


@pytest.mark.parametrize('song,expected', [
    ('Sting - Englishman in new york', ('sting', 'englishman in new york')),
    ('AC-DC - Hells Bells', ('ac', 'dc'))
])
def test_process_song_name(song, expected):
    assert process_song_name(song) == expected
