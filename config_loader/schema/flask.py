"""
    config_loader.schema.base
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Implement base marshmallow schema to deserialize configuration data

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

from marshmallow import post_load

from .base import ConfigSchema
from ..utils import unwrap_dict


class FlaskConfigSchema(ConfigSchema):
    """Base config schema to load flask app configuration

    Flask configurations are flat dictionaries
    """

    @post_load
    def unwrap_nested_fields(self, data):
        print(self.__class__, "Unwrap", data)
        return unwrap_dict(data)
