# Convert local playlist to Spotify playlist

## Requirements
Need to setup some environment variables before running:

### Linux

    export SPOTIPY_CLIENT_ID="<paste-from-dev-dashboard>"
    export SPOTIPY_CLIENT_SECRET="<paste-from-dev-dashboard>"
    # note that it needs to be whitelisted in the dev dashboard!
    # for local can just use "http://localhost:8888"
    export SPOTIPY_REDIRECT_URI="<your-chosen-uri>"
    
    for username you need to find your id; only way i could find was by logging in
    to open.spotify.com, open develop console (F12) and go to network, click Your Library,
    now find the "playlists" request and there you'll see the full url with the user id
    i.e. https://api.spotify.com/v1/users/<id>/playlists