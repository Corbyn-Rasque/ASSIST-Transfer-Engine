import pytest

from pathlib import Path
from typing import Callable

from tests.json.data            import  Registry, Load
from api.agreement.advisement   import  Advisement

Example = Registry('agreement/advisement')

# These will all save over each other (shouldn't error out) and you'll be left with the last one. 
Example += Load[Advisement.Model](Example.folder)('advisement', 'additionalNToReach')
Example += Load[Advisement.Model](Example.folder)('advisement', 'nInAnyNAreas')
Example += Load[Advisement.Model](Example.folder)('advisement', 'nInNDifferentAreas')
Example += Load[Advisement.Model](Example.folder)('advisement', 'nFromUnits')
Example += Load[Advisement.Model](Example.folder)('advisement', 'nFollowing')
Example += Load[Advisement.Model](Example.folder)('advisement', 'nToNFollowing')

@pytest.fixture
def advisement():
    return Example