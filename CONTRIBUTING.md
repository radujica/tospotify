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
    
Publishing to pypi is handled through github releases and action.
    