import pytest

from pathlib    import Path
from typing     import Callable

from tests.json.data                    import Model, Load, Compose
from api.agreement.generaleducation  import GeneralEducation
import api.agreement.generaleducation

class Example:
    class GeneralEducation:
        folder = Path('')

        model: Model

Example.GeneralEducation.model = \
    Load[GeneralEducation](Example.GeneralEducation.folder)('generaleducation')

@pytest.fixture
def generaleducation() -> Callable[[type[GeneralEducation]], Model]:
    def load(type: type[GeneralEducation]):
        match type:
            case api.agreement.generaleducation.GeneralEducation: return Example.GeneralEducation.model
    return load