import pytest, glob
from pathlib import Path
from pydantic import TypeAdapter

import sources.api.agreement.advisement         as advisement
import sources.api.agreement.agreement          as agreement
import sources.api.agreement.asset              as asset
import sources.api.agreement.attribute          as attribute
import sources.api.agreement.generaleducation   as generaleducation
import sources.api.agreement.instruction        as instruction
import sources.api.agreement.receiving          as receiving
import sources.api.agreement.requirement        as requirement
import sources.api.agreement.sending            as sending
import sources.api.agreement.series             as series

import sources.api.course                       as course
import sources.api.institution                  as institution
import sources.api.year                         as year

FIXTURES = Path(__file__).parent / 'fixtures'

def load(model, location: str):
    with open(location) as data:
        return TypeAdapter(model).validate_json(data.read())


@pytest.mark.parametrize('path', glob.glob(f'{FIXTURES}/agreement/advisement/*.json'))
def test_advisements(path):
    assert load(advisement.Advisement.Models, path)

def test_agreement():
    folder = f'{FIXTURES}/agreement/'
    assert load(agreement.Agreement.Model, folder + 'Agreement.json')

def test_asset():
    folder = f'{FIXTURES}/agreement/asset/'

    assert load(asset.Asset.Models, folder + 'GeneralText.json')
    assert load(asset.Asset.Models, folder + 'GeneralTitle.json')
    assert load(asset.Asset.Models, folder + 'RequirementTitle.json')
    assert load(asset.Asset.Models, folder + 'Group.json')

    assert load(asset.PublishedAgreement.Model, folder + 'PublishedAgreement.json')

@pytest.mark.parametrize('name, cells', [
    ('CourseSeries',    {'Course', 'Series'}),
    ('Requirement',     {'Requirement'}),
    ('CalGetc',         {'Course', 'CALGETC'}),
])
def test_asset_group(name, cells):
    group   = load(asset.Asset.Models, f'{FIXTURES}/agreement/asset/group/{name}.json')
    Section = asset.Asset.Group.Section
    assert isinstance(group, asset.Asset.Group)

    # Sections and cells must parse as their concrete types. Typed as the base
    # models, they validate but silently drop every row and cell.
    assert all(isinstance(s, (Section, asset.Asset.Group.SectionHeader)) for s in group.sections)

    parsed = [cell for s in group.sections if isinstance(s, Section) for row in s.rows for cell in row.cells]
    assert {type(cell).__name__ for cell in parsed} == cells

def test_attribute():
    folder = f'{FIXTURES}/agreement/'
    assert load(attribute.Attribute.Model, folder + 'Attribute.json')

def test_generaleducation():
    folder = f'{FIXTURES}/agreement/'
    assert load(generaleducation.GeneralEducation.Model, folder + 'GeneralEducation.json')

@pytest.mark.parametrize('path', glob.glob(f'{FIXTURES}/agreement/receiving/*.json'))
def test_receiving(path):
    assert load(receiving.ReceivingArticulation.Models, path)

def test_requirement():
    folder = f'{FIXTURES}/agreement/'
    assert load(requirement.Requirement.Model, folder + 'Requirement.json')

def test_sending():
    folder = f'{FIXTURES}/agreement/sending/'

    assert load(sending.SendingArticulation.Model, folder + 'SendingArticulation.json')
    assert load(sending.SendingTemplateArticulation.Model, folder + 'SendingTemplateArticulation.json')

def test_sending_course_groups():
    # (FR 2 And FR 1) Or (FR 2 And FR 1H)
    articulation = load(sending.SendingArticulation.Model, f'{FIXTURES}/agreement/sending/CourseGroups.json')

    # Course group items must parse as their concrete types. Typed as the base
    # model, they validate but silently drop every course.
    assert articulation.items is not None

    # Course group items must parse as their concrete types. Typed as the base
    # model, they validate but silently drop every course.
    groups = [g for g in articulation.items if isinstance(g, sending.SendingArticulation.CourseGroup)]
    assert len(groups) == len(articulation.items)

    items   = [item for group in groups for item in group.items]
    courses = [c for c in items if isinstance(c, sending.SendingArticulation.CourseGroup.Course)]
    assert len(courses) == len(items)
    assert sorted(f'{c.prefix} {c.courseNumber}' for c in courses) == ['FR 1', 'FR 1H', 'FR 2', 'FR 2']

def test_series():
    folder = f'{FIXTURES}/agreement/series/'

    assert load(series.Attribute.Model, folder + 'Attribute.json')
    assert load(series.Course.Model, folder + 'Course.json')
    assert load(series.Crosslisted.Model, folder + 'Crosslisted.json')
    assert load(series.Series.Model, folder + 'Series.json')

    folder += 'cell/'

    assert load(series.Cell.Crosslisted.Model, folder + 'Crosslisted.json')
    assert load(series.Cell.Requisite.Model, folder + 'Requisite.json')

def test_course():
    folder = f'{FIXTURES}/course/'

    assert load(course.Course.Model, folder + 'Course.json')
    assert load(course.Denied.Model, folder + 'Denied.json')
    assert load(course.Denied.Model, folder + 'DeniedUndated.json').deniedOn is None
    assert load(course.Requisite.Model, folder + 'Requisite.json')

    folder += 'cell/'

    assert load(course.Course.Cell.Crosslisted.Model, folder + 'Crosslisted.json')
    assert load(course.Course.Cell.Requisite.Model, folder + 'Requisite.json')

def test_institution():
    folder = f'{FIXTURES}/'

    assert load(institution.Institution.Model, folder + 'Institution.json')

def test_year():
    folder = f'{FIXTURES}/year/'

    assert load(year.AcademicYear.Model, folder + 'AcademicYear.json')
    assert load(year.YearTerm.Model, folder + 'YearTerm.json')