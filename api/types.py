import re
from typing import Annotated, Optional
from pydantic import BaseModel, BeforeValidator
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

class Polymorphism(ModelMetaclass):
    registry:   dict = {}
    field:      str

    def __init__(cls, name, bases, namespace, field = 'type', **kwargs):
        super().__init__(name, bases, namespace, **kwargs)
        cls.field = field
        if field_value := namespace.get(field):
            Polymorphism.registry[field_value] = cls

        schema(cls)

    def __call__(cls, data: dict):
        field = cls.field
        if field in data and data[field] in Polymorphism.registry:
            return Polymorphism.registry[data[field]].model_validate(data)
        return super().__call__(data)
    
class Polymorphic (BaseModel, metaclass = Polymorphism):
    pass

class Monomorphism(ModelMetaclass):
    def __init__(cls, name, bases, namespace, **kwargs):
        super().__init__(name, bases, namespace, **kwargs)
        schema(cls)

class Monomorphic(BaseModel, metaclass = Monomorphism):
    pass