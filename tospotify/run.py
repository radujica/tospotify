import argparse
import logging
import os

from spotipy import Spotify
from spotipy.util import prompt_for_user_token

from tospotify import create_spotify_playlist, update_spotify_playlist


def parse_args():
    parser = argparse.ArgumentParser(description='Create/update a Spotify playlist from a local m3u playlist')
    parser.add_argument('spotify_username', help='Spotify username where playlist should be updated', type=str)
    parser.add_argument('playlist_path', help='full path to the playlist', type=str)
    parser.add_argument('-v', '--verbose', help='print all the steps when searching for songs', action='store_true')
    parser.add_argument('--public', help='playlist is public, otherwise private', action='store_true')
    parser.add_argument('--playlist-id', help='do not create a new playlist, '
                                              'instead update the existing playlist with this id', type=str)
    parsed_args = parser.parse_args()

    return parsed_args


def main():
    args = parse_args()

    logger = logging.getLogger()
    logger_level = logging.INFO if args.verbose else logging.WARNING
    logger.setLevel(logger_level)

    # required by Spotipy for authorization code flow
    os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:8888'

    username = args.spotify_username
    scope = 'playlist-modify-public' if args.public else 'playlist-modify-private'
    token = prompt_for_user_token(username, scope)

    if token is None:
        logging.error('Could not acquire token!')

    sp = Spotify(auth=token)

    if args.playlist_id is None:
        _, filename = os.path.split(args.playlist_path)
        playlist_name = str(filename.split('.')[0])
        playlist_id = create_spotify_playlist(sp, playlist_name)
        logging.info('Created playlist with name={} at id={}'.format(playlist_name, playlist_id))
    else:
        playlist_id = args.playlist_id
        logging.info('Updating existing playlist with id={}'.format(playlist_id))

    update_spotify_playlist(sp, args.playlist_path, playlist_id)
