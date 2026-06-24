import re
from typing import Annotated, Optional, ClassVar, Any, TypeAlias, cast
from pydantic import BaseModel, BeforeValidator, Field
from pydantic._internal._model_construction import ModelMetaclass

# Used for the numerous `type` attributes throughout models, since :type: is a reserved keyword for Pylance and Sphinx.
# Type must be second in the attributes description list or beyond for formatting to work this way.
INVISIBLE_CHARACTERS = ['\u200b', '\u200c']

def schema(model):
    '''Function designed to parse the docstring and assign attribute descriptions from the docstring to the Pydantic model. Also allows for population by name by default.'''

    model.model_config['populate_by_name'] = True

    doc = model.__doc__ or ''
    invisible = f'[{"".join(INVISIBLE_CHARACTERS)}]?'

    for name, field in model.model_fields.items():
        if field.description: continue
        if match := re.search(rf':{invisible}{re.escape(name)}:\s*(.+)', doc):
            field.description = match.group(1).strip()
    return model

def null_or_blank(v):
    if (v is None ) or (isinstance(v, str) and not v.strip()):
        return None
    return v

type OptionalBlank = Annotated[
    Optional[str],
    BeforeValidator(null_or_blank),
]


class Polymorphic(BaseModel):
    _union: ClassVar[Any] = None
    _field: ClassVar[str] = "type"

    def __init_subclass__(cls, field="type", **kwargs):
        super().__init_subclass__(**kwargs)

        schema(cls)

        if Polymorphic in cls.__bases__:
            cls._field = field
            cls._union = None
            return

        parent = next(
            base for base in cls.__bases__
            if issubclass(base, Polymorphic) and base is not Polymorphic
        )

        cls._field = field or parent._field
        cls._union = parent._union

        parent._union = cls if parent._union is None else parent._union | cls

class Models:
    @classmethod
    def annotated(cls):
        union = cls.Model._union
        field = cls.Model._field

        if union is None:
            raise TypeError("No polymorphic subclasses registered")

        return Annotated[cast(Any, union), Field(discriminator=field)]


# class Polymorphism(ModelMetaclass):
#     registry:   dict = {}
#     field:      str

#     def __init__(cls, name, bases, namespace, field = 'type', **kwargs):
#         super().__init__(name, bases, namespace, **kwargs)
#         cls.field = field
#         if field_value := namespace.get(field):
#             Polymorphism.registry[field_value] = cls

#         schema(cls)

    # def __call__(cls, data: dict):
    #     field = cls.field
    #     if field in data and data[field] in Polymorphism.registry:
    #         return Polymorphism.registry[data[field]].model_validate(data)
    #     return super().__call__(data)
    
# class Polymorphic (BaseModel, metaclass = Polymorphism):
#     pass

class Monomorphism(ModelMetaclass):
    def __init__(cls, name, bases, namespace, **kwargs):
        super().__init__(name, bases, namespace, **kwargs)
        schema(cls)

class Monomorphic(BaseModel, metaclass = Monomorphism):
    pass