Advanced Usage
==============

Standalone
----------

You can also use your Nextcord-Ormar models outside of your Nextcord bot. Simply instantiate the
:py:class:`nextcord_ormar.OrmarManager` class yourself and call :py:meth:`nextcord_ormar.OrmarManager.start`
once the async loop has started.

The OrmarManager `must` be instantiated before models are imported. This is required so that models can
hook on to your database connection when Python loads them. It's potentially possible to create a workaround
for this so open an issue if this doesn't work for you.

.. code-block:: python

    from nextcord_ormar import OrmarManager

    manager = OrmarManager("sqlite:///db.sqlite")

    from mycog.models import MyModel

    # later once async has started

    await manager.start()
    await MyModel.objects.create(message="hi")


Other Discord.py Forks
----------------------

Nextcord-Ormar doesn't rely on many specific features of Nextcord so it's possible to easily implement support
for other Discord.py forks.

In your Bot's ``__init__`` function, create a ``_ormar`` property and assign it an :py:class:`nextcord_ormar.OrmarManager`
instance. Then, register it's :py:meth:`nextcord_ormar.OrmarManager.start` function with the ``on_connect`` event.

.. code-block:: python

    import discord
    from discord.ext import commands
    from nextcord_ormar import OrmarManager

    class MyBot(commands.Bot):
        def __init__(*args, **kwargs):
            self._ormar = OrmarManager("sqlite:///db.sqlite")
            self.add_listener(self._ormar.start, "on_connect")
            super().__init__(*args, **kwargs)


If your Discord.py fork supports a closing event, attach the :py:meth:`nextcord_ormar.OrmarManager.close` function
during ``close()``. We attach it here to ensure it happens last in case a cog needs to send data to the database
when it exits.

.. code-block:: python

    class MyBot(commands.Bot):
        ...
        async def close():
            self.add_listener(self._ormar.close, "on_close")
            await super().close()


If your fork doesn't support an ``on_close`` event, we can just exit it during the ``close()``.

.. code-block:: python

    class MyBot(commands.Bot):
        ...
        async def close():
            await self._ormar.close()
            await super().close()


Usage in cogs and NXAlembic should be



If you'd like to add official support for your fork, feel free to send a pull request.




