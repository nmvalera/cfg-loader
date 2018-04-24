.. image:: https://travis-ci.org/nmvalera/boilerplate-package.svg?branch=master
    :target: https://travis-ci.org/nmvalera/boilerplate-package#

.. image:: https://codecov.io/gh/nicolas-maurice/boilerplate-package/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/nmvalera/boilerplate-package

Boilerplate Python
==================

This project is a Python boilerplate and is meant to be forked when creating a new Python project.

This project is structured as respecting common Python project conventions and gathers scripts to make DevOps straightforward including

- creating development environment
- testing
- building docs
- CI/CD scripts
- etc.

Requirements
------------

Distribution
~~~~~~~~~~~~

It is highly recommended to use this project on Unix distribution.

Git
~~~

Having the latest version of ``git`` installed locally.

Docker
~~~~~~

Having ``docker`` and ``docker-compose`` installed locally.

Python
~~~~~~

Having Python 3.5 and 3.6 installed locally.

It is also recommended having ``virtualenv`` installed locally.

How to create a new Python project from this boilerplate ?
----------------------------------------------------------

Create the GitHub repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fork Boilerplate-Package
```````````````````````

Fork Boilerplate-Package project.

Manage project settings
```````````````````````

Go to the forked project settings and

#. "Rename repository" as you like (assuming here you renamed it ``new-project-name``) being careful to rename Project Name and Path the same
#. "Remove fork"

Setup the project locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Clone the project
`````````````````

.. code-block:: sh

    $ git clone git@github.com:<group>/new-project-name.git
    $ cd new-project-name

Add a remote for later update
`````````````````````````````

.. code-block:: sh

    $ git remote add boilerplate git@gitlab.com:ConsenSys-Fr/boilerplates/boilerplate-package.git
    $ git fetch boilerplate

Rename the project
``````````````````

They are multiple scripts in the project that reference boilerplate-package, thus these scripts should be updated
to be consistent with your project's name.

When modifying name you should be careful to always respect the case sensitivity.

- Boilerplate-Package -> New-Project-Name
- boilerplate_package -> new_project_name
- boilerplate-package -> new-project-name

Update README.rst
`````````````````

Once all previous steps completed you can erase this README.rst script content and start it over with the description of your new project.

You can also update the project description parameter in the ``setup.py`` script.

For any further question you can refer to CONTRIBUTING.rst.