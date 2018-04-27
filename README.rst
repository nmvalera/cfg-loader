.. image:: https://travis-ci.org/nmvalera/config-loader.svg?branch=master
    :target: https://travis-ci.org/nmvalera/config-loader#

.. image:: https://codecov.io/gh/nicolas-maurice/config-loader/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/nmvalera/config-loader

Config-Loader
=============

Config loader is a library that allows to easily load configuration settings.

Main features are

- validation and automatic processing of configuration input data (by using `marshmallow`_ schemas)
- substitution of environment variables in input data (following `docker compose variable substitution syntax`_)
- configuration loading from .yaml file

.. _`marshmallow`: https://github.com/marshmallow-code/marshmallow
.. _`docker compose variable substitution syntax`: https://docs.docker.com/compose/compose-file/#variable-substitution

Requirements
------------

- Python>=3.5


