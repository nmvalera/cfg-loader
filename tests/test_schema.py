"""
    tests.test_schema
    ~~~~~~~~~~~~~~~~~

    Test schema

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import pytest
from marshmallow import fields

from cfg_loader.exceptions import ValidationError
from cfg_loader.fields import UnwrapNested
from cfg_loader.schema import ConfigSchema


class NestedConfigSchemaTest(ConfigSchema):
    field = fields.Int()
    many = fields.List(fields.Str())


class ConfigSchemaTest(ConfigSchema):
    field = fields.Str()
    nested = fields.Nested(NestedConfigSchemaTest)


@pytest.fixture(scope='module')
def basic_config_schema_loader():
    yield ConfigSchemaTest()


@pytest.fixture(scope='module')
def interpolating_config_schema_loader():
    yield ConfigSchemaTest(substitution_mapping={'VARIABLE': 'substitution', 'VARIABLE_INT': '24'})


def _test_invalid_basic_config_schema_loading(schema_loader):
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
        schema_loader.load(invalid_raw_config)


def _test_valid_basic_config_schema_loading(schema_loader):
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
    assert schema_loader.load(valid_raw_config) == {
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


def test_basic_config_schema_loading(basic_config_schema_loader, interpolating_config_schema_loader):
    for config_loader in [basic_config_schema_loader, interpolating_config_schema_loader]:
        _test_invalid_basic_config_schema_loading(config_loader)
        _test_valid_basic_config_schema_loading(config_loader)


def test_interpolating_config_schema_loading(interpolating_config_schema_loader):
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
    assert interpolating_config_schema_loader.load(raw_config) == {
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


class UnwrapNestedConfigSchemaTest(ConfigSchema):
    nested = UnwrapNested(NestedConfigSchemaTest)


class UnwrapConfigSchemaTest(ConfigSchema):
    field = fields.Str()
    unwrap_nested = UnwrapNested(UnwrapNestedConfigSchemaTest, prefix='unwrapped_')
    regular_nested = fields.Nested(NestedConfigSchemaTest)


@pytest.fixture(scope='module')
def unwrap_config_schema_loader():
    yield UnwrapConfigSchemaTest(substitution_mapping={'VARIABLE': 'substitution', 'VARIABLE_INT': '24'})


def test_unwrap_config_schema_loading(unwrap_config_schema_loader):
    raw_config = {
        'field': 'value',
        'extra': '${VARIABLE?err}',
        'unwrap_nested': {
            'nested': {
                'field': '${VARIABLE_INT}',
                'many': [
                    '${UNSET_VARIABLE-default}',
                    'element',
                ],
            },
            'extra': [
                'element',
            ],
        },
        'regular_nested': {
            'field': 33,
            'many': [
                '${UNSET_VARIABLE-default}',
            ],
        }
    }

    assert unwrap_config_schema_loader.load(raw_config) == {
        'field': 'value',
        'extra': 'substitution',
        'unwrapped_field': 24,
        'unwrapped_many': [
            'default',
            'element',
        ],
        'unwrapped_extra': [
            'element'
        ],
        'regular_nested': {
            'field': 33,
            'many': [
                'default',
            ],
        }
    }


class NestedDataKeyConfigSchemaTest(ConfigSchema):
    nested = fields.Nested(NestedConfigSchemaTest, data_key='nested-key')


def test_nested_data_key_loading():
    schema = NestedDataKeyConfigSchemaTest()
    raw_data = {
        'nested-key': {
            'field': '4',
            'many': [],
        },
    }
    loaded_data = schema.load(raw_data)
    assert loaded_data == {
        'nested': {
            'field': 4,
            'many': [],
        },
    }


class UnwrapNestedDataKeyConfigSchemaTest(ConfigSchema):
    nested = UnwrapNested(NestedConfigSchemaTest, data_key='nested-key')


def test_unwrap_nested_data_key_loading():
    schema = UnwrapNestedDataKeyConfigSchemaTest()
    raw_data = {
        'nested-key': {
            'field': '4',
            'many': [],
        },
    }
    loaded_data = schema.load(raw_data)
    assert loaded_data == {
        'field': 4,
        'many': [],
    }
