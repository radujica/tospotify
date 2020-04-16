import argparse
import logging
import os

from spotipy import Spotify
from spotipy.util import prompt_for_user_token

from .search import create_spotify_playlist, update_spotify_playlist


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Create/update a Spotify playlist from a local m3u playlist')
    parser.add_argument('spotify_username',
                        help='Spotify username where playlist should be updated. '
                             'Your email address should work just fine, or could find your user id '
                             'through e.g. the developer console', type=str)
    parser.add_argument('playlist_path', help='full path to the playlist', type=str)
    parser.add_argument('--verbose', help='print all the steps when searching for songs', action='store_true')
    parser.add_argument('--public', help='playlist is public, otherwise private', action='store_true')
    parser.add_argument('--playlist-id', help='do not create a new playlist, '
                                              'instead update the existing playlist with this id', type=str)
    parsed_args = parser.parse_args()

    return parsed_args


def _parse_path(path: str) -> str:
    if path.startswith('/'):
        return path

    return os.path.join(os.getcwd(), *path.split(os.sep))


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
        _, filename = os.path.split(playlist_path)
        playlist_name = str(filename.split('.')[0])
        playlist_id = create_spotify_playlist(spot, playlist_name)
        logging.info('Created playlist with name={} at id={}'.format(playlist_name, playlist_id))
    else:
        playlist_id = args.playlist_id
        logging.info('Updating existing playlist with id={}'.format(playlist_id))

    update_spotify_playlist(spot, playlist_path, playlist_id)
