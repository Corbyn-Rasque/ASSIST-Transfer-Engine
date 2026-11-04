from pydantic import BaseModel, field_validator
from enum import IntEnum

from sources.web.year                   import Term

# from sources.api.types import Polymorphic
# from pydantic import ConfigDict

# Polymorphic.model_config = ConfigDict(extra = 'ignore')

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

class Area (BaseModel):
    id:             int
    areaType:       int
    name:           str
    description:    str
    begin:          Term
    end:            Term
    sortOrder:      int

class Categories (BaseModel):
    class Type (IntEnum):
        GE_BREADTH  = 1
        DEPARTMENT  = 2
        MAJOR       = 3
        PREFIX      = 10

    label:                  str
    code:                   str
    reportType:             Type
    reportCategoryType:     int
    courseTransferItemType: int
    hasReports:             bool