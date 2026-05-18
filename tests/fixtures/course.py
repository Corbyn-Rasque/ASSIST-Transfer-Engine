import pytest

from tests.json.data    import Registry, Load, Compose
from api.course         import Course, Denied, Requisite

Example = Registry('course')

Example +=  Load[Course.Model]   (Example.folder)('course')
Example +=  Load[Denied.Model]   (Example.folder)('course', 'denied')
Example +=  Load[Requisite.Model](Example.folder)('course', 'requisite')
Example +=  Compose[Course.Cell.Crosslisted.Model](Example.folder / 'cell')('crosslisted')({
                'course':   Example[Course.Model]
            })
Example +=  Compose[Course.Cell.Crosslisted.Model](Example.folder /  'cell')('crosslisted')({
                'course':   Example[Course.Model]
            })

@pytest.fixture
def course():
    return Example