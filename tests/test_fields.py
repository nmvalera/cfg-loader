"""
    tests.test_utils
    ~~~~~~~~~~~~~~~~

    Test fields

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see LICENSE for more details.
"""

import pytest
from cfg_loader.fields import PathValidator, Path
from marshmallow import Schema, ValidationError


def test_path_validator(config_path):
    validator = PathValidator()
    with pytest.raises(ValidationError):
        validator('invalid')
    assert validator(config_path) == config_path


def test_path_field(config_path):
    class SchemaTest(Schema):
        path_field = Path()

    data = {
        'path_field': config_path,
    }
    assert SchemaTest().load(data) == {
        'path_field': config_path,
    }
