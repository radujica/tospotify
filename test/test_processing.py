import pytest

from tospotify.processing import clean_name, process_song_name, clean_title


@pytest.mark.parametrize('name,expected', [
    ('The Police', 'the police'),
    (' The  Police   ', 'the police'),
    ('St-ing; The, Police', 'sting; the, police'),
    ('ßtïngé', 'tng'),
    ('é', ''),
    ('Every Breath You Take (feat. Sting)', 'every breath you take (feat sting)'),
    ('Every Breath You Take [Acoustic]', 'every breath you take [acoustic]')
])
def test_clean_name(name, expected):
    assert clean_name(name) == expected


@pytest.mark.parametrize('song,expected', [
    ('Sting - Englishman in new york', ('sting', 'englishman in new york')),
    ('AC-DC - Hells Bells', ('ac', 'dc'))
])
def test_process_song_name(song, expected):
    assert process_song_name(song) == expected


@pytest.mark.parametrize('title,expected', [
    ('every breath you take (feat. sting)', 'every breath you take'),
    ('every breath you take featuring sting', 'every breath you take'),
    ('every breath you take [acoustic]', 'every breath you take'),
    ('every breath you take (feat. sting)[acoustic]', 'every breath you take'),
    ('every breath you take [acoustic](feat. sting)', 'every breath you take')
])
def test_clean_title(title, expected):
    assert clean_title(title) == expected
