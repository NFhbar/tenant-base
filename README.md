# Tenant Base Backend

[![CircleCI](https://circleci.com/gh/NFhbar/tenant-base.svg?style=svg)](https://circleci.com/gh/NFhbar/tenant-base)
[![Coverage Status](https://coveralls.io/repos/github/NFhbar/tenant-base/badge.svg?branch=master)](https://coveralls.io/github/NFhbar/tenant-base?branch=master)

Simple key-value storage which implements a small subset of the [memcached protocol](https://memcached.org/).
Data is persisted through [SQLite](https://www.sqlite.org/index.html).

## Requirements
- [Python 3.6](https://www.python.org/downloads/release/python-360/)
- [Pip](https://pypi.org/project/pip/)
- [Memcached](https://memcached.org/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/) - optional
- [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html) - optional

## Installation
In your local machine, clone this repo then create a new `virtualenv`:
```
$ git clone git@github.com:NFhbar/tenant-base.git
$ cd tenant-base
$ mvirtualenv tenant-base
```

If there are issues with `python` version you can force `3.6` by using:
```
$ mkvirtualenv --python=`which python3` tenant-base
```

Install the requirements:
```
(tenant-base) $ pip install -r requirements.txt
```

## Usage
To print the help menu:
```
(tenant-base) $ python3 main.py -h
```

The program assumes that there is a `database.sqlite` file in root. If it does not exist the program will create it along with a `key_value` table.

To view all existing key-value pairs:
```
(tenant-base) $ python3 main.py -sh database.sqlite
```

To enter the memcached-interface:
```
(tenant-base) $ python3 main.py -s database.sqlite
```

The interface options are:
```
Interface options:
 - set key value exptime
 - get key
 - delete key
 - exit
```

Note: `exptime` is the expiration time for the key-value pair. This value is ignored.

## Unit Tests
To run the unit tests:
```
(tenant-base) $ python3 -m pytest --cov-report term-missing --cov=main tests/ -s
```
## Pylint
`Pylint` is configured through `.pylintrc`.

To run:
```
(tenant-base) $ pylint main.py
```
## Contact
Nicolas Frega

`frega.nicolas@gmail.com`
