# Setup

    # install the dev requirements
    pipenv install --dev
    
    # run tests
    pipenv run pytest test
    
    # run linter
    pipenv run pylint tospotify
    # regenerate default linter rcfile
    pipenv run pylint --generate-rcfile > .pylintrc
    