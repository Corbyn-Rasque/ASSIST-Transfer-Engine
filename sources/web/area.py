from pydantic import BaseModel

from sources.web.year import AcademicYear

class Area (BaseModel):
    id:             int
    areaType:       int
    name:           str
    description:    str
    begin:          AcademicYear
    end:            AcademicYear
    sortOrder:      int