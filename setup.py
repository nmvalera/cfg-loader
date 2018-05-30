"""
    Cfg-Loader
    ~~~~~~~~~~

    Config-Loader is an empty Python project.

    It is meant to be forked when starting a new Python project to inherit structure.

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import os

from setuptools import setup, find_packages


def read(file_name):
    try:
        return open(os.path.join(os.path.dirname(__file__), file_name)).read()
    except FileNotFoundError:
        return ''


setup(
    name='Cfg-Loader',
    version='0.1.1',
    license=read('LICENSE'),
    url='https://github.com/nmvalera/cfg-loader',
    author='Nicolas Maurice',
    author_email='nicolas.maurice.valera@gmail.com',
    maintainer='ConsenSys France',
    description='A library that allows to easily load configuration settings.',
    long_description=read('README.rst'),
    packages=find_packages(),
    install_requires=[
        'marshmallow==3.0.0b11',
        'PyYAML>=3.12',
    ],
    extras_require={
        'dev': [
            'flake8',
            'autoflake',
            'autopep8',
            'coverage',
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
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests'
)
