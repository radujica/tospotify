# Convert local playlist to Spotify playlist

![Build, Test, Lint](https://github.com/radujica/tospotify/workflows/Build,%20Test,%20Lint/badge.svg)
[![PyPI version](https://badge.fury.io/py/tospotify.svg)](https://badge.fury.io/py/tospotify)

Currently works for m3u files; m3u8 support to come!

## Usage

    usage: tospotify [-h] [-v] [--public] [--playlist-id PLAYLIST_ID]
                     spotify_username playlist_path
    
    Create/update a Spotify playlist from a local m3u playlist
    
    positional arguments:
      spotify_username      Spotify username where playlist should be updated.
                            Your email address should work just fine, or could
                            find your user id through e.g. the developer console
      playlist_path         full path to the playlist
    
    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         print all the steps when searching for songs
      --public              playlist is public, otherwise private
      --playlist-id PLAYLIST_ID
                            do not create a new playlist, instead update the
                            existing playlist with this id
                            
### Example
* Linux/MacOS

        tospotify --verbose "john.doe@gmail.com" "D:/playlist/name.m3u"
        
* Windows*

        python -m tospotify "john.doe@gmail.com" "D:/playlist/name.m3u"
        
\*`entry_points` does not seem to simply work on Windows 


## Requirements
1. First need to enable Developer Dashboard and your 'app'.

    - Go to https://developer.spotify.com/dashboard/login
    - Create an app
    - Get the client id and client secret from there for step 2
    - Edit settings and whitelist a redirect uri; for default use `http://localhost:8888`
    
2. Setup some environment variables:

### Linux

    export SPOTIPY_CLIENT_ID="<paste-from-dev-dashboard>"
    export SPOTIPY_CLIENT_SECRET="<paste-from-dev-dashboard>"
    export SPOTIPY_REDIRECT_URI="<your-chosen-uri>"
    
### Windows
Same as linux but use `set` instead of `export`
    