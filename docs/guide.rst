About Cfg-Loader
================

Cfg-loader is a library that allows to easily setup a configuration loader that makes
no assumption on the python framework you are using.
It uses `marshmallow`_ to deserialize input data into a desired formatted configuration.
It gives you full freedom to configure your own configuration schema.

Main features
~~~~~~~~~~~~~

- input data validation and automatic processing using `marshmallow`_
- substitution of environment variables in input data (following `docker compose variable substitution syntax`_)
- configuration loading from .yaml file

.. _`marshmallow`: https://github.com/marshmallow-code/marshmallow
.. _`docker compose variable substitution syntax`: https://docs.docker.com/compose/compose-file/#variable-substitution

Quickstart
==========

This page gives a good introduction to Cfg-Loader. If not yet install please refer to the Installation section.

Cfg-Loader is built upon `marshmallow`_ for deserializing data.
It is recommended that you have some light knowledge of `marshmallow`_ before you try
to setup you own configuration loader.

A minimal configuration loader
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Declaring a configuration loader
````````````````````````````````

.. code-block:: python

    >>> from cfg_loader import ConfigSchema, BaseConfigLoader
    >>> from marshmallow import fields

    >>> class MyConfigSchema(ConfigSchema):
    ...     setting1 = fields.Str()
    ...     setting2 = fields.Int(required=True)
    ...     setting3 = fields.Float(missing=13.2)

    >>> my_config_loader = BaseConfigLoader(MyConfigSchema)

What did we do?

#. We imported the :class:`~cfg_loader.ConfigSchema` class, which is an enhanced version
   of the `marshmallow`_ base :class:`~marshmallow.Schema` class.
   :class:`~cfg_loader.ConfigSchema` is 100% compatible with :class:`~marshmallow.Schema`
#. We imported :class:`~cfg_loader.BaseConfigLoader` class which is
   the main class for instantiating a configuration loader
#. We imported useful marshmallow resources to declare the configuration schema.
#. We declared a configuration schema that inherits from :class:`~cfg_loader.ConfigSchema`.
   This schema describes what the configuration should look like.
#. We declared a configuration loader

Loading configuration
`````````````````````

Once a configuration loader has been declared it is possible to load configuration from objects
that can be deserialized with the declared schema

.. code-block:: python

    >>> config = my_config_loader.load({
    ...    'setting1': 'value',
    ...    'setting2': '4',
    ... })

    >>> config == {
    ...     'setting1': 'value',
    ...     'setting2': 4,
    ...     'setting3': 13.2,
    ... }
    True

Note that ``setting3`` field has been automatically fulfilled in the configuration result
because the field has been declared with a ``missing`` argument.

The same way trying to load a configuration with a required field missing is not possible

.. code-block:: python

    >>> config = my_config_loader.load({
    ...    'setting1': 'value',
    ... })
    Traceback (most recent call last):
    ...
    cfg_loader.exceptions.ValidationError: {'setting2': ['Missing data for required field.']}


Specific features
=================

Class :class:`~cfg_loader.ConfigSchema` implements some specific features to make your life easier
when loading a configuration from data.

Environment variables substitution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When loading a configuration you may like to retrieve some external information that is not
directly available in your input data (typically environment variables values).
Cfg-Loader allows to include placeholders in the input data that are automatically substituted
with data from an external mapping at configuration loading.
Cfg-Loader follows the same placeholder convention as `docker compose variable substitution syntax`_.

Example
```````

.. code-block:: python

    >>> substitution_mapping = {'VARIABLE': 'substitution'}
    >>> my_config_loader = BaseConfigLoader(MyConfigSchema,
    ...                                     substitution_mapping)

    >>> config = my_config_loader.load({
    ...    'setting1': '${VARIABLE}',
    ...    'setting2': '${UNSET_VARIABLE:-1}',
    ... })

    >>> config == {
    ...     'setting1': 'substitution',
    ...     'setting2': 1,
    ...     'setting3': 13.2,
    ... }
    True

