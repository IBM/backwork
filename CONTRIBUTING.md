# Contributing

## Development

### Setup virtual environment
```
$ virtualenv venv --python=python3
$ source venv/bin/activate
```

### Install dependencies
```
$ pip install -r requirements.txt
```
### Install the plug-in in editable mode
```
$ pip install -e .
```

## Releasing a new version
To publish a new PyPI release, update the version in [setup.py](setup.py) on the master branch
and create a new GitHub release. Travis will build and publish a new release on PyPI.
