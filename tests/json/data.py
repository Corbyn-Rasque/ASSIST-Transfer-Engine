import json
from pathlib import Path
from functools import reduce
from pydantic import BaseModel

class Model:
    '''
    Holds both the dict generated directly from the json with the json module, as well as the parsed Pydantic BaseModel-derived model instantiated with the dictionary data. This class is simply meant to be inherited from to for loading the dictionary, and model is meant to be instantiated by in the proper way from test data, whether directly loaded from example json (if fully specified) or loaded and with empty fields that are composed of other models dictionaries passed in from Model objects.

    :dictionary:    Raw dictionary containing the example data for the model.
    :model:         Pydantic BaseModel-derived class instance, populated with the example data.
    '''
    dictionary: dict
    model:      BaseModel

    def load(self, folder: str):
        '''Curried function that takes a (folder) followed by (*filenames) without their extension.'''

        def file(name) -> dict:
            return json.loads((Path(__file__).parent / folder / f'{name}.json').read_text())
        def files(*names: str) -> dict:
            return reduce(lambda basemodel, extended: basemodel | extended, map(file, names))
        return files

class LoadMeta (type):
    '''
    A factory metaclass designed to take a folder, files, and Pydantic BaseModel type in the form `SomeClass[BaseModel](Path)(*files)` and pass it as `SomeClass(model, folder, *files)`. Syntactic sugar & whatnot...
    '''

    def __getitem__(cls, model):
        def folder(folder: str):
            def files(*files: str):
                return cls(model, folder, *files)
            return files
        return folder

class Load (Model, metaclass = LoadMeta):
    '''
    A custom class that reads json files from a folder and assembled them into a single dictionary to allow creating extended data types from consituent pieces for testing and verification. Inherits from `Data`, which has `dictionary` & `model` attributes.

    Use: `Compose[BaseModel](Path)(*files)`  Note: files passed as names **without** extension
    
    :dictionary:    Contains the raw assembled dictionary.
    :model:         The validated model created from the Pydantic BaseModel-derived class passed by item notation to class during instantiation.'''
    dictionary: dict
    model:      BaseModel

    def __init__(self, model: BaseModel, folder: str, *files: str):
        self.dictionary = self.load(folder)(*files)
        self.model      = model.model_validate(self.dictionary)
    
class ComposeMeta (type):
    '''
    A factory metaclass designed to take a folder, files, Pydantic BaseModel type, and key value overrides (for empty object values in the test json) in the form `Compose[BaseModel](Path)(*files)({'key': Model()})` and pass it as `SomeClass(model, folder, *file, dict)`. Syntactic sugar & whatnot...
    '''
    def __getitem__(cls, model):
        def folder(folder: str):
            def files(*files: str):
                def dictionary(dict: dict):
                    return cls(model, dict, folder, *files)
                return dictionary
            return files
        return folder

class Compose (Model, metaclass = ComposeMeta):
    '''
    A custom class that composes a model from other models. The composed model is loaded from a json with empty objects where composed objects fill in. The data to be filled in is passed through a dictionary replacement from the dict given. Dictionary values passed in are expected to be of Model type (which Compose and Load inherit from), which contain `dictionary` and `model` attributes. 
    
    Use: `Compose[BaseModel](Path)(*files)({'key': Model()})`  Note: files passed as names **without** extension
    
    :dictionary:    Contains the raw assembled dictionary.
    :model:         The validated model created from the Pydantic BaseModel-derived class passed by item notation to class during instantiation.'''
    dictionary: dict
    model:      BaseModel

    def __init__(self, model: BaseModel, dict: dict, folder: str, *files: str):
        self.dictionary = self.load(folder)(*files)
        
        for key, value in dict.items():
            match value:
                case Model(): self.dictionary[key] = value.dictionary
                case list():  self.dictionary[key] = [data.dictionary for data in value]
                case _:       self.dictionary[key] = value

        self.model = model.model_validate(self.dictionary)