"""
    tests.test_loader
    ~~~~~~~~~~~~~~~~~

    Test configuration loader

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""
import pytest
from config_loader.exceptions import ConfigFileMissingError, ConfigFileNotFoundError
from config_loader.loader import BaseConfigLoader, YamlBaseConfigLoader
from config_loader.schema import ConfigSchema
from marshmallow import fields

from .conftest import BASE_CONFIG_PATH


class ConfigSchemaTest(ConfigSchema):
    setting = fields.Str()


def test_base_config_loader():
    config_loader = BaseConfigLoader(ConfigSchemaTest)
    assert config_loader.load({'setting': 'value'}) == {'setting': 'value'}


def test_yaml_config_loader(config_path):
    config_loader = YamlBaseConfigLoader(ConfigSchemaTest)

    assert config_loader.load(config_path) == {'setting': 'setting_value'}


@pytest.mark.parametrize('env_vars', [[('VARIABLE', BASE_CONFIG_PATH)]])
def test_yaml_config_loader_from_env_var(config_path):
    config_loader = YamlBaseConfigLoader(ConfigSchemaTest, config_file_env_var='VARIABLE')

    assert config_loader.load() == {'setting': 'setting_value'}


@pytest.mark.parametrize('env_vars', [[('VARIABLE', None)]])
def test_yaml_config_loader_no_path(config_path):
    config_loader = YamlBaseConfigLoader(ConfigSchemaTest, config_file_env_var='VARIABLE')

    with pytest.raises(ConfigFileMissingError) as e:
        config_loader.load()
    assert 'VARIABLE' in str(e.value)


def test_yaml_config_loader_invalid_path():
    config_loader = YamlBaseConfigLoader(ConfigSchemaTest)

    with pytest.raises(ConfigFileNotFoundError) as e:
        config_loader.load('unknown/config/file')
    assert 'unknown/config/file' in str(e.value)
