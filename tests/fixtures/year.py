import pytest
from pathlib import Path

from tests.json.data    import Model, Load, Compose
from api.year        import Year

class Example: 
    class Year:
        folder = Path('')

@pytest.fixture
def year() -> Model:
    return Load[Year](Example.Year.folder)('year')