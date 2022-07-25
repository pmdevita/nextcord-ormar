Migrations
==========

Migrations are provided through NXAlembic, a custom wrapper around `Alembic <https://github.com/sqlalchemy/alembic>`_
that automatically configures it and provides compatibility with Nextcord-Ormar's separate per-cog migration history.

Before Migrating
----------------

There are a couple things to know about how NXAlembic handles migrations

- If you are coming from Django, Alembic cannot work purely from a migration history like Django. Alembic must have a live database to compare against to make migrations.
- Table drops are not automatically detected. This was done to ensure Alembic wouldn't accidentally delete tables if you do not have all of your cogs loaded at once. To drop a database, you can create a blank migration and add the drop yourself.
- Alembic is currently unable to detect table name changes, column name changes, or anonymously named constraints. You can read more about `Alembic's limitations here <https://alembic.sqlalchemy.org/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect>`_.

Configuration
-------------

NXAlembic looks for a ``nxalembic.ini`` file in the current directory when run. This file should look something like
this.

.. code-block:: ini

    [nxalembic]
    module = example.demo
    bot = bot

where ``module`` is the Python import path to your bot's main script and ``bot`` is the name of your
:py:class:`nextcord_ormar.Bot` instance. During migration, NXAlembic will import your bot out of this script to
examine the models instantiated by your cogs.

Usage
-----

.. argparse::
    :ref: nextcord_ormar.nxalembic.parser.parser
    :prog: NXAlembic






Appendix
--------

Why can't I create database migrations without a database (ala Django?)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    `Here's a write up from SQLAlchemy's lead, Mike Bayer <https://github.com/sqlalchemy/alembic/issues/792#issuecomment-774556013>`_.
    In short, Alembic lacks the funding and manpower to implement the feature. Even Django had to put a Kickstarter
    together in order to fund one of their developers to work on it.
