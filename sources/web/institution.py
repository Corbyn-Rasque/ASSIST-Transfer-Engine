from pydantic import BaseModel, field_validator
from enum import IntEnum

class Name (BaseModel):
    name:                       str
    hasDepartments:             bool
    hideInList:                 bool

class Term (BaseModel):
    class Type (IntEnum):
        SEMESTER    = 0
        QUARTER     = 1
        TRIMESTER   = 2

    termType:                   Type
    fromYear:                   int

    @field_validator('termType', mode='before')
    @classmethod
    def coerce_term_type(cls, v):
        if isinstance(v, str):
            return {'Semester': 0, 'Quarter': 1, 'Trimester': 2}[v]
        return v

class Institution (BaseModel):
    '''
    :id:        Represents the unique ID for the institution in the system. This value does not change from year to year and can be used when calling other APIs for data specific to the given institution.
    :names:     The names collection provides possible name values for the given institution depending on which year you are observing the data. When the fromYear value is specified, that name record applies to any academic years that start in that year as well as all following years up to the point where another name record starts. When the fromYear value is not specified, or not present, it means that record is the default value to use. In the above example, institution 14 has the name “Rancho Santiago College.” Starting in 1997 the institution’s name changed to “Santa Ana College.” This means you would use the name “Santa Ana College” when observing this institution in 1997 and newer records. In years prior to 1996, you would use the name “Santa Ana College.”
    :code:      A unique code, abbreviation, assigned to the institution.
    :isCommunityCollege: Self-evident
    :category:  An int value representing one of the possible Institution Type values in Institution.Category
    :termType:  (Deprecated) - in older version(s) of the API this value provided a term type that was not versioned by academic year and exists for backward-compatability.
    :beginId:   The four digit year in which the Institution started.
    :termTypeAcademicYears: The termTypeAcademicYears collection provides possible Term Types (see below) for the institutions given the academic year you are observing the data. Similar logic is applied to these values using the fromYear property as documented for the names collection (above).
    '''

    class Category (IntEnum):
        CSU     = 0
        UC      = 1
        CCC     = 2
        AICCU   = 5

    id:                         int
    names:                      list[Name]
    code:                       str
    prefers2016LegacyReport:    bool | None = None
    isCommunityCollege:         bool
    category:                   Category
    termType:                   Term.Type
    beginId:                    int
    termTypeAcademicYears:      list[Term]

    @field_validator('category', 'termType', mode='before')
    @classmethod
    def coerce_enum(cls, v):
        if isinstance(v, str):
            mapping = {
                # Category
                'CSU': 0, 'UC': 1, 'CCC': 2, 'AICCU': 5,
                # Term.Type
                'Semester': 0, 'Quarter': 1, 'Trimester': 2,
            }
            return mapping[v]
        return v