from __future__ import annotations

from enum import IntEnum
from typing import Optional
from pydantic import Field, BaseModel

from sources.api.types import Monomorphic

class Institution:
    class Model (Monomorphic):
        '''
        In addition to being versioned by Academic Year or Year Terms, data in the ASSIST system is associated with Institutions. Allows you to get information about that institution, such as the name (which can change over time).

        :id:                    Represents the unique ID for the institution in the system. This value does not change from year to year and can be used when calling other APIs for data specific to the given institution.
        :names:                 The names collection provides possible name values for the given institution depending on which year you are observing the data. When the `fromYear` value is specified, that name record applies to any academic years that start in that year as well as all following years up to the point where another name record starts. When the `fromYear` value is not specified, or not present, it means that record is the default value to use.
        :code:                  A unique code, abbreviation, assigned to the institution.
        :isCommunityCollege:    A `True` or `False` value indicating if the given institution is a Community College (CCC).
        :category:              An `int` value representing one of the possible `Institution Type` values below.
        :termType:              (Deprecated) - in older version(s) of the API this value provided a term type that was not versioned by academic year and exists for backward-compatability.
        :beginId:               An `int` value for the initial year of the institution.
        :termTypeAcademicYears: The termTypeAcademicYears collection provides possible `Term Types` for the institutions given the academic year you are observing the data. Similar logic is applied to these values using the `fromYear` property as documented for the names collection.
        
        [Documentation](https://prod.assistng.org/apidocs/docs/institutions/get#institution-model)
        '''
        id:                     int
        names:                  list[Institution.Name]
        code:                   str
        isCommunityCollege:     bool
        category:               Institution.Types
        termType:               Institution.TermType
        beginId:                int
        termTypeAcademicYears:  list[Institution.Term]
    
    class Types (IntEnum):
        '''
        ```
        Institution.Model.Types: CSU | UC | CCC | AICCU
        ```
        '''
        CSU         = 0
        UC          = 1
        CCC         = 2
        AICCU       = 5

    class TermType (IntEnum):
        '''
        ```
        Institution.Model.TermType: Semester | Quarter | Trimester
        ```
        '''
        Semester  = 0
        Quarter   = 1
        Trimester = 2

    class History (BaseModel):
        fromYear:       Optional[int] = Field(default = None)

    class Name (History):
        name:           str
        hasDepartments: bool
        hideInList:     bool

    class Term (History):
        termType:       Institution.TermType