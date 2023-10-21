# Convert local playlists to Spotify playlists

![Build, Test, Lint](https://github.com/radujica/tospotify/workflows/Build,%20Test,%20Lint/badge.svg)
[![PyPI version](https://badge.fury.io/py/tospotify.svg)](https://badge.fury.io/py/tospotify)

Supports m3u and m3u8 files in the [Extended format](https://en.wikipedia.org/wiki/M3U) encoded as UTF-8.

Take a look [below](#help) for more details and debugging tips.

## Usage

    usage: tospotify [-h] [--verbose] [--public] [--convert]
                     [--playlist-id PLAYLIST_ID]
                     spotify_username playlist_path
    
    Create/update a Spotify playlist from a local m3u playlist
    
    positional arguments:
      spotify_username      Spotify username where playlist should be updated.
                            Your email address should work just fine, or could
                            find your user id through e.g. the developer console
      playlist_path         full path to the playlist
    
    optional arguments:
      -h, --help            show this help message and exit
      --verbose             print all the steps when searching for songs
      --public              playlist is public, otherwise private
      --convert             convert from locale default to utf-8
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
1. Python > 3.6
2. Enable Developer Dashboard and your 'app'.

    - Go to https://developer.spotify.com/dashboard/login
    - Create an app
    - Get the client id and client secret from there for step 2
    - Edit settings and whitelist a redirect uri; for default use `http://localhost:8888`
    
3. Setup some environment variables:

### Linux

    export SPOTIPY_CLIENT_ID="<paste-from-dev-dashboard>"
    export SPOTIPY_CLIENT_SECRET="<paste-from-dev-dashboard>"
    export SPOTIPY_REDIRECT_URI="<your-chosen-uri>"
    
### Windows
Same as linux but use `set` instead of `export`


## Help

### Encoding

Seeing unexpected characters in the log messages is a sign of faulty encoding.

This tool uses [m3u8](https://github.com/globocom/m3u8) library to parse the files, which relies on utf-8.

Encoding can be checked by opening the playlist in a text editor, such as Notepad++.
If the playlist is in a different encoding, 
try using the `--convert` argument which will attempt to convert it to utf-8.

Alternatively, could try importing the playlist into your music player and using its export function 
to export as utf-8, if it exists. AIMP, for example, can do this.

### Songs missing

This might happen when the file is not actually in the [extended m3u](https://en.wikipedia.org/wiki/M3U) format. 
This format looks like

    #EXTM3U
    #EXTINF:277,Faun - Sieben Raben
    /Music/Selection/Faun - Sieben Raben.mp3
    
and is populated from file tags. For this example, the mp3 file contains the tags 
artist = Faun and title = Sieben Raben which then populate the `#EXTINF` line.

If your playlist only contain paths, try importing it in a (different) music player and exporting again.
AIMP, for example, exports in the expected format.

### What does tospotify actually do internally?

It tries various cleaning steps and search queries in an attempt to find the correct songs on Spotify.

The [extended m3u](https://en.wikipedia.org/wiki/M3U) format is important. As mentioned above, the ground truth
is actually the artist and title tags stored in the songs themselves which are then reflected in the playlist.
Looking at the example above, the format is essentially `artist - title`; this implicitly means that dashes `-`
in the artist or title cannot be interpreted properly at the moment. Sorry, AC-DC :(

The tool then uses rules to compute various queries. Take for example the song 
`Every Breath You Take` by `Sting and the Police`. This can be stored in many ways. The artist could be
`Sting and the Police`, `Sting;The Police`, `Sting & the Police`, `The Police`, etc.
Then the title could be `Every Breath You Take` but also `Every Breath You Take feat. Sting` and other
variations. Many of these are not found exactly as such on Spotify.

There can also be live versions, e.g. with title `Every Breath You Take [live]`,
covers by other artists, separate recordings of the song,
and the list goes on. This song was actually recorded both by The Police with Sting
and solo by Sting; both versions are available on Spotify!

Bit more complex than it initially seems :)

So this is what tospotify does; it will try to find the correct song through various rules derived from the data in the 
playlist.


## Contributing

Take a look at the [CONTRIBUTING](CONTRIBUTING.md) file for more details. Pull requests are welcome!
