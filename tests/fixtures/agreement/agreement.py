import pytest

from tests.json.data            import Registry, Load
from api.agreement.agreement    import Agreement

Example = Registry('agreement')

Example +=  Load[Agreement.Model](Example.folder)('agreement')

@pytest.fixture
def agreement():
    return Example