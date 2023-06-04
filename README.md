# innovation-merge
Core modules of innovation merge projects

## readme of the innovationmerge

- Author : innovationmerge
- Version: 1.0
- Description: innovationmerge core components

#### Requirements: 
- Python > 3.7
- `pip install poetry`

### Add Environmental variables
```
Note: ENVIRONMENT should be passed as argument to main.py but code gives priority to Operating System Environmental variables
```
- If OS is Windows
```
    # If Development Environment
        - set ENVIRONMENT=development

    # If Production Environment
        - set ENVIRONMENT=production

    # If Test Environment
        - set ENVIRONMENT=test
```
- If OS is Linux
```
    # If Development Environment
        - export ENVIRONMENT=development

    # If Production Environment
        - export ENVIRONMENT=production

    # If Test Environment
        - export ENVIRONMENT=test
```

#### Run the project using poetry
- `poetry install`
- `poetry run python main.py <ENVIRONMENT>`

#### Add project dependencies using poetry 
- `poetry add package_name`

#### List project dependencies using poetry 
- `poetry show --tree`

#### Check latest version of a project dependencies using poetry 
- `poetry show --latest`

#### Update project dependencies using poetry 
- `poetry update`

#### Check project virtual environment path using poetry 
- `poetry env info --path`

#### Test the project using poetry and Pytest
- `poetry run pytest`

#### Auto fix Linting issues of the project using poetry and black
- `black <folder>`

#### Check Linting of the project using poetry and flake8
- `poetry run flake8`

#### Test the code with multiple python versions and linting problems using poetry and tox
- `poetry run tox`

#### Build the project using poetry
-  `poetry build`

#### Add pypi api token 
- `poetry config pypi-token.pypi your-api-token`

#### Publish to pypi 
- `poetry publish`

#### Build and Publish to pypi 
- `poetry publish --build`

#### Code Security check
-  `poetry run bandir -r .`

#### Generate exe file
-  `poetry run pyinstaller main.py`