Connection
==========

Depending on your database backend, you'll need to install a different
set of libraries and use a different database URL.

You can see more examples of database URLs on `SQLAlchemy's docs <https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls>`_.

SQLite
------

.. code-block:: shell

    $ pip install ormar[sqlite]

.. code-block:: python

    from nextcord_ormar import Bot

    bot = Bot(command_prefix="$", database_url="sqlite:///db.sqlite")


MySQL
------

.. code-block:: shell

    $ pip install ormar[mysql]

Ormar and SQLAlchemy use ``aiomysql`` and ``pymysql`` respectively so your
URL should start with ``mysql+pymysql://``

.. code-block:: python

    from nextcord_ormar import Bot

    bot = Bot(command_prefix="$", database_url="mysql+pymysql://username:password@hostname/database")



PostgreSQL
----------

.. code-block:: shell

    $ pip install ormar[mysql]

Ormar and SQLAlchemy use ``asyncpg`` and ``psycopg2`` respectively so your
URL should start with ``postgresql+psycopg2://``

.. code-block:: python

    from nextcord_ormar import Bot

    bot = Bot(command_prefix="$", database_url="postgresql+psycopg2://username:password@hostname/database")



