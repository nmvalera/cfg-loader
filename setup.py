"""
    Config-Loader
    ~~~~~~~~~~~~~

    Config-Loader is an empty Python project.

    It is meant to be forked when starting a new Python project to inherit structure.

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import os

from setuptools import setup


def read(file_name):
    try:
        return open(os.path.join(os.path.dirname(__file__), file_name)).read()
    except FileNotFoundError:
        return ''


setup(
    name='Config-Loader',
    version='0.0.0',
    license=read('LICENSE'),
    url='https://gitlab.com/ConsenSys-Fr/sandbox/config-loader',
    author='ConsenSys France',
    description='Config-Loader is an empty Python project',
    packages=['config_loader'],
    install_requires=[
    ],
    extras_require={
        'dev': [
            'autoflake',
            'autopep8',
            'coverage',
            'flake8',
            'pytest>=3',
            'tox',
            'sphinx',
        ],
        'doc': [
            'sphinx',
        ],
    },
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests'
)
