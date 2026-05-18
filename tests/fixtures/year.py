import pytest
from pathlib import Path

from tests.json.data    import Model, Load, Compose
from api.year           import YearTerm, AcademicYear

class Example: 
    class Year:
        folder = Path('year')

@pytest.fixture
def yearterm() -> Model:
    return Load[YearTerm](Example.Year.folder)('yearterm')

@pytest.fixture
def yearterm() -> Model:
    return Load[AcademicYear](Example.Year.folder)('academicyear')