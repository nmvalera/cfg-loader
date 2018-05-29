.. _api_reference:

***
API
***

.. module:: cfg_loader

This part of the documentation covers all the interfaces of Conf-Loader.

Schema
======

.. py:currentmodule:: cfg_loader.schema.base

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

.. py:currentmodule:: cfg_loader.loader

.. autoclass:: BaseConfigLoader
    :members:

.. autoclass:: YamlConfigLoader
    :members:

Interpolator
============

.. py:currentmodule:: cfg_loader.interpolator

.. autoclass:: Interpolator
    :members:

.. autoclass:: SubstitutionTemplate
    :members:

Fields
======

.. py:currentmodule:: cfg_loader.fields

.. autoclass:: Path
    :members:

.. autoclass:: UnwrapNested
    :members:

Exceptions
==========

.. py:currentmodule:: cfg_loader.exceptions

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
