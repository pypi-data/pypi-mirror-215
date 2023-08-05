#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from os import path

requirements = [
    'zcache'
]
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name='kolak',
    version='0.1.5',
    packages=['kolak',],
    license='MIT',
    author="guangrei",
    author_email="myawn@pm.me",
    description="universal rss parser",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords="rss feed parser podcast xml",
    url="https://gitlab.com/guangrei/Kolak",
    install_requires=requirements,

)
