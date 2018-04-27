"""
    tests.conftest
    ~~~~~~~~~~~~~~

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import os

import pytest

TEST_DIR = os.path.dirname(__file__)
CONFIG_DIR = os.path.join(TEST_DIR, 'config')


@pytest.fixture(scope='session')
def config_path():
    yield os.path.join(CONFIG_DIR, 'config.yml')
