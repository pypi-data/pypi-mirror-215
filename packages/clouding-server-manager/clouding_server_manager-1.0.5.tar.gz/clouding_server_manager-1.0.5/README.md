# Clouding Server Manager
![Version](https://img.shields.io/badge/Version-1.0.5-brightgreen.svg)
![Python](https://img.shields.io/badge/Python-3.9-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

Clouding Server Manager is a Python project that allows you to manage your Clouding servers from the command line. It is designed to list, archive, and unarchive servers in your Clouding account. It uses the [Clouding API](https://api.clouding.io/docs) to perform the actions.

## Table of Contents
* [Features](#features)
* [Examples](#examples)
* [Installation with Poetry (recommended)](#installation-with-poetry-recommended)
* [Installation with pip](#installation-with-pip)
* [Installation as a PyPI package](#installation-as-a-pypi-package)
* [Development Setup](#development-setup)
* [Contributing](#contributing)
* [License](#license)

## Features
* Simple and easy to use command line interface.
* List all the information about your Clouding servers and filter their fields so that you can see only the information you want.
* Archive one or multiple servers at once.
* Unarchive one or multiple servers at once.

## Examples
These are just a few examples of how to use the script. For more information, check out the help message by running `python -m clouding_server_manager --help`.
* List all servers:
    ```bash
    python -m clouding_server_manager list -t all
    ```
* List all servers and filter their fields:
    ```bash
    python -m clouding_server_manager list -t all --f id -f name
    ```
* Archive a server:
    ```bash
    python -m clouding_server_manager archive -t 123456
    ```
* Archive multiple servers:
    ```bash
    python -m clouding_server_manager archive -t 123456 -t 789012
    ```
* Unarchive a server:
    ```bash
    python -m clouding_server_manager unarchive -t 123456
    ```
* Unarchive multiple servers:
    ```bash
    python -m clouding_server_manager unarchive -t 123456 -t 789012
    ```

## Installation with Poetry (recommended)
To set up the project, follow these steps:
1. Make sure you have [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) installed in your system.
2. It is highly recommended to set this Poetry configuration parameters to avoid multiple issues:
    ```bash
    poetry config virtualenvs.in-project true
    poetry config virtualenvs.prefer-active-python true
    ```
3. Clone the repository:
    ```bash
    git clone https://github.com/dmarts05/clouding-server-manager
    ```
4. Navigate to the project directory:
    ```bash
    cd clouding-server-manager
    ```
5. Install the project dependencies using Poetry:
    ```bash
    poetry install
    ```
    You might need [pyenv](https://github.com/pyenv/pyenv) to install the Python version specified in the `pyproject.toml` file. If that's the case, run `pyenv install 3.9` before running the previous command. Also, check out the [Poetry documentation about pyenv](https://python-poetry.org/docs/managing-environments/) for more information.
6. Activate the virtual environment:
    ```bash
    poetry shell
    ```
    This will activate the virtual environment so that you can run the script.
7. Enter your Clouding API key in the `.env` file. Check out `.env.sample` for an example. You can find your Clouding API key in the API section of your Clouding account (as of now you need access to the beta version of the Clouding API). As an alternative, you can use --api-key or -k to specify your API key when running the script.
8. Run the script:
    ```bash
    python -m clouding_server_manager --help
    ```
    or
    ```bash
    poetry run clouding-sm --help
    ```
    This will display the help message and show you how to use the script.

## Installation with pip
This is an alternative installation method that uses pip instead of Poetry. It might not work as expected, so it is recommended to use the Poetry installation method instead. To set up the project, follow these steps:
1. Clone the repository:
    ```bash
    git clone https://github.com/dmarts05/clouding-server-manager
    ```
2. Navigate to the project directory:
    ```bash
    cd clouding-server-manager
    ```
3. Install the project dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```
    You might need [pyenv](https://github.com/pyenv/pyenv) to install the Python version specified in the `requirements.txt` file.
4. Enter your Clouding API key in the `.env` file. Check out `.env.sample` for an example. You can find your Clouding API key in the API section of your Clouding account (as of now you need access to the beta version of the Clouding API). As an alternative, you can use --api-key or -k to specify your API key when running the script.
5. Run the script:
    ```bash
    python -m clouding_server_manager --help
    ```
    or
    ```bash
    poetry run clouding-sm --help
    ```
    This will display the help message and show you how to use the script.

## Installation as a PyPI package
This is an alternative installation method that uses pip to install the package from PyPI. It might not work as expected, so it is recommended to use the Poetry installation method instead. To set up the project, follow these steps:
1. Install the package using pip:
    ```bash
    pip install clouding-server-manager
    ```
2. Configure the environment variable with `export` or by adding them to your `.bashrc` or `.zshrc` file:
    ```bash
    export CLOUDING_API_KEY="YOUR API KEY"
    ```
    You can find your Clouding API key in the API section of your Clouding account (as of now you need access to the beta version of the Clouding API). As an alternative, you can use --api-key or -k to specify your API key when running the script.
2. Run the script:
    ```bash
    clouding-sm --help
    ```
    This will display the help message and show you how to use the script.

## Development Setup
If you want to contribute to the project or run the development environment, follow these additional steps:
1. Install the development dependencies:
    ```bash
    poetry install --with dev
    ```
2. Install pre-commit hooks:
    ```bash
    poetry run pre-commit install
    ```
3. Format the code:
    ```bash
    poetry run black clouding_server_manager
    ```
4. Lint the code:
    ```bash
    poetry run flake8 clouding_server_manager
    ```
5. Run static type checking:
    ```bash
    poetry run mypy clouding_server_manager
    ```
6. Generate the documentation:
    ```bash
    cd docs && poetry run make html
    ```
7. Do everything at once (except for generating the documentation):
    ```bash
    poetry run pre-commit run --all-files
    ```
That's it! You now have the project set up and ready for development or execution.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/). See the [LICENSE](LICENSE) file for details.