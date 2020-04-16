from unittest.mock import patch, Mock

import pytest

import tospotify


@patch('tospotify.search._run_query')
@pytest.mark.parametrize('song,_run_query_results,expected', [
    ('Sting - Every Breath You Take', [None, 'uri1'], 'uri1'),
    ('Sting - Every Breath You Take', ['uri1', 'uri2'], 'uri1'),
])
def test__find_track(mock__run_query, song, _run_query_results, expected):
    mock_song = Mock()
    mock_song.title.return_value = song
    mock__run_query.side_effect = _run_query_results

    actual = tospotify.search._find_track(None, mock_song)

    assert actual == expected
