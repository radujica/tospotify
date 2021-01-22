import argparse
import logging
import os
from typing import Optional

from spotipy import Spotify
from spotipy.util import prompt_for_user_token

from .search import create_spotify_playlist, update_spotify_playlist


def _m3u_file(path: str) -> Optional[str]:
    if not isinstance(path, str):
        raise argparse.ArgumentTypeError('Path must be a string. Encountered type={}'.format(str(type(path))))

    splits = path.rsplit('.', 1)
    if len(splits) == 1:
        raise argparse.ArgumentTypeError('Could not determine file extension')

    filename, extension = splits[0], splits[1]
    if len(filename) == 0:
        raise argparse.ArgumentTypeError('Filename without extension cannot be empty')

    if extension in {'m3u', 'm3u8'}:
        return path

    raise argparse.ArgumentTypeError('Only m3u files are supported. Encountered={}'.format(extension))


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Create/update a Spotify playlist from a local m3u playlist')
    parser.add_argument('spotify_username',
                        help='Spotify username where playlist should be updated. '
                             'Your email address should work just fine, or could find your user id '
                             'through e.g. the developer console', type=str)
    parser.add_argument('playlist_path', help='full path to the playlist', type=_m3u_file)
    parser.add_argument('--verbose', help='print all the steps when searching for songs', action='store_true')
    parser.add_argument('--public', help='playlist is public, otherwise private', action='store_true')
    parser.add_argument('--convert', help='convert from locale default to utf-8', action='store_true')
    parser.add_argument('--playlist-id', help='do not create a new playlist, '
                                              'instead update the existing playlist with this id', type=str)
    parsed_args = parser.parse_args()

    return parsed_args


def _parse_path(path: str) -> str:
    if path.startswith('/'):
        return path

    return os.path.join(os.getcwd(), *path.split(os.sep))


def _extract_playlist_name(playlist_path: str) -> str:
    _, filename = os.path.split(playlist_path)
    playlist_name = str(filename.split('.')[0])

    return playlist_name


def main() -> None:
    """ Main entry point to the script """
    args = _parse_args()

    logger = logging.getLogger()
    logger_level = logging.INFO if args.verbose else logging.WARNING
    logger.setLevel(logger_level)

    username = args.spotify_username
    scope = 'playlist-modify-public' if args.public else 'playlist-modify-private'
    token = prompt_for_user_token(username, scope)
    playlist_path = _parse_path(args.playlist_path)

    if token is None:
        logging.error('Could not acquire token!')

    spot = Spotify(auth=token)

    if args.playlist_id is None:
        playlist_name = _extract_playlist_name(playlist_path)
        playlist_id = create_spotify_playlist(spot, playlist_name)
        logging.info('Created playlist with name={} at id={}'.format(playlist_name, playlist_id))
    else:
        playlist_id = args.playlist_id
        logging.info('Updating existing playlist with id={}'.format(playlist_id))

    update_spotify_playlist(spot, playlist_path, playlist_id, args.convert)
