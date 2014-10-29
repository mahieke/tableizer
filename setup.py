#!/usr/bin/env python

from setuptools import setup, find_packages  # Always prefer setuptools over distutils

name = "tableizer"


def get_version(relpath="__init__.py"):
    """read version info from file without importing it"""
    from os.path import dirname, join

    for line in open(join(dirname(__file__), name, relpath)):
        if '__version__' in line:
            if '"' in line:
                return line.split('"')[1]
            elif "'" in line:
                return line.split("'")[1]


setup(
    name=name,
    description='A small tool to create simple ascii tables',
    version=get_version(),
    author='Manuel Hieke',
    author_email='mahieke90@gmail.com',
    packages=find_packages(),
    keywords='ascii, table',
    install_requires=[
    ],
    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python :: 2',
        'Topic :: Utilities',
    ],
)


