"""
    tests.test_schema
    ~~~~~~~~~~~~~~~~~

    Test schema

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import pytest
from config_loader.schema import ConfigSchema
from marshmallow import fields
from marshmallow.exceptions import ValidationError


class NestedConfigSchema(ConfigSchema):
    field = fields.Int()
    many = fields.List(fields.Str())


class ConfigSchemaTest(ConfigSchema):
    field = fields.Str()
    nested = fields.Nested(NestedConfigSchema)


@pytest.fixture(scope='module')
def basic_config_loader():
    yield ConfigSchemaTest()


@pytest.fixture(scope='module')
def interpolating_config_loader():
    yield ConfigSchemaTest(substitution_mapping={'VARIABLE': 'substitution', 'VARIABLE_INT': '24'})


def _test_invalid_basic_config_loading(config_loader):
    invalid_raw_config = {
        'field': 2,
        'extra': 'extra_value',
        'nested': {
            'field': 4,
            'many': [
                'element',
            ],
        }
    }
    with pytest.raises(ValidationError):
        config_loader.load(invalid_raw_config)


def _test_valid_basic_config_loading(config_loader):
    valid_raw_config = {
        'field': 'value',
        'extra': 'extra_value',
        'nested': {
            'field': '4',
            'many': [
                'element',
            ],
            'extra': {
                'key': 2,
                'many': [
                    'element',
                ],
            }
        }
    }
    assert config_loader.load(valid_raw_config) == {
        'field': 'value',
        'extra': 'extra_value',
        'nested': {
            'field': 4,
            'many': [
                'element',
            ],
            'extra': {
                'key': 2,
                'many': [
                    'element',
                ],
            },
        },
    }


def test_basic_config_loading(basic_config_loader, interpolating_config_loader):
    for config_loader in [basic_config_loader, interpolating_config_loader]:
        _test_invalid_basic_config_loading(config_loader)
        _test_valid_basic_config_loading(config_loader)


def test_interpolating_config_loading(interpolating_config_loader):
    raw_config = {
        'field': 'value',
        'extra': '${VARIABLE?err}',
        'nested': {
            'field': '${VARIABLE_INT}',
            'many': [
                '${UNSET_VARIABLE-default}',
                'element',
            ],
            'extra': [
                'element',
                {
                    'key': 'value',
                }
            ]
        },
    }

    assert interpolating_config_loader.load(raw_config) == {
        'field': 'value',
        'extra': 'substitution',
        'nested': {
            'field': 24,
            'many': [
                'default',
                'element',
            ],
            'extra': [
                'element',
                {
                    'key': 'value',
                },
            ],
        },
    }
