import pytest

from tests.json.data        import Registry, Load, Compose
from api.agreement.asset    import Asset

Example = Registry('asset')

Example +=  Load[Asset.Model](Example.folder)('asset')
Example +=  Load[Asset.Model](Example.folder)('asset', 'general/title')
Example +=  Load[Asset.Model](Example.folder)('asset', 'general/text')
Example +=  Load[Asset.Model](Example.folder)('asset', 'requirement/title')


@pytest.fixture
def course():
    return Example