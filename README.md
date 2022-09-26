## Setup

1) Install [PyEnv](https://github.com/pyenv/pyenv)
2) Install Python 3.11 with PyEnv
    ```script
    $ pyenv install 3.11-dev
    ```
3) Install [Pipenv](https://pipenv.pypa.io/en/latest/)
4) Create and activate a venv using Pipenv
    ```script
    $ PIPENV_DOTENV_LOCATION=envs/dev.env pipenv shell --python 3.11-dev
    ```
5) Install dev-requirements
    ```script
    $ make install-dev-requirements
    ```
6) Install [pre-commit](https://pre-commit.com/) Git hook scripts 
    ```script
    $ pre-commit install
    ```

## Unit tests with code coverage measurement

1) Activate the previously created venv
    ```script
    $ PIPENV_DOTENV_LOCATION=envs/dev.env pipenv shell
    ```
2) Run the unit tests suite
    ```script
    $ make test-coverage
    ```