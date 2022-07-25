import typing
import databases
from nextcord.ext import commands
import ormar
import sqlalchemy
import inspect

from nextcord_ormar.models import ModelMetaTemplate
from nextcord_ormar.models import AppModelMetaclass, ModelMetaTemplate


class ModuleNotFound(Exception):
    def __init__(self, name: str) -> None:
        msg = f'Module {name!r} could not be loaded.'
        super().__init__(msg)


class AppModel(ormar.Model, metaclass=AppModelMetaclass):
    pass


class OrmarApp:
    """
    Generate per-cog MetaModel classes for grouping into different database apps.
    """
    apps = {}

    @classmethod
    def create_app(cls, name: str) -> typing.Type[ModelMetaTemplate]:
        """
        Create a new database app

        :param name: The name of the database app
        :return: A MetaModel class to use in your models
        """
        frames = inspect.stack()
        frame = frames[1]
        module = inspect.getmodule(frame[0])
        app_module = None
        if module:
            app_module = module.__name__

        if name in cls.apps:
            raise Exception(f"App name \"{name}\" already registered in Ormar.")

        class ModelMeta(ModelMetaTemplate):
            _name = name
            _app_module = app_module
            metadata = sqlalchemy.MetaData()

        cls.apps[name] = ModelMeta
        return ModelMeta


class OrmarManager:
    """
    Manages the database connection and helps organize tables for migration.
    """
    def __init__(self, database_url):
        """

        :param database_url: An `SQLAlchemy database URL <https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls>`_
        """
        self.database_url = database_url
        self.database = databases.Database(database_url)
        self.engine = None

        # Bootstrap ModelMeta convenience into the database and grab its apps
        ModelMetaTemplate.database = self.database
        self.apps: typing.Dict[str, typing.Type[ModelMetaTemplate]] = OrmarApp.apps

    async def start(self):
        """
        Start the database connection
        """
        if not self.engine:
            self.engine = sqlalchemy.create_engine(self.database_url)

    async def close(self):
        """
        Close the database connection
        """
        if self.database:
            await self.database.disconnect()
            self.database = None


class Bot(commands.Bot):
    """
    A subclass of the Nextcord Bot class that adds integration for Ormar. Refer to the
    `Nextcord Bot docs <https://docs.nextcord.dev/en/stable/ext/commands/api.html#bot>`_.
    """
    def __init__(self, command_prefix, database_url, help_command=commands.bot._default, description=None, **kwargs):
        """
        Identical to the `Nextcord Bot <https://docs.nextcord.dev/en/stable/ext/commands/api.html#bot>`_ ``__init__``
        with the addition of the positional ``database_url`` parameter.

        :param command_prefix:
        :param database_url: An `SQLAlchemy database URL <https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls>`_
        :param help_command:
        :param description:
        :param kwargs:
        """
        super().__init__(command_prefix, help_command, description, **kwargs)
        self._ormar = OrmarManager(database_url)
        self.add_listener(self._ormar.start, "on_connect")

    async def close(self) -> None:
        """
        Nextcord Bot's close function. This is used to close the database connection so make sure to call ``super()``
        if you override it.

        :return:
        """
        # We register here right before close to make sure Tortoise closing is the last thing that happens
        # in case some cogs were dependent on Tortoise being open to finish an operation.
        self.add_listener(self._ormar.close, "on_close")
        await super().close()

