import pytest

from pathlib    import Path
from typing     import Callable

from tests.json.data            import Model, Load, Compose
from api.agreement.asset import Asset
import api.agreement.asset