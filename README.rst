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


Configure the list of directories searched for GraphQL SDL definitions.

.. code:: python

    GRAPHQL_PERSIST = {
        'DOCUMENTS_DIRS': [
            '/app/documents',
        ],
    }


Schema definition
-----------------

**/app/documents/schema.graphql**

.. code:: graphql

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

    fragment userFields on UserType {
      id
      email
    }


**Query by "id"**

.. code:: json

    {
      "id": "schema",
      "operationName": "GetViewer",
      "variables": {}
    }


Operations definition
---------------------

The server needs to do **less processing** to parse the query and verify the parameters.

**/app/documents/GetViewer.graphql**

.. code:: graphql

    query GetViewer {
      viewer {
        ...userFields
      }
    }

    fragment userFields on UserType {
      id
      email
    }


**Query by "operationName"**

.. code:: json

    {
      "operationName": "GetViewer",
      "variables": {}
    }


Settings
--------

Here's a **list of settings** available in *Django-graphql-persist* and their default values.

**DOCUMENTS_DIRS**

::

    List of directories searched for GraphQL SDL definitions
    Default: None 

**CACHE_NAME**

::

    This selects the cache to use.
    Default: 'default'

**CACHE_TIMEOUT_HANDLER**

::

    A custom function to generate the timeout, in seconds, to use for the cache
    Default: lambda query_key: 0 if settings.DEBUG else None

**QUERY_KEY_HANDLER**

::

    A custom function to generate the persisted query key
    Default: lambda query_id, request: query_id

**DEFAULT_RENDERER_CLASSES**

::

    A list or tuple of renderer classes that may be used when returning a persisted query response
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
