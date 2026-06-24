from pydantic import BaseModel, field_validator
from enum import StrEnum
from typing import Union
from datetime import datetime
import json

from sources.web.institution            import Institution
from sources.web.year                   import AcademicYear

from sources.api.agreement.asset        import Asset, PublishedAgreement
from sources.api.agreement.receiving    import ReceivingArticulation

from sources.api.types import Polymorphic
from pydantic import ConfigDict

Polymorphic.model_config = ConfigDict(extra='ignore')

class Availability (BaseModel):
    uctca:      list[int]
    csutc:      list[int]
    uctel:      list[int]
    csuge:      list[int]
    igetc:      list[int]
    csuai:      list[int]
    calgetc:    list[int]

    @field_validator('uctca', 'csutc', 
                     'uctel', 'csuge', 
                     'igetc', 'csuai', 
                     'calgetc')
    @classmethod
    def sort_ids(cls, v: list[int]) -> list[int]:
        return sorted(v)

class List (BaseModel):
    institutionParentId:    int
    institutionName:        str
    code:                   str
    isCommunityCollege:     bool
    sendingYearIds:         list[int]
    receivingYearIds:       list[int]

class Department(BaseModel):
    name: str
    articulations: list[ReceivingArticulation.Models]

class Agreement (BaseModel):
    class Type (StrEnum):
        PREFIX                  = 'Prefix'
        DEPARTMENT              = 'Department'
        MAJOR                   = 'Major'
        GENERALEDUCATION        = 'GeneralEducation'
        ALLDEPARTMENTS          = 'AllDepartments'
        ALLPREFIXES             = 'AllPrefixes'
        ALLMAJORS               = 'AllMajors'
        ALLGENERALEDUCATION     = 'AllGeneralEducation'
        SENDINGDEPARTMENT       = 'SendingDepartment'
        SENDINGPREFIX           = 'SendingPrefix'
        ALLSENDINGPREFIXES      = 'AllSendingPrefixes'
        ALLSENDINGDEPARTMENTS   = 'AllSendingDepartments'

    name:                   str
    type:                   Type
    publishDate:            datetime
    receivingInstitution:   Institution
    sendingInstitution:     Institution
    academicYear:           AcademicYear
    templateAssets:         list[Union[PublishedAgreement.Model, Asset.Models]] | None = None
    articulations:          list[Union[Department, ReceivingArticulation.Models]] | None = None

    @field_validator('receivingInstitution', 'sendingInstitution', 
                     'academicYear', 'templateAssets', 'articulations',
                     mode = 'before')
    @classmethod
    def parse_json_string(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v

class Result (BaseModel):
    result:                 Agreement
    validationFailure:      bool | None
    isSuccessful:           bool

class Reports (BaseModel):
    class Type (StrEnum):
        MAJOR       = 'major'
        DEPARTMENT  = 'dept'
        PREFIX      = 'prefix'

    class Report (BaseModel):
        label:              str
        key:                str
        ownerInstitutionId: int

    reports:    list[Report]
    allReports: list[Report]