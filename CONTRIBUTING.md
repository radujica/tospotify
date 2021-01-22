# Setup

Currently pipenv focused; can adapt to your dev env.
Check out the Makefile for the common commands.

    # activate virtual env where necessary
    pipenv shell
    
    # install the dev requirements
    pipenv install --dev
    # could also use the requirements; this is how to regenerate but note that it's ALL of them
    pip freeze > requirements.txt
    # above includes the dev, otherwise through pipenv can make them
    pipenv lock -r > requirements.txt
    pipenv lock --dev -r > requirements-dev.txt
    
Publishing to pypi is handled through github releases and action, 
though version in setup.py needs to be manually bumped.

# Current ideas

- Use more data from the playlist or even the song tags themselves to more accurately find songs, e.g. song duration,
year, album artist
- Try removing the "the" from song names; `The Wolven Storm` is not the same as `Wolven Storm`
- Compute some similarity metrics after finding matches on Spotify; taking the example above, atm can't know which 
one to search first but after seeing the artist from each attempt, one could deduce the correct one
    