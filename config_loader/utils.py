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


def unwrap_dict(dictionary):
    """Unwrap nested sub dictionaries from a dictionary

    Example:
    >>> dictionary = {'1.0': 'v', '1.1': {'1.1.0': 'v'}, '1.2': {'1.2.0': 'v', '1.2.1': {'1.2.1.0': 'v'}}}
    >>> unwrap_dict(dictionary)
    {'1.0': 'v', '1.1.0': 'v', '1.2.0': 'v', '1.2.1.0': 'v'}

    When a key is found both in the main dictionary and in a nested dictionary then the nested value is kept
    >>> dictionary ={'key': 'value', 'nested': {'key': 'value_nested'}}
    >>> unwrap_dict(dictionary) == {'key': 'value_nested'}
    True

    :param dictionary: dictionary to unwrap
    :type dictionary: dict
    """

    unwrapped_dict, nested_dict = {}, {}

    for key, value in dictionary.items():
        if isinstance(value, dict):
            nested_dict.update(unwrap_dict(value))
        else:
            unwrapped_dict[key] = value

    unwrapped_dict.update(nested_dict)

    return unwrapped_dict
