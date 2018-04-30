.. _api_reference:

***
API
***

.. module:: config_loader

This part of the documentation covers all the interfaces of Config-Loader.

Schema
======

.. py:currentmodule:: config_loader.schema.base

.. autoclass:: InterpolatingSchema
    :members:

.. autoclass:: ExtraFieldsSchema
    :members:

.. autoclass:: UnwrapNestedSchema
    :members:

.. autoclass:: ConfigSchema
    :members:

Loader
======

.. py:currentmodule:: config_loader.loader

.. autoclass:: BaseConfigLoader
    :members:

.. autoclass:: YamlConfigLoader
    :members:

Interpolator
============

.. py:currentmodule:: config_loader.interpolator

.. autoclass:: Interpolator
    :members:

.. autoclass:: SubstitutionTemplate
    :members:

Fields
======

.. py:currentmodule:: config_loader.fields

.. autoclass:: Path
    :members:

.. autoclass:: UnwrapNested
    :members:

Exceptions
==========

.. py:currentmodule:: config_loader.exceptions

.. autoclass:: ConfigLoaderError
    :show-inheritance:

.. autoclass:: ConfigFileMissingError
    :show-inheritance:

.. autoclass:: ConfigFileNotFoundError
    :show-inheritance:

.. autoclass:: LoadingError
    :show-inheritance:

.. autoclass:: ValidationError
    :show-inheritance:

.. autoclass:: UnsetRequiredSubstitution
    :show-inheritance:

.. autoclass:: InvalidSubstitution
    :show-inheritance:
