import pytest

from pathlib import Path
from typing import Callable
from types import SimpleNamespace

from tests.json.data    import Model, Load, Compose
from api.course      import Course, Denied, Requisite, Cell
import api.course

class Example:
     class Course:  
          folder = Path('course')
          
          model:        Model
          denied:       Model
          requisite:    Model

     class Cell:
        folder = Path('course') / 'cell'

        crosslisted:    Model
        requisite:      Model

Example.Course.model         = \
    Load[Course](Example.Course.folder)('course')

Example.Course.denied       = \
    Load[Denied](Example.Course.folder)('denied', 'course')

Example.Course.requisite    = \
    Load[Requisite](Example.Course.folder)('requisite', 'course')

Example.Cell.crosslisted    = \
    Compose[Cell.CrossListed](Example.Cell.folder)('crosslisted')({
        'course':   Example.Course.model
    })

Example.Cell.requisite      = \
    Compose[Cell.Requisite](Example.Cell.folder)('requisite')({
        'course':   Example.Course.model
    })

@pytest.fixture
def course() -> Callable[[type[Course] | type[Denied] | type[Requisite] | type[Cell]], Model]:
    def load(type: type[Course] | type[Denied] | type[Requisite] | type[Cell]):
            match type:
                case api.course.Course:              return Example.Course.model                 
                case api.course.Denied:              return Example.Course.denied
                case api.course.Requisite:           return Example.Course.requisite
                case api.course.Cell.CrossListed:    return Example.Cell.crosslisted
                case api.course.Cell.Requisite:      return Example.Cell.requisite
    return load