"""
    cfg_loader.utils
    ~~~~~~~~~~~~~~~~

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


def add_prefix(dictionary, prefix):
    """Add prefix to every key in a dictionary

    :param dictionary: Original dictionary
    :type dictionary: dict
    :param prefix: Prefix to add to every key
    :type prefix: str
    """
    return {'{}{}'.format(prefix, key): value for key, value in dictionary.items()}
