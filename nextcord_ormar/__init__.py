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


# Convenience allows us to generate separate ModelMeta for each application
class OrmarApp:
    apps = {}

    @classmethod
    def create_app(cls, name):
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
    def __init__(self, database_url):
        self.database_url = database_url
        self.database = databases.Database(database_url)
        self.engine = None

        # Bootstrap ModelMeta convenience into the database and grab its apps
        ModelMetaTemplate.database = self.database
        self.apps: typing.Dict[str, typing.Type[ModelMetaTemplate]] = OrmarApp.apps

    async def on_connect(self):
        if not self.engine:
            self.engine = sqlalchemy.create_engine(self.database_url)
            for app in self.apps.values():
                for table in app.metadata.tables.values():
                    print(table)
                # app.metadata.create_all(self.engine)

    async def on_close(self):
        pass
        # if self.engine:
        #     self.database.


class Bot(commands.Bot):
    def __init__(self, command_prefix, database_url, help_command=commands.bot._default, description=None, **kwargs):
        super().__init__(command_prefix, help_command, description, **kwargs)
        self._ormar = OrmarManager(database_url)
        self.add_listener(self._ormar.on_connect, "on_connect")

    async def close(self) -> None:
        if self._closed:
            return
        # We register here right before close to make sure Tortoise closing is the last thing that happens
        # in case some cogs were dependent on Tortoise being open to finish an operation.
        self.add_listener(self._ormar.on_close, "on_close")
        await super(Bot, self).close()

