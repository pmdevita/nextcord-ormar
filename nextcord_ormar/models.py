import typing

import ormar
from ormar.models.metaclass import ModelMetaclass


class AppModelMetaclass(ModelMetaclass):
    def __new__(mcs: ModelMetaclass, name: str, bases: typing.Any, attrs: dict):
        # If this model doesn't have a table name set, create one from the app name and its name
        if "Meta" in attrs:
            if not hasattr(attrs["Meta"], "tablename"):
                attrs["Meta"].tablename = f"{attrs['Meta']._name}.{name.lower()}s"
        return super().__new__(mcs, name, bases, attrs)


class ModelMetaTemplate(ormar.ModelMeta):
    database = None
