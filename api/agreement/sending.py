from __future__ import annotations

from uuid import UUID
from enum import StrEnum
from typing import Literal, Optional

from api.agreement.attribute    import Attribute
from api.agreement.advisement   import Advisement
from api.course                 import Course, Denied, Requisite

from api.types                  import Monomorphic, Polymorphic

class SendingArticulation:
    class Model (Monomorphic):
        '''
        This model composes all the data on the sending side of the articulation.

        :noArticulationReason:      The reason why this articulation has no sending articulation. This field should be null if it has been articulated
        :deniedCourses:             An array of courses that have explicitly been denied
        :items:                     An array of sending articulation items that is polymorphic to the type of sending articulation it is
        :courseGroupConjunctions:   An array of conjunctions that can be applied between the array of sending articulation items
        :​type:                      The type of SendingArticulation from `SendingArticulation.Type`
        :attributes:                Cell-level attributes associated to the sending side of the articulation

        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/sending#sending-articulation-model)
        '''
        noArticulationReason:       Optional[str]
        deniedCourses:              list[Denied.Model]
        items:                      list[SendingArticulation.Item.Model]
        courseGroupConjunctions:    list[SendingArticulation.CourseGroup.Conjunction.Model]
        type:                       SendingArticulation.Type
        attributes:                 list[Attribute.Model]

    class Type (StrEnum):
        '''
        ```
        SendingArticulation.Type: SendingArticulation | TemplateOverride
        ```
        '''
        SendingArticulation = 'SendingArticulation'
        TemplateOverride    = 'TemplateOverride'

    class Item:
        class Model (Polymorphic):
            '''
            The base sending articulation model contains fields that are common to all sending articulation items.

            :position:      The position in the array that the sending item should display
            :​type:          The type of sending articulation item from `Articulation.Item.Type`

            [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/sending#sending-articulation-item-base-model)
            '''
            position:   int
            type:       SendingArticulation.Item.Type

        class Type (StrEnum):
            '''
            ```
            SendingArticulation.Item.Type: CourseGroup | Advisement
            ```
            '''
            CourseGroup = 'CourseGroup'
            Advisement  = 'Advisement'

    class CourseGroup (Item.Model):
        '''
        This model extends the [Sending Articulation Item][Sending Articulation Item] if the sending articulation type is a `CourseGroup`.

        :courseConjunction: The conjunction relationship for the items from `SendingArticulation.CourseGroup.Conjunction`
        :​type:              `SendingArticulation.Item.Type.CourseGroup`

        [Sending Articulation Item]: https://prod.assistng.org/apidocs/docs/articulation/model/sending#sending-articulation-item-base-model
        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/sending#sending-articulation-course-group)
        '''
        type:               Literal[SendingArticulation.Item.Type.CourseGroup]
        courseConjunction:  SendingArticulation.CourseGroup.Conjunction.Type
        items:              list[Item.Model]

        class Conjunction:
            class Model (Monomorphic):
                '''
                This model composes the defined conjunction for a group of courses on an articulation.
                
                :id:                                The unique id for the course group conjunction
                :sendingArticulationId:             The unique id for the sending articulation id in which this conjunction belongs
                :groupConjunction:                  The conjunction type from `SendingArticulation.CourseGroup.Conjunction.Type`
                :sendingCourseGroupBeginPosition:   The first position in which the conjunction applies
                :sendingCourseGroupEndPosition:     The last position in which the conjunction applies
                
                [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/sending#course-group-conjunction)
                '''
                id:                                 UUID
                sendingArticulationId:              UUID
                groupConjunction:                   SendingArticulation.CourseGroup.Conjunction.Type
                sendingCourseGroupBeginPosition:    int
                sendingCourseGroupEndPosition:      int

            class Type (StrEnum):
                '''
                ```
                SendingArticulation.CourseGroup.Conjunction: And | Or
                ```
                '''
                And = 'And'
                Or  = 'Or'

        class Item:
            class Model (Polymorphic):
                '''
                The model that represents a sending articulation item in a course group. This model is the base model in which other Course Group Items are derived.

                :position:  The position in the array that the sending item should display
                :​type:      The type of sending articulation item from `SendingArticulation.CourseGroup.Item.Type`

                [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/sending#sending-articulation-course-group-item-base-model)
                '''
                position:   int
                type:       SendingArticulation.CourseGroup.Item.Type

            class Type (StrEnum):
                '''
                ```
                SendingArticulation.CourseGroup.Item.Type: Course | Advisement
                ```
                '''
                Course      = 'Course'
                Advisement  = 'Advisement'

        class Course (Item.Model):
            '''
            The model that represents a sending course item in a course group. This model extends [Sending Articulation Course Group Item Base Model][Sending Articulation Course Group Item Base Model] and is the model used when the group item type is `Course`.

            :visibleCrossListedCourses:             The cross listed courses to show the "same as" on the sending articulation
            :requisites:                            The pre-requisite and co-requisite courses associated with this course
            :attributes:                            The attributes associated with this course
            :courseIdentifierParentId:              The unique id of the course in which versions can be derived
            :courseTitle:                           The title of the course
            :courseNumber:                          The course number
            :prefix:                                The prefix
            :prefixParentId:                        The unique id of this course's prefix in which prefix versions can be derived
            :prefixDescription:                     The description of the prefix associated with this course
            :departmentParentId:                    The unique id of this course’s department in which department versions can be derived
            :department:                            The department title
            :begin:                                 The yearTermCode in which this course version becomes active
            :end:                                   The yearTermCode in which this course version ceases to be active. If end is blank then this course version continues indefinitely. If end is populated with a yearTermCode, that could either mean that a future course version continues this course version forward, likely with a revision, or the course is terminated.
            :minUnits:                              The minimum units
            :maxUnits:                              The maximum units
            :publishedCourseIdentifierYearTermId:   The yearTermId that this course version applies to, usually `None` when there's not a midyear revision for the course
            :​type:                                  `SendingArticulation.CourseGroup.Item.Type.Course`

            [Sending Articulation Course Group Item Base Model]: https://prod.assistng.org/apidocs/docs/articulation/model/sending#sending-articulation-course-group-item-base-model
            [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/sending#sending-articulation-course-group-item-course)
            '''
            type:                                   Literal[SendingArticulation.CourseGroup.Item.Type.Course]
            visibleCrossListedCourses:              list[Course.Model]
            requisites:                             list[Requisite.Model]
            attributes:                             list[Attribute.Model]
            courseIdentifierParentId:               int
            courseTitle:                            str
            courseNumber:                           int
            prefix:                                 str
            prefixParentId:                         int
            prefixDescription:                      str
            departmentParentId:                     int
            department:                             str
            begin:                                  str
            end:                                    Optional[str]
            minUnits:                               int
            maxUnits:                               int
            publishedCourseIdentifierYearTermId:    int

        class Advisement (Item.Model):
            '''
            The model that represents a sending advisement in a course group. This model extends [Sending Articulation Course Group Item Base Model][Sending Articulation Course Group Item Base Model] and is the model used when the course group item type is an `Advisement`.

            :advisement:    The advisement object which is polymorphic to the type of advisement it is
            :​type:          `SendingArticulation.CourseGroup.Item.Type.Advisement`

            [Sending Articulation Course Group Item Base Model]: https://prod.assistng.org/apidocs/docs/articulation/model/sending#sending-articulation-course-group-item-base-model
            [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/sending#sending-articulation-course-group-item-advisement)
            '''
            type:       Literal[SendingArticulation.CourseGroup.Item.Type.Advisement]
            advisement: Advisement.Model

    class Advisement (Item.Model):
        '''
        This model extends the [Sending Articulation Item][Sending Articulation Item] if the sending articulation type is an Advisement.

        :advisement:    The advisement object which is polymorphic to the type of advisement it is
        :​type:          `SendingArticulation.Item.Type.Advisement`   
            
        [Sending Articulation Item]: https://prod.assistng.org/apidocs/docs/articulation/model/sending#sending-articulation-item-base-model
        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/sending#sending-articulation-advisement-item)
        '''
        type:       Literal[SendingArticulation.Item.Type.Advisement]
        advisement: Advisement.Model

class SendingTemplateArticulation:
    class Model (Monomorphic):
        '''
        This model represents the template override for sending articulation on template agreements (Major and General Education). Typically, the articulations defined on a template agreements are pulled from existing defined articulations from Department and Prefix Agreements. However, articulation officers have the option to override those articulations with a different articulation on specific Major and General Education agreements. This model represents that override.

        :id:                    The unique id of this override
        :variantIds:            The array of template variant Ids that are associated with this override
        :sendingArticulation:   The Sending Articulation to override the articulation's `sendingArticulation` with
        '''
        id:                     UUID
        variantIds:             list[UUID]
        sendingArticulation:    SendingArticulation.Model