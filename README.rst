.. image:: https://travis-ci.org/nmvalera/cfg-loader.svg?branch=master
    :target: https://travis-ci.org/nmvalera/cfg-loader#

.. image:: https://codecov.io/gh/nicolas-maurice/cfg-loader/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/nmvalera/cfg-loader

Cfg-Loader
==========

Cfg-Loader is a library that allows to easily load configuration settings.
It uses `marshmallow`_ to deserialize input data into a target format configuration data.

Main features
~~~~~~~~~~~~~

- input data validation and automatic processing using `marshmallow`_
- substitution of environment variables in input data (following `docker compose variable substitution syntax`_)
- configuration loading from .yaml file

.. _`marshmallow`: https://github.com/marshmallow-code/marshmallow
.. _`docker compose variable substitution syntax`: https://docs.docker.com/compose/compose-file/#variable-substitution

Requirements
------------

- Python>=3.5

A simple example
----------------

.. code-block:: python

    >>> from cfg_loader import ConfigSchema, BaseConfigLoader
    >>> from marshmallow import fields

    # Declare your configuration schema
    >>> class MyConfigSchema(ConfigSchema):
    ...     setting1 = fields.Str()
    ...     setting2 = fields.Int(required=True)
    ...     setting3 = fields.Float(missing=13.2)

    # Declare mapping to substitute environment variable
    >>> substitution_mapping = {'FILE_PATH': 'file'}

    # Initialize config loader
    >>> my_config_loader = BaseConfigLoader(MyConfigSchema, substitution_mapping=substitution_mapping)

    # Load configuration
    >>> config = my_config_loader.load({'setting1': '/home/folder/${FILE_PATH?:file path required}', 'setting2': '4'})
    >>> config == {'setting1': '/home/folder/file', 'setting2': 4, 'setting3': 13.2}
    True

    # Invalid input data
    >>> my_config_loader.load({'setting1': '/home/folder/${FILE_PATH?:file path required}', 'setting3': 13.4})
    Traceback (most recent call last):
    ...
    cfg_loader.exceptions.ValidationError: {'setting2': ['Missing data for required field.']}

    >>> my_config_loader.load({'setting2': 12, 'setting3': 'string'})
    Traceback (most recent call last):
    ...
    cfg_loader.exceptions.ValidationError: {'setting3': ['Not a valid number.']}

    # Variable substitution invalid
    >>> my_config_loader.load({'setting2': '${UNSET_VARIABLE?Variable "UNSET_VARIABLE" required}'})
    Traceback (most recent call last):
    ...
    cfg_loader.exceptions.UnsetRequiredSubstitution: Variable "UNSET_VARIABLE" required
