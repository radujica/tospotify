# Setup

Currently pipenv focused; can adapt to your dev env.

    # activate virtual env where necessary
    pipenv shell
    
    # install the dev requirements
    pipenv install --dev
    # could also use the requirements; this is how to regenerate
    pip freeze > requirements.txt
    # above includes the dev, otherwise through pipenv can make them
    pipenv lock -r > requirements.txt
    pipenv lock --dev -r > requirements-dev.txt
    
    # build for publish
    python setup.py sdist
    # clean
    rm -rf dist tospotify.egg-info
    # check before publish
    twine check <dist/path>
    # publish
    twine upload -r pypi <dist/path>
    