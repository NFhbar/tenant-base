# Tenant Base Backend

[![CircleCI](https://circleci.com/gh/NFhbar/tenant-base.svg?style=svg)](https://circleci.com/gh/NFhbar/tenant-base)

[![Coverage Status](https://coveralls.io/repos/github/NFhbar/tenant-base/badge.svg?branch=issue_1)](https://coveralls.io/github/NFhbar/tenant-base?branch=issue_1)

Simple key-value storage which implements a small subset of the [memcached protocol](https://memcached.org/).
Data is persisted through [SQLite](https://www.sqlite.org/index.html).

## Requirements
- Python 3.6
- Pip

## Installation & Usage
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

To run the cli:
```
(tenant-base) $ python3 main.py
```

## Unit Tests
To run the unit tests:
```
(tenant-base) $ python3 -m pytest --cov-report term-missing --cov=main tests/ -s
```
## Pylint
`Pylint` is configured through `.pylintrc`. To run:
```
(tenant-base) $ pylint main.py
```

To run `pylint` on the entire project:
```
$ find . -iname "*.py" | xargs pylint
```

## Contact
Nicolas Frega
`frega.nicolas@gmail.com`
