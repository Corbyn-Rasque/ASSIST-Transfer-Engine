from __future__ import annotations
from datetime import date

from api.types import Monomorphic

class AcademicYear:
    class Model (Monomorphic):
        '''
        Data in the ASSIST system is versioned to each Academic Year and in some cases Term. This means that with each new Academic Year, or even Term, the potential exists for the data you are working with to change. When an API requires a parameter named `academicYearId` it will be referring to the `id` value here.

        :id:    Represents the Academic Year's unique ID. Use this value with other APIs that require `academicYearId` parameter
        :code:  A display value representation of the academic year
        :start: The date at which the academic year begins
        :end:   The data at which the academic year ends

        [Documentation](https://prod.assistng.org/apidocs/docs/acadmicyears/get#academic-year-model)
        '''
        id:         int
        code:       str
        beginDate:  date
        endDate:    date

class YearTerm:
    class Model(Monomorphic):
        '''A custom class to parse a Term Code into a term and year, which can be serialized again if needbe. Comparable.
        
        :id:            Represents the Term's unique ID.
        :code:          A display value representation of the term
        :yearTermCode:  A display value representation of the term (same as `code`)
        :beginDate:     The date at which the term begins
        :endDate:       The data at which the term ends
        :description:   A textual description of the term
        
        [Documentation](https://prod.assistng.org/apidocs/docs/acadmicyears/terms#get-year-terms)
        '''
        id:             int
        code:           str
        yearTermCode:   str
        beginDate:      date
        endDate:        date
        description:    str