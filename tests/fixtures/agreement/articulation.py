import pytest

from tests.json.data            import Registry, Load
from api.agreement.articulation import Articulation

Example = Registry('agreement/articulation')

# All will be loaded, though only the last will be accessible.
Example +=  Load[Articulation.Model](Example.folder)('articulation', 'course')
Example +=  Load[Articulation.Model](Example.folder)('articulation', 'series')
Example +=  Load[Articulation.Model](Example.folder)('articulation', 'requirement')
Example +=  Load[Articulation.Model](Example.folder)('articulation', 'generaleducation')
Example +=  Load[Articulation.Model](Example.folder)('articulation', 'transferability')

@pytest.fixture
def articulation():
    return Example