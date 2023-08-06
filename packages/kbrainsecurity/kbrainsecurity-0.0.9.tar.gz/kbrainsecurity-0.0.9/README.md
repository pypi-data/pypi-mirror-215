# kbrain-security

Common security and authentication functions / decorators for KBRAIN projects.

## Setup

### poetry 

(Poetry)[https://python-poetry.org/docs/] is used to manage project dependencies at the KBRain level. The python version is specified in the `pyproject.toml` file. A virtual environment can be created by running the command:

`poetry shell`

From there, dependencies can be installed by typing

`poetry install`

## pre-commit

Once dependencies have been installed via poetry, use the `pre-commit install` command to configure pre-commit. 

## Development

Create a feature branch and push your changes there. Open a PR on GitHub. This will trigger CICD and publish a prerelease version of the package with appropriate tags and updates to the pyproject.toml file. Merging a PR into main increments the patch version of the release and tags it appropriately. At this time this package can be installed in KBRAIN services with `pipenv` using the `git` protocol.