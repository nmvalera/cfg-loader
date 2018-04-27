"""
    config_loader.utils
    ~~~~~~~~~~~~~~~~~~~

    Implement utilities functions

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

import yaml


def parse_yaml(content):
    return yaml.safe_load(content)


def parse_yaml_file(path):
    with open(path, 'rt') as f:
        return parse_yaml(f.read())
