"""
    cfg_loader
    ~~~~~~~~~~

    A library to load configuration

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

from .loader import BaseConfigLoader, YamlConfigLoader
from .schema import ConfigSchema

__version__ = '0.1.1'

__all__ = [
    'ConfigSchema',
    'BaseConfigLoader',
    'YamlConfigLoader',
]
