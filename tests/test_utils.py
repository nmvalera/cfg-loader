"""
    tests.test_utils
    ~~~~~~~~~~~~~~~~

    Test utility functions

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import pytest

from config_loader.utils import parse_yaml, parse_yaml_file


def test_parse_yaml():
    assert parse_yaml("""
    section:
      subsection:
        - one
        - two
    """) is not None


def test_parse_yaml_file(config_path):
    with pytest.raises(TypeError):
        parse_yaml_file(None)

    with pytest.raises(FileNotFoundError):
        parse_yaml_file('unknown')

    assert parse_yaml_file(config_path)
