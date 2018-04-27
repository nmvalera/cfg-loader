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
BASE_CONFIG_PATH = os.path.join(CONFIG_DIR, 'config.yml')


def set_env_vars(env_vars_to_set):
    """Set environment variable to a value and returns a function to reset environment variables to their old value

    :param env_vars_to_set: List of tuples `(var, new_value)` of environment variables to set
    :type env_vars_to_set: list

    Example:
    >>> import os
    >>> os.environ['VARIABLE'] = 'value'
    >>> reset_env_vars = set_env_vars([('VARIABLE', 'new_value')])
    >>> os.environ['VARIABLE']
    'new_value'
    >>> reset_env_vars()
    >>> os.environ['VARIABLE']
    'value'
    """

    vars = [(var[0], var[1], os.environ.get(var[0])) for var in env_vars_to_set]

    # Set environment variables
    for var, new_value, old_value in vars:
        if new_value is None and old_value is not None:
            del os.environ[var]
        elif new_value is not None:
            os.environ[var] = new_value

    def reset_env_vars():
        set_env_vars([(var[0], var[2]) for var in vars])

    return reset_env_vars


@pytest.fixture
def env_vars():
    yield []


@pytest.fixture
def config_path(env_vars):
    reset_env_vars = set_env_vars(env_vars)

    yield BASE_CONFIG_PATH

    reset_env_vars()
