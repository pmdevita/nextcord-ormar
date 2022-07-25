Quickstart
==========

Before you start, you'll want to be roughly familiar with
`Nextcord's cogs <https://docs.nextcord.dev/en/stable/ext/commands/cogs.html>`_ and
`extensions <https://docs.nextcord.dev/en/stable/ext/commands/extensions.html>`_ and
`Ormar <https://collerek.github.io/ormar/>`_.


Installation
------------

Nextcord-Ormar is still in alpha so the best way to install is from the GitHub repository.

.. code-block:: console

    $ pip install git+https://github.com/pmdevita/nextcord-ormar


Import Nextcord-Ormar's bot class and pass it your `database URL <https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls>`_.

.. code-block:: python

    from nextcord_ormar import Bot

    bot = Bot(command_prefix="$", database_url="sqlite:///db.sqlite")

Defining and Using Models
-------------------------

In your cog file import OrmarApp to create an app,
then use AppModel to create a database model. Define your model like a `normal Ormar model <https://collerek.github.io/ormar/models/>`_.

If you prefer, you can also define your models elsewhere and import them into your cog.

.. code-block:: python

    import ormar
    from nextcord_ormar import OrmarApp, AppModel

    ModelMeta = OrmarApp.create_app("example")

    class ExampleTable(AppModel):
        class Meta(ModelMeta):
            pass

        id = ormar.Integer(primary_key=True)
        discord_id = ormar.BigInteger()
        message = ormar.Text()


You can then use this model in your cog.

.. code-block:: python

    from nextcord.ext import commands

    class Example(commands.Cog):
        def __init__(self, nextcord):
            self.nextcord = nextcord

        @commands.command("example")
        async def example(self, ctx: commands.Context, *args):
            new_example = await ExampleTable.objects.create(discord_id=ctx.author.id, message=args[0])
            await ctx.send("Hello!")


Database Setup and Migrations
----------

Before you can start the bot though, you'll need to set up migrations and the database. Create a file called
``nxalembic.ini`` in your project root folder and tell it how to import your bot.

.. code-block:: ini

    [nxalembic]
    module = example.demo
    bot = bot


You can think of this as ``from module import bot``, or in this instance, ``from example.demo import bot``. NXAlembic will
use it to import your bot along with your definitions for each model.

In the same folder, you can now use the ``nxalembic`` tool. Create migrations with

.. code-block:: shell

    $ nxalembic migrate --app example

Upgrade the database

.. code-block:: shell

    $ nxalembic upgrade --app example


Your bot is now ready to start!

Further examples
----------------

Take a look at the `example Nextcord project <https://github.com/pmdevita/nextcord-ormar/tree/master/example>`_.

