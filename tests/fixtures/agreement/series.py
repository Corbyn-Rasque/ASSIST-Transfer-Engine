import pytest
from pathlib import Path
from types import SimpleNamespace

from tests.json.data            import Model, Load, Compose
from api.agreement.series    import Series


Example = SimpleNamespace(
    Series = SimpleNamespace(folder = Path('agreement') / 'series')
)

@pytest.fixture
def series():
    return Load[Series](Example.Series.folder)('series')