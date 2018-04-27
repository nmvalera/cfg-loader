"""
    config_loader.schema
    ~~~~~~~~~~~~~~~~~~~~

    Implement marshmallow schema loading

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

from .base import ConfigSchema
from .flask import FlaskConfigSchema

__all__ = [
    'ConfigSchema',
    'FlaskConfigSchema',
]
