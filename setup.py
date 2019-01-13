# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='tenant-base',
    version='0.1.0',
    description='simple memcahed and sqlite3 server',
    long_description=readme,
    author='Nicolas Frega',
    author_email='frega.nicolas@gmail.com',
    url='https://github.com/NFhbar/tenant-base',
    license=license,
    packages=find_packages(exclude=('tests', '.circleci'))
)
