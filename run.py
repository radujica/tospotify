import os

from spotipy import Spotify
from spotipy.util import prompt_for_user_token

from tospotify import create_spotify_playlist, update_spotify_playlist

playlist_path = 'D:/Workspace/The Mix.m3u'


def get_token(username):
    scope = 'playlist-modify-private'
    token = prompt_for_user_token(username, scope)

    return token


def main():
    username = os.getenv('SPOTIPY_USERNAME')
    token = get_token(username)

    if token:
        sp = Spotify(auth=token)
        # TODO: add option to just use the passed id
        playlist_id = create_spotify_playlist(sp, 'The Mix')
        update_spotify_playlist(sp, playlist_path, playlist_id)
    else:
        print('no token :(')


main()
