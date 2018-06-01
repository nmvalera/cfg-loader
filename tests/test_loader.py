"""
    tests.test_loader
    ~~~~~~~~~~~~~~~~~

    Test configuration loader

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

import pytest
from marshmallow import fields

from cfg_loader.exceptions import ConfigFileMissingError, ConfigFileNotFoundError
from cfg_loader.loader import BaseConfigLoader, YamlConfigLoader
from cfg_loader.schema import ConfigSchema
from .conftest import BASE_CONFIG_PATH


class BaseConfigSchema(ConfigSchema):
    name = fields.Str()
    path = fields.Str()


class SecurityConfigSchema(ConfigSchema):
    secret = fields.Str()


class ConfigSchemaTest(ConfigSchema):
    base = fields.Nested(BaseConfigSchema)
    security = fields.Nested(SecurityConfigSchema)


def test_base_config_loader():
    config_loader = BaseConfigLoader(ConfigSchemaTest)
    assert config_loader.load({
        'base': {
            'name': 'App-Name',
            'path': '/home/folder',
        },
        'security': {
            'secret': 'my-secret',
        },
    }) == {
        'base': {
            'name': 'App-Name',
            'path': '/home/folder',
        },
        'security': {
            'secret': 'my-secret',
        },
    }


def test_yaml_config_loader(config_path):
    config_loader = YamlConfigLoader(ConfigSchemaTest,
                                     substitution_mapping={'PATH': 'folder/file', 'SECRET': 'my-secret'})

    assert config_loader.load(config_path) == {
        'base': {
            'name': 'App-Name',
            'path': '/home/user/folder/file',
        },
        'security': {
            'secret': 'my-secret',
        },
    }


@pytest.mark.parametrize('env_vars', [[('VARIABLE', BASE_CONFIG_PATH)]])
def test_yaml_config_loader_from_env_var(config_path):
    config_loader = YamlConfigLoader(ConfigSchemaTest,
                                     substitution_mapping={'PATH': 'folder/file', 'SECRET': 'my-secret'},
                                     config_file_env_var='VARIABLE')

    assert config_loader.load() == {
        'base': {
            'name': 'App-Name',
            'path': '/home/user/folder/file',
        },
        'security': {
            'secret': 'my-secret',
        },
    }


@pytest.mark.parametrize('env_vars', [[('VARIABLE', None)]])
def test_yaml_config_loader_no_path(config_path):
    config_loader = YamlConfigLoader(ConfigSchemaTest,
                                     substitution_mapping={'PATH': 'folder/file', 'SECRET': 'my-secret'},
                                     config_file_env_var='VARIABLE')

    with pytest.raises(ConfigFileMissingError) as e:
        config_loader.load()
    assert 'VARIABLE' in str(e.value)


@pytest.mark.parametrize('env_vars', [[('VARIABLE', None)]])
def test_yaml_config_loader_with_default_path(config_path):
    config_loader = YamlConfigLoader(ConfigSchemaTest,
                                     substitution_mapping={'PATH': 'folder/file', 'SECRET': 'my-secret'},
                                     config_file_env_var='VARIABLE',
                                     default_config_path=BASE_CONFIG_PATH)

    assert config_loader.load() == {
        'base': {
            'name': 'App-Name',
            'path': '/home/user/folder/file',
        },
        'security': {
            'secret': 'my-secret',
        },
    }


def test_yaml_config_loader_invalid_path():
    config_loader = YamlConfigLoader(ConfigSchemaTest,
                                     substitution_mapping={'PATH': 'folder/file', 'SECRET': 'my-secret'}, )

    with pytest.raises(ConfigFileNotFoundError) as e:
        config_loader.load('unknown/config/file')
    assert 'unknown/config/file' in str(e.value)
