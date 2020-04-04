# Setup

Currently pipenv focused; can adapt to your dev env.

    # install the dev requirements
    pipenv install --dev
    # could also use the requirements; this is how to regenerate
    pip freeze > requirements.txt
    # above includes the dev, otherwise through pipenv can make them
    pipenv lock -r > requirements.txt
    pipenv lock --dev -r > requirements.txt
    
    # run tests
    pipenv run pytest test
    
    # run linter
    pipenv run pylint tospotify
    # regenerate default linter rcfile
    pipenv run pylint --generate-rcfile > .pylintrc
    