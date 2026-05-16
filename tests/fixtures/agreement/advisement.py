import pytest

from pathlib import Path
from typing import Callable

from tests.json.data            import  Model, Load, Compose
from api.agreement.advisement   import  Base,           AdditionalNToReach, \
                                        NInAnyNAreas,   NInNDifferentAreas, \
                                        NFromUnits,     NFollowing,         \
                                        NToNFollowing
import api.agreement.advisement

class Example:
    class Advisement:
        folder = Path('agreement') / 'advisement'

        model:              Model
        additionalNToReach: Model
        nInAnyNAreas:       Model
        nInNDifferentAreas: Model
        nFromUnits:         Model
        nFollowing:         Model
        nToNFollowing:      Model

Example.Advisement.model = \
    Load[Base](Example.Advisement.folder)('advisement')

Example.Advisement.additionalNToReach = \
    Load[AdditionalNToReach](Example.Advisement.folder)('advisement', 'additionalntoreach')

Example.Advisement.nInAnyNAreas = \
    Load[NInAnyNAreas](Example.Advisement.folder)('advisement', 'nInAnyNAreas')

Example.Advisement.nInNDifferentAreas = \
    Load[NInNDifferentAreas](Example.Advisement.folder)('advisement', 'nInNDifferentAreas')

Example.Advisement.nFromUnits = \
    Load[NFromUnits](Example.Advisement.folder)('advisement', 'nFromUnits')

Example.Advisement.nFollowing = \
    Load[NFollowing](Example.Advisement.folder)('advisement', 'nFollowing')

Example.Advisement.nToNFollowing = \
    Load[NToNFollowing](Example.Advisement.folder)('advisement', 'nToNFollowing')

@pytest.fixture
def advisement() -> Callable[[type[Base] | 
                          type[AdditionalNToReach] | 
                          type[NInAnyNAreas] | 
                          type[NInNDifferentAreas] | 
                          type[NFromUnits] | 
                          type[NFollowing] | 
                          type[NToNFollowing]], Model]:
    def load(type: type[Base] |
                   type[AdditionalNToReach] |
                   type[NInAnyNAreas] | 
                   type[NInNDifferentAreas] | 
                   type[NFromUnits] | 
                   type[NFollowing] | 
                   type[NToNFollowing]):
            match type:
                case api.agreement.advisement.Base:                 return Example.Advisement.model
                case api.agreement.advisement.AdditionalNToReach:   return Example.Advisement.additionalNToReach
                case api.agreement.advisement.NInAnyNAreas:         return Example.Advisement.nInAnyNAreas
                case api.agreement.advisement.NInNDifferentAreas:   return Example.Advisement.nInNDifferentAreas
                case api.agreement.advisement.NFromUnits:           return Example.Advisement.nFromUnits
                case api.agreement.advisement.NFollowing:           return Example.Advisement.nFollowing
                case api.agreement.advisement.NToNFollowing:        return Example.Advisement.nToNFollowing
    return load