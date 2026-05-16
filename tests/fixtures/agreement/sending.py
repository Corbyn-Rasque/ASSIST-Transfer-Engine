import pytest

from pathlib import Path
from typing import Callable

from tests.json.data import Model, Load, Compose
from api.agreement.sending import Sending, Articulation, Template
import api.agreement.sending

import tests.fixtures.course                as course
import tests.fixtures.agreement.attribute   as attribute
import tests.fixtures.agreement.advisement  as advisement

class Example:
    class Articulation: 
        folder      = Path('agreement') / 'sending' / 'articulation'

        model:          Model
        item:           Model
        advisement:     Model
        conjunction:    Model

        class Group:
            folder  = Path('agreement') / 'sending' / 'articulation' / 'group'

            model:      Model
            item:       Model
            course:     Model
            advisement: Model

    class Template:
        folder      = Path('agreement') / 'sending'

        model:          Model

Example.Articulation.item = \
    Load[Articulation.Item](Example.Articulation.folder)('item')

Example.Articulation.advisement = \
    Compose[Articulation.Advisement](Example.Articulation.folder)('item', 'advisement')({
        'advisement':                   advisement.Example.Advisement.additionalNToReach
    })

Example.Articulation.conjunction = \
    Load[Articulation.Conjunction](Example.Articulation.folder)('conjunction')


Example.Articulation.Group.item = \
    Load[Articulation.Group.Item](Example.Articulation.Group.folder)('item')

Example.Articulation.Group.course = \
    Compose[Articulation.Group.Course](Example.Articulation.Group.folder)('item', 'course')({
        'visibleCrossListedCourses':    [course.Example.Course.model],
        'requisites':                   [course.Example.Course.requisite],
        'attributes':                   [attribute.Example.Attribute.model]
    })

Example.Articulation.Group.advisement = \
    Compose[Articulation.Group.Advisement](Example.Articulation.Group.folder)('item', 'advisement')({
        'advisement':                   advisement.Example.Advisement.additionalNToReach
    })

Example.Articulation.Group.model = \
    Compose[Articulation.Group](Example.Articulation.Group.folder)('item', 'group')({
        'items':                        [Example.Articulation.Group.course, 
                                         Example.Articulation.Group.advisement],
        'attributes':                   [attribute.Example.Attribute.model]
    })

Example.Articulation.model = \
    Compose[Articulation](Example.Articulation.folder)('articulation')({
        'deniedCourses':                [course.Example.Course.denied],
        'items':                        [Example.Articulation.advisement, 
                                        Example.Articulation.Group.model],
        'courseGroupConjunctions':      [Example.Articulation.conjunction],
        'attributes':                   [attribute.Example.Attribute.model]
    })

Example.Template.model = \
    Compose[Template](Example.Template.folder)('template')({
        'sendingArticulation':          Example.Articulation.model
    })

@pytest.fixture
def sending() -> Callable[[type[Articulation] | type[Template]], Model]:
    def load(type: type[Articulation] | type[Template]):
            match type:
                case api.agreement.sending.Articulation: return Example.Articulation.model           
                case api.agreement.sending.Template:     return Example.Template.model
    return load