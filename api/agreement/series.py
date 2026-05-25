from __future__ import annotations

from uuid import UUID
from enum import StrEnum
from typing import TypeAlias

from api.course import Course as BaseCourse
from api.agreement.attribute import Attribute as BaseAttribute

from api.types import Monomorphic

class Course:
    class Model (BaseCourse.Model):
        '''
        The series course model extends the [Course][Course] model with a couple of fields that are needed when a course is placed on a Series.

        :id:        The unique id of a course on a series. On an articulation, this id can be referenced by the VisibleCrossListedCourses array and the CourseAttributes array
        :position:  The position this course should appear in the series

        [Course]: https://prod.assistng.org/apidocs/docs/courses/get#course-model
        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/series#series-course-model)
        '''
        id:         UUID
        position:   int

class Crosslisted:
    class Model (Course.Model):
        '''
        This model extends the [Series Course Model][Series Course Model]. This model represents a cross listed course for a course in the series array.

        :seriesCourseId:    The series course id in which this cross listed course belongs
        
        [Series Course Model]: https://prod.assistng.org/apidocs/docs/articulation/model/series#series-course-model
        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/series#series-cross-listed-course)
        '''
        seriesCourseId: UUID

class Attribute:
    class Model (BaseAttribute.Model):
        '''
        This model extends an [Attribute][Attribute]. This model represents an attribute for a course in the series array.
        
        :seriesCourseId:    The series course id in which this attribute belongs

        [Attribute]: https://prod.assistng.org/apidocs/docs/articulation/model/attribute
        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/series#series-attribute-course)
        '''
        seriesCourseId: UUID

class Cell:
    class Requisite:
        class Model (Monomorphic):
            '''
            This model represents a pre-requisite or a co-requisite for a course in the series array.

            :seriesCourseId:    The series course id in which this requisite belongs    
            :course:            The pre-requisite or co-requisite course  
            :​type:              The type of requisite from `CellRequisite.Type` 

            [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/series#series-cell-requisite)
            '''
            seriesCourseId: UUID
            type:           Cell.Requisite.Type
            course:         BaseCourse.Model

        class Type (StrEnum):
            '''
            ```
            CellRequisite.Type: PreRequisite | CoRequisite
            ```
            '''
            PreRequisite    = 'PreRequisite'
            CoRequisite     = 'CoRequisite'
    
    class Crosslisted:
        class Model (Monomorphic):
            '''
            :seriesCourseId:    The series course id in which this cross listed course belongs
            :course:            The cross-listed course

            [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/series#series-cell-cross-listed-course)
            '''
            seriesCourseId: UUID
            course: BaseCourse.Model

class Series:
    class Model (Monomorphic):
        '''
        :conjunction:   The type of conjunction between the courses in the series from `Series.Conjunction`
        :name:          The name of the series, usually derived from the courses contained in the series
        :course:        The array of courses contained in the series

        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/series#series-model)
        '''
        conjunction:    Series.Conjunction
        name:           str
        courses:        list[Course.Model]

    class Conjunction (StrEnum):
        '''
        ```
        Series.Conjunction: And | Or
        ```
        '''
        And = 'And'
        Or  = 'Or'

    Course:         TypeAlias = Course
    Crosslisted:    TypeAlias = Crosslisted
    Attribute:      TypeAlias = Attribute
    Cell:           TypeAlias = Cell

Series.Model.model_rebuild(_types_namespace={
    'Series': Series,
})