#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name='mimisc',
    version='unknown',
    description='miscellaneous migen utilities',
    author='Jannis Harder',
    author_email='jix@jixco.de',
    license='BSD',
    packages=find_packages(),
    install_requires=['migen'],
)