Substitution Syntax
```````````````````

.. list-table::
    :widths: 35 65
    :header-rows: 1

    * - Syntax
      - Behavior

    * - ``$VARIABLE`` or ``${VARIABLE}``
      - Evaluates to ``VARIABLE`` value in the substitution mapping

    * - ``${VARIABLE:-default}``
      - Evaluates to default if ``VARIABLE`` is unset or empty in the substitution mapping

    * - ``${VARIABLE-default}``
      - Evaluates to default only if ``VARIABLE`` is unset in the substitution mapping

    * - ``${VARIABLE:?err}``
      - Exits with an error message containing ``err`` if ``VARIABLE`` is unset or empty in the substitution mapping.

    * - ``${VARIABLE?err}``
      - Exits with an error message containing ``err`` if ``VARIABLE`` is unset in the substitution mapping.

Substitution with shell environment variables
`````````````````````````````````````````````

Typically one can choose to use ``os.environ`` as the substitution mapping so placeholders
will be replaced with environment variables as set in the current shell.

.. code-block:: python

    >>> import os

    >>> my_config_loader = BaseConfigLoader(MyConfigSchema, os.environ)

Loading configuration from .yaml file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cfg-Loader enables you to load configuration from .yaml file

Example
```````

tests/config/config.yml
#######################

.. literalinclude:: ../tests/config/config.yml
    :language: YAML
    :name: tests/config/config.yml

Loading configuration
#####################

.. code-block:: python

    >>> from cfg_loader import YamlConfigLoader

    >>> class BaseConfigSchema(ConfigSchema):
    ...     name = fields.Str()
    ...     path = fields.Str()

    >>> class SecurityConfigSchema(ConfigSchema):
    ...     secret = fields.Str()

    >>> class MyConfigSchema(ConfigSchema):
    ...     base = fields.Nested(BaseConfigSchema)
    ...     security = fields.Nested(SecurityConfigSchema)

    >>> substitution_mapping = {'PATH': 'folder/file', 'SECRET': 'my-secret'}
    >>> my_config_loader = YamlConfigLoader(MyConfigSchema,
    ...                                     substitution_mapping)

    >>> config = my_config_loader.load('tests/config/config.yml')

    >>> config == {
    ...     'base': {
    ...         'name': 'App-Name',
    ...         'path': '/home/user/folder/file',
    ...     },
    ...     'security': {
    ...         'secret': 'my-secret',
    ...     },
    ... }
    True

Non-declared fields are preserved
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If a field has been omitted when declaring a schema but this field is provided in the input data
then the field will be preserved in the output configuration. No validation is performed on such
a field at deserialization.

Example
```````

.. code-block:: python

    >>> class MyConfigSchema(ConfigSchema):
    ...     setting1 = fields.Str()

    >>> my_config_loader = BaseConfigLoader(MyConfigSchema)

    >>> config = my_config_loader.load({
    ...    'setting1': 'value',
    ...    'extra': 'extra_value',
    ... })

    >>> config == {
    ...     'setting1': 'value',
    ...     'extra': 'extra_value',
    ... }
    True

Nested fields can be automatically unwrapped
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is sometimes useful to have a configuration schema with nested fields for better readability
but you do not want your resulted configuration to have nested information.
This is typically the case when you want to declare configuration by grouping settings belonging
to a common family but in the end you want your configuration to have all the fields at the same
level. The :class:`~cfg_loader.fields.UnwrapNested` field class is there for this purpose.

Example
```````
.. code-block:: python

    >>> from cfg_loader.fields import UnwrapNested

    >>> class MyNestedConfigSchema(ConfigSchema):
    ...     setting1 = fields.Str()
    ...     setting2 = fields.Int()

    >>> class MyConfigSchema(ConfigSchema):
    ...     regular_nested = fields.Nested(MyNestedConfigSchema)
    ...     unwrap_nested = UnwrapNested(MyNestedConfigSchema,
    ...                                  prefix='my_prefix_')

    >>> my_config_loader = BaseConfigLoader(MyConfigSchema)

    >>> config = my_config_loader.load({
    ...     'regular_nested': {
    ...         'setting1': 'regular_value',
    ...         'setting2': '5',
    ...     },
    ...     'unwrap_nested': {
    ...         'setting1': 'unwrap_value',
    ...         'setting2': '4',
    ...     },
    ... })

    >>> config == {
    ...     'regular_nested': {
    ...         'setting1': 'regular_value',
    ...         'setting2': 5,
    ...     },
    ...     'my_prefix_setting1': 'unwrap_value',
    ...     'my_prefix_setting2': 4,
    ... }
    True

The :class:`~cfg_loader.fields.UnwrapNested` inherits from :class:`~marshmallow.fields.Nested` and
can be parametrized as such.