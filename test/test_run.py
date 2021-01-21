import argparse
import os
from unittest.mock import patch

import pytest

from tospotify.run import _parse_path, _m3u_file


@patch('os.getcwd', lambda: '/test/path')
@pytest.mark.parametrize('path,expected', [
    ('/abs/path', ['/abs/path']),
    ('relative/path', ['/test/path', 'relative/path'])
])
def test__parse_path(path, expected):
    assert _parse_path(path) == os.sep.join(expected)


@pytest.mark.parametrize('playlist_path', [
    'path/to/file.m3u',
    'file.m3u'
])
def test__m3u_extension(playlist_path):
    _m3u_file(playlist_path)


@pytest.mark.parametrize('playlist_path', [
    'path/to/file.m3u8',
    'file.m3u8',
    'path/file.mp3',
    '.m3u',
    'file'
])
def test__m3u_extension_invalid(playlist_path):
    with pytest.raises(argparse.ArgumentTypeError):
        _m3u_file(playlist_path)
