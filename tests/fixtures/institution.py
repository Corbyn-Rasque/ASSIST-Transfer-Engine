import pytest
from pathlib import Path

from tests.json.data    import Model, Load, Compose
from api.institution import Institution

class Example: 
    class Institution:
        folder = Path('')

@pytest.fixture
def institution() -> Model:
    return Load[Institution](Example.Institution.folder)('institution')

