"""
    Cfg-Loader
    ~~~~~~~~~~

    Config-Loader is an empty Python project.

    It is meant to be forked when starting a new Python project to inherit structure.

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import os
import re

from setuptools import setup, find_packages


def read(file_name):
    try:
        return open(os.path.join(os.path.dirname(__file__), file_name)).read()
    except FileNotFoundError:
        return ''


def find_version(file):
    """Attempts to find the version number in a file.

    Raises RuntimeError if not found.

    :param file: File where to find version
    :type file: str
    """
    version = ''
    with open(file, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version


setup(
    name='Cfg-Loader',
    version=find_version('cfg_loader/__init__.py'),
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
            'sphinx_rtd_theme',
        ],
        'doc': [
            'sphinx',
            'sphinx_rtd_theme',
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
