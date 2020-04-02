import pytest

from tospotify.types.titles import Title, CleanedTitle


@pytest.mark.parametrize('title,title_class,expected_sense,expected_process', [
    ('Every Breath You Take', Title, True, 'Every Breath You Take'),
    ('Every Breath You Take', CleanedTitle, False, 'Every Breath You Take'),
    ('Every Breath You Take feat. Sting', CleanedTitle, True, 'Every Breath You Take')
])
def test_titles(title, title_class, expected_sense, expected_process):
    actual = title_class(title)

    assert actual.makes_sense() == expected_sense
    assert actual.process() == expected_process
