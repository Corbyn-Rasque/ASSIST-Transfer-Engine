from __future__ import annotations

from uuid import UUID
from enum import StrEnum
from typing import Optional
from datetime import datetime
from pydantic import Field

from sources.api.agreement.attribute    import Attribute

from sources.api.types                  import Monomorphic

class Course:
    class Model (Monomorphic):
        '''
        Courses are versioned by year terms. The course model represents a snapshot in time of a course for the given begin and end year terms.

        :courseIdentifierParentId:  The unique id of the course in which versions can be derived
        :courseParentId:            A shared id across all cross-listed versions of a course. All courses that are cross-listed with one another will have the same `courseParentId`
        :courseTitle:               The title of the course
        :courseNumber:              The course number
        :prefix:                    The prefix
        :prefixParentId:            The unique id of this course's prefix in which prefix versions can be derived
        :prefixDescription:         The description of the prefix associated with this course
        :departmentParentId:        The unique id of this course's department in which department versions can be derived
        :department:                The department title
        :begin:                     The yearTermCode in which this course version becomes active
        :beginDate:                 The date on which this course version becomes active, corresponding to the `begin` `yearTermCode`
        :beginTermId:               The id of the year term in which this course version becomes active. Year term ids are returned from `YearTerm`
        :end:                       The yearTermCode in which this course version ceases to be active. If end is blank then this course version continues indefinitely. If end is populated with a yearTermCode, then it could mean that either a future course version continues this course version forward, likely with a revision, or the course is terminated.
        :endDate:                   The date on which this course version ceases to be active, corresponding to the `end` `yearTermCode`. `None` if `end` is blank
        :endTermId:                 The id of the year term in which this course version ceases to be active. `None` if `end` is blank. Year term ids are returned from `YearTerm`
        :minUnits:                  The minimum units
        :maxUnits:                  The maximum units
        :isTerminated:              Indicates the course has been terminated. When `True`, `end` will be populated with the final active `yearTermCode`
        :hasOutline:                Indicates that a course outline document exists for this course in the system.
        :isCsuTransferable:         Indicates the course is transferable to a California State University (CSU)
        :isUcTransferable:          Indicates the course is transferable to a University of California (UC)
        :crosslistedCourses:        Courses that are cross-listed with this course. Cross-listed courses share the same `courseParentId`
        :pathways:                  The UC Transfer Pathways associated with this course.

        [Documentation](https://prod.assistng.org/apidocs/docs/courses/get#course-model)
        '''
        courseIdentifierParentId:   int
        courseParentId:             int | None          = None
        courseTitle:                str
        courseNumber:               str
        prefix:                     str
        prefixParentId:             int
        prefixDescription:          str
        departmentParentId:         int
        department:                 str
        begin:                      str
        beginDate:                  datetime | None     = None
        beginTermId:                int | None          = None
        end:                        str
        endDate:                    datetime | None     = None
        endTermId:                  int | None          = None
        # endDate:                    Optional[datetime]  = Field(default = None)
        # endTermId:                  Optional[int]       = Field(default = None)
        minUnits:                   float
        maxUnits:                   float
        isTerminated:               bool | None         = None
        hasOutline:                 bool | None         = None
        isCsuTransferable:          bool | None         = None
        isUcTransferable:           bool | None         = None
        crosslistedCourses:         list[Course.Model] | None = None
        pathways:                   list[Pathway.Model] | None = None

    class Cell:
        class Crosslisted:
            class Model (Monomorphic):
                '''
                This model represents a cross listed course for the course in this cell.

                :course:    The cross listed course

                [Documentation](https://prod.assistng.org/apidocs/docs/courses/get#course-cell-cross-listed)
                '''
                course: Course.Model

        class Requisite:
            class Model (Monomorphic):
                '''
                :course:    The pre-requisite or co-requisite course
                :​type:      The type of requisite from [PreRequisite,CoRequisite]

                [Documentation](https://prod.assistng.org/apidocs/docs/courses/get#course-cell-requisite)
                '''
                type:   Requisite.Type
                course: Course.Model

class Denied:
    class Model (Course.Model):
        '''
        The Denied Course Model represents courses on a sending articulation that have been explicitly denied. This model extends [Course][Course].

        :denied:        The date the course is denied on attributes
        :attributes:    The attributes associated to the denied course

        [Course]: https://prod.assistng.org/apidocs/docs/courses/get#course-model
        [Documentation](https://prod.assistng.org/apidocs/docs/courses/get#denied-course-model)
        '''
        deniedOn:                   datetime
        attributes:                 list[Attribute.Model]

class Requisite:
    class Model (Course.Model):
        '''
        The Requisite Course Model represents the pre-requisite or co-requisite course for an associated course. This model extends [Course][Course].
        
        :id:                                    The unique id of the requisite
        :publishedCourseIdentifierYearTermId:   The yearTermId that this course version applies to, usually `None` when there's not a midyear revision for the course.
        :​type:                                  The type of requisite from [PreRequisite,CoRequisite]

        [Course]: https://prod.assistng.org/apidocs/docs/courses/get#course-model
        [Documentation](https://prod.assistng.org/apidocs/docs/courses/get#requisite-course-model)
        '''
        id:                                     UUID
        type:                                   Requisite.Type
        publishedCourseIdentifierYearTermId:    Optional[int]

    class Type (StrEnum):
        PreRequisite = 'PreRequisite'
        CoRequisite  = 'CoRequisite'

class Pathway:
    class Model (Monomorphic):
        '''
        A UC Transfer Pathway associated with a course, indicating the pathway, expectation, and sub-expectation the course satisfies, along with the term range for which the association is active.

        :pathwayId:             The unique id of the pathway
        :pathwayName:           The name of the pathway
        :pathwayCode:           The short code identifying the pathway
        :expectationId:         The unique id of the expectation within the pathway
        :expectationName:       The name of the expectation
        :subexpectationId:      The unique id of the sub-expectation within the expectation
        :subexpectationName:    The name of the sub-expectation
        :begin:                 The `yearTermCode` in which this pathway association becomes active
        :beginDate:             The date on which this pathway association becomes active
        :beginTermId:           The id of the year term in which this pathway association becomes active
        :end:                   The `yearTermCode` in which this pathway association ceases to be active. Blank if the association continues indefinitely.
        :endDate:               The date on which this pathway association ceases to be active. `None` if `end` is blank.
        :endTermId:             The id of the year term in which this pathway association ceases to be active. `None` if `end` is blank.

        [Documentation](https://prod.assistng.org/apidocs/docs/courses/get#pathway-model)
        '''
        pathwayId:                  int
        pathwayName:                str
        pathwayCode:                str
        expectationId:              int
        expectationName:            str
        subexpectationId:           int
        subexpectationName:         str
        begin:                      str
        beginDate:                  datetime
        beginTermId:                int
        end:                        str
        endDate:                    Optional[datetime]
        endTermId:                  Optional[int]

Course.Model.model_rebuild()