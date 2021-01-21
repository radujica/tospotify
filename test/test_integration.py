import os
from unittest.mock import patch

import pytest

from tospotify.run import main


class MockArgs:
    def __init__(self, playlist_path, playlist_id=None):
        self.verbose = False
        self.spotify_username = 'test_username'
        self.public = True
        self.playlist_path = playlist_path
        self.playlist_id = playlist_id


# the point here is to run through the whole flow
@patch('tospotify.run._parse_args')
@patch('tospotify.run.prompt_for_user_token', lambda x, y: 'token')
@patch('tospotify.search._find_track', lambda x, y, z: 'uri')
@patch('tospotify.search.add_tracks', lambda x, y, z: None)
@pytest.mark.parametrize('playlist', [
    os.path.join('test', 'data', 'valid_playlist.m3u'),
    os.path.join('test', 'data', 'empty_playlist.m3u'),
    os.path.join('test', 'data', 'empty_playlist.m3u')
])
def test_integration(mock_function, playlist):
    mock_function.return_value = MockArgs(playlist_path=playlist, playlist_id=1)
    main()
