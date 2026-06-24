from pydantic import BaseModel
from datetime import datetime
from enum import IntEnum

from sources.web.year import AcademicYear

class Area (BaseModel):
    areaType:                   int
    areaParentId:               int
    code:                       str
    codeDescription:            str
    courseIdentifierParentId:   int
    beginDate:                  datetime
    beginTermCode:              str
    endDate:                    datetime
    endTermCode:                str
    sortOrder:                  int

class Notation (BaseModel):
    displayText:                str
    prefixCode:                 str
    courseNumber:               str
    eventDate:                  datetime
    eventTerm:                  str
    positionNumber:             int

class Course (BaseModel):
    footnoteParentIds:          list
    prefixParentId:             int
    prefixCode:                 str
    prefixDescription:          str
    departmentName:             str
    courseIdentifierParentId:   int
    courseNumber:               str
    courseTitle:                str
    courseParentId:             int
    isCsuTransferable:          bool
    minUnits:                   float
    maxUnits:                   float
    beginDate:                  datetime
    beginTermCode:              str
    endDate:                    datetime
    endTermCode:                str
    transferAreas:              list[Area]
    isRepeatable:               bool
    identifier:                 str
    notations:                  list

class List (BaseModel):
    class Type (IntEnum):
        CSUTC   = 0
        UCTCA   = 1
        UCTEL   = 2
        IGETC   = 3
        CSUGE   = 4
        CSUAI   = 5

        CALGETC = 8

    listType:                   Type
    institutionName:            str
    academicYear:               AcademicYear
    courseInformationList:      list[Course]