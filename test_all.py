import pytest, glob
from typing import Annotated
from pydantic import BaseModel, TypeAdapter

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


def load(model: BaseModel | Annotated, location: str):
    with open(location) as data:
        match type:
            case BaseModel(): return model.model_validate_json(data.read())
            case _:            return TypeAdapter(model).validate_json(data.read())


@pytest.mark.parametrize('path', glob.glob('tests/agreement/advisement/*.json'))
def test_advisements(path):
    assert load(advisement.Advisement.Models, path)

def test_agreement():
    folder = 'tests/agreement/'
    assert load(agreement.Agreement.Model, folder + 'Agreement.json')

def test_asset():
    folder = 'tests/agreement/asset/'

    assert load(asset.Asset.Models, folder + 'GeneralText.json')
    assert load(asset.Asset.Models, folder + 'GeneralTitle.json')
    assert load(asset.Asset.Models, folder + 'RequirementTitle.json')
    assert load(asset.Asset.Models, folder + 'Group.json')

    assert load(asset.PublishedAgreement.Model, folder + 'PublishedAgreement.json')

def test_attribute():
    folder = 'tests/agreement/'
    assert load(attribute.Attribute.Model, folder + 'Attribute.json')

def test_generaleducation():
    folder = 'tests/agreement/'
    assert load(generaleducation.GeneralEducation.Model, folder + 'GeneralEducation.json')

@pytest.mark.parametrize('path', glob.glob('tests/agreement/receiving/*.json'))
def test_receiving(path):
    assert load(receiving.ReceivingArticulation.Models, path)

def test_requirement():
    folder = 'tests/agreement/'
    assert load(requirement.Requirement.Model, folder + 'Requirement.json')

def test_sending():
    folder = 'tests/agreement/sending/'

    assert load(sending.SendingArticulation.Model, folder + 'SendingArticulation.json')
    assert load(sending.SendingTemplateArticulation.Model, folder + 'SendingTemplateArticulation.json')

def test_series():
    folder = 'tests/agreement/series/'

    assert load(series.Attribute.Model, folder + 'Attribute.json')
    assert load(series.Course.Model, folder + 'Course.json')
    assert load(series.Crosslisted.Model, folder + 'Crosslisted.json')
    assert load(series.Series.Model, folder + 'Series.json')

    folder += 'cell/'

    assert load(series.Cell.Crosslisted.Model, folder + 'Crosslisted.json')
    assert load(series.Cell.Requisite.Model, folder + 'Requisite.json')

def test_course():
    folder = 'tests/course/'

    assert load(course.Course.Model, folder + 'Course.json')
    assert load(course.Denied.Model, folder + 'Denied.json')
    assert load(course.Requisite.Model, folder + 'Requisite.json')

    folder += 'cell/'

    assert load(course.Course.Cell.Crosslisted.Model, folder + 'Crosslisted.json')
    assert load(course.Course.Cell.Requisite.Model, folder + 'Requisite.json')

def test_institution():
    folder = 'tests/'

    assert load(institution.Institution.Model, folder + 'Institution.json')

def test_year():
    folder = 'tests/year/'

    assert load(year.AcademicYear.Model, folder + 'AcademicYear.json')
    assert load(year.YearTerm.Model, folder + 'YearTerm.json')