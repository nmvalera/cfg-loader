.. image:: https://gitlab.com/nicolas.maurice.valera/boilerplate-python/badges/master/pipeline.svg
    :target: https://gitlab.com/nicolas.maurice.valera/boilerplate-python/commits/master

.. image:: https://gitlab.com/nicolas.maurice.valera/boilerplate-python/badges/master/coverage.svg
    :target: https://gitlab.com/nicolas.maurice.valera/boilerplate-python/commits/master

Boilerplate Python
==================

This project is a Python boilerplate and is meant to be forked each time someone needs to create a new Python project.

This boilerplate is structured as every Python project should be and gathers resources to make DevOps straightforward including

- creating development environment
- testing
- building docs
- CI/CD scripts
- etc.

Requirements
------------

Distribution
~~~~~~~~~~~~

This boilerplate has been developed under on linux Ubuntu 16.04.
It is highly recommended to use it on Unix system since some functions could be .

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

Create the GitLab repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fork Boilerplate-Python
```````````````````````

On GitLab fork Boilerplate-Python project by clicking the `Fork`_ button

.. _Fork: https://gitlab.com/nicolas.maurice.valera/boilerplate-python/forks/new

Manage project settings
```````````````````````

On GitLab go to the forked project "General>Advanced Settings" and

#. "Rename repository" as you like (assuming here you renamed it ``new-package-name``) being careful to rename Project Name and Path the same
#. "Remove fork"

Setup the project locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Clone the project
`````````````````

.. code-block:: sh

    $ git clone git@git.lab-apps.fr:<group>/new-package-name.git
    $ cd new-package-name

Add a remote for later update
`````````````````````````````

.. code-block:: sh

    $ git remote add boilerplate git@gitlab.com:nicolas.maurice.valera/boilerplate-python.git
    $ git fetch boilerplate

Rename the project
``````````````````

They are multiple scripts in the project that reference boilerplate-python, thus these scripts should be updated
to be consistent with your package's name.

When modifying name you should be careful to always respect the case sensitivity.

- Boilerplate-Python -> New-Package-Name
- boilerplate_python -> new_package_name
- boilerplate-python -> new-package-name

Update README.rst
`````````````````

Once all previous steps completed you can erase this README.rst script content and start it over with the description of your new project.

You can also update the package description parameter in the ``setup.py`` script.

For any further question you can refer to CONTRIBUTING.rst.