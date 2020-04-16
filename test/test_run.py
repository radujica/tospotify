import os
from unittest.mock import patch

import pytest

from tospotify.run import _parse_path


@patch('os.getcwd', lambda: '/test/path')
@pytest.mark.parametrize('path,expected', [
    ('/abs/path', ['/abs/path']),
    ('relative/path', ['/test/path', 'relative/path'])
])
def test__parse_path(path, expected):
    assert _parse_path(path) == os.sep.join(expected)
