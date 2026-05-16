import pytest

from pathlib    import Path
from typing     import Callable

from tests.json.data            import Model, Load, Compose
from api.agreement.attribute import Attribute
import api.agreement.attribute

class Example:
    class Attribute:
        folder = Path('agreement')

        model:  Model

Example.Attribute.model = \
    Load[Attribute](Example.Attribute.folder)('attribute')

@pytest.fixture
def attribute() -> Callable[[type[Attribute]], Model]:
    def load(type: type[Attribute]):
            match type:
                case api.agreement.attribute.Attribute: return Example.Attribute.model
    return load