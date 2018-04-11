Django GraphQL Persist
======================

|Pypi| |Wheel| |Build Status| |Codecov| |Code Climate|


**Persisted queries** for `Django GraphQL`_

.. _Django GraphQL: https://github.com/graphql-python/graphene-django


Dependencies
------------

* Django ≥ 1.11
* Python ≥ 3.4


Installation
------------

Install last stable version from Pypi.

.. code:: sh

    pip install django-graphql-persist


Include the ``PersistMiddleware`` middleware in your *MIDDLEWARE* settings:

.. code:: python

    MIDDLEWARE = [
        ...
        'graphql_persist.middleware.PersistMiddleware',
        ...
    ]


Loaders
-------

*Django-graphql-persist* searches for documents directories in a number of places, depending on your ``DEFAULT_LOADER_CLASSES`` variable.

* **AppDirectoriesLoader**

Loads documents from Django apps on the filesystem. For each app in ``INSTALLED_APPS``, the loader looks for a ``documents/`` subdirectory defined by ``APP_DOCUMENT_DIR`` variable.

* **FilesystemLoader**

Loads documents from the filesystem, according to ``DOCUMENTS_DIRS`` variable.

* **URLLoader**

Loads documents from urls, according to ``DOCUMENTS_DIRS``.


.. code:: python

    GRAPHQL_PERSIST = {
        'DOCUMENTS_DIRS': [
            '/app/documents',  # FilesystemLoader
            'https:// ... /documents',  # URLLoader
        ],
    }


A. Schema definition
--------------------

You can split schemas into separate files...

``/app/documents/fragments.graphql``

.. code:: graphql

    fragment userFields on UserType {
      id
      email
    }

and define Pythonic imports prefixed with ``#``.

``/app/documents/schema.graphql``

.. code:: graphql

    # from fragments import userFields

    query GetViewer {
      viewer {
        ...userFields
      }
    }

    query GetUsers {
      users {
        ...userFields
      }
    }


**Query by** ``id``

.. code:: json

    {
      "id": "schema",
      "operationName": "GetViewer",
      "variables": {}
    }


B. Operations definition
------------------------

``/app/documents/GetViewer.graphql``

.. code:: graphql

    # from fragments import userFields

    query GetViewer {
      viewer {
        ...userFields
      }
    }


**Query by** ``operationName``

.. code:: json

    {
      "operationName": "GetViewer",
      "variables": {}
    }


✋ Versioning
-------------

The versioning scheme is defined by the ``DEFAULT_VERSIONING_CLASS`` setting variable.

.. code:: python

    GRAPHQL_PERSIST = {
        'DEFAULT_VERSIONING_CLASS': 'graphql_persist.versioning.AcceptHeaderVersioning'
    }

This is the full **list of versioning classes**.

+--------------------------+-------------------------------------+
| DEFAULT_VERSIONING_CLASS |               Example               |
+==========================+=====================================+
|  AcceptHeaderVersioning  |  ``application/json; version=v1``   |
+--------------------------+-------------------------------------+
|   VendorTreeVersioning   | ``application/vnd.flavors.v1+json`` |
+--------------------------+-------------------------------------+
| QueryParameterVersioning |          ``?version=v1``            |
+--------------------------+-------------------------------------+
|    HostNameVersioning    |         ``v1.flavors.com``          |
+--------------------------+-------------------------------------+

Configure the versioning scheme and storage the GraphQL documents according to the version.

👇 **Example**

.. code::

    POST /graphql HTTP/1.1
    Accept: application/json; version=v1.full

    {
      "operationName": "GetViewer",
      "variables": {}
    }

.. code::

    documents/
    |
    ├── v1/
    │   ├── full/
    │   |     └── GetViewer.graphql 👈
    │   └── basic/
    |   |     └── GetViewer.graphql
    |   └── fragments/
    |         └── users.graphql
    └── v2/
        └── full/
        └── basic/

👉 ``/app/documents/v1/full/GetViewer.graphql``

.. code:: graphql

    # from ..fragments.users import userFields

    query GetViewer {
      viewer {
        ...userFields
      }
    }


Settings
--------

Here's a **list of settings** available in *Django-graphql-persist* and their default values.

**DOCUMENTS_DIRS**

::

    List of directories or urls searched for GraphQL SDL definitions
    Default: () 

**CACHE_NAME**

::

    Cache key name `CACHES[name]` to cache the queries results
    Default: 'default'

**QUERY_KEY_HANDLER**

::

    A custom function `f(query_id, request)` to generate the persisted query keys
    Default: 'graphql_persist.query.query_key_handler'


**DEFAULT_VERSIONING_CLASS**

::

    A versioning class to determine the `request.version` attribute
    Default: None

**DEFAULT_LOADER_ENGINE_CLASS**

::

    Class that takes a list of template loaders and attempts to load templates from them in order
    Default: 'graphql_persist.loaders.Engine'
    Note: Set variable to 'graphql_persist.loaders.CachedEngine' for caching documents

**DEFAULT_LOADER_CLASSES**

::

    A list of loader classes to import documents from a particular source
    Default: (
        'graphql_persist.loaders.AppDirectoriesLoader',
        'graphql_persist.loaders.FilesystemLoader',
        'graphql_persist.loaders.URLLoader',
    )

**APP_DOCUMENT_DIR**

::

    Subdirectory of installed applications for searches documents
    Default: 'documents'

**DOCUMENTS_EXT**

::

    GraphQL document file extension
    Default: '.graphql'

**DEFAULT_RENDERER_CLASSES**

::

    A list of renderer classes that may be used when returning a persisted query response
    Default: ()


.. |Pypi| image:: https://img.shields.io/pypi/v/django-graphql-persist.svg
   :target: https://pypi.python.org/pypi/django-graphql-persist

.. |Wheel| image:: https://img.shields.io/pypi/wheel/django-graphql-persist.svg
   :target: https://pypi.python.org/pypi/django-graphql-persist

.. |Build Status| image:: https://travis-ci.org/flavors/django-graphql-persist.svg?branch=master
   :target: https://travis-ci.org/flavors/django-graphql-persist

.. |Codecov| image:: https://img.shields.io/codecov/c/github/flavors/django-graphql-persist.svg
   :target: https://codecov.io/gh/flavors/django-graphql-persist

.. |Code Climate| image:: https://api.codeclimate.com/v1/badges/46eaf45a95441d5470a4/maintainability
   :target: https://codeclimate.com/github/flavors/django-graphql-persist
