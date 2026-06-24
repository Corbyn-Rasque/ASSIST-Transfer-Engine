from __future__ import annotations

from enum       import StrEnum
from typing     import Literal

from sources.api.agreement.attribute        import Attribute
from sources.api.course                     import Course as BaseCourse
from sources.api.agreement.series           import Series as BaseSeries
from sources.api.agreement.requirement      import Requirement as BaseRequirement
from sources.api.agreement.generaleducation import GeneralEducation as BaseGeneralEducation
from sources.api.agreement.sending          import SendingArticulation, SendingTemplateArticulation

from sources.api.types import Polymorphic, Models

class ReceivingArticulation (Models):
    class Model (Polymorphic):
        '''
        The base articulation model represents the articulation details from which articulation types are derived.
         
        :sendingArticulation:  The sending side details of this articulation. For `Major` and `General Education` agreements, this object can be overridden or replaced with `templateOverrides`
        :templateOverrides:     The template overrides which composes a `sendingArticulation` object in which to replace this model's `sendingArticulation` with, when present (only applicable to `Major` and `General Education`)
        :attributes:            Row-level attributes that apply to both sides of the articulation instance
        :receivingAttributes:   Cell-level attribute that apply to the receiving side of the articulation instance
        :​type:                  Indicates the type of receiving articulation from `Articulation.Type`    

        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/receiving#base-articulation-model)
        '''
        type:                   ReceivingArticulation.Type
        sendingArticulation:    SendingArticulation.Model | None     = None
        templateOverrides:      list[SendingTemplateArticulation.Model] | None = None
        attributes:             list[Attribute.Model] | None         = None
        receivingAttributes:    list[Attribute.Model] | None         = None

    class Type (StrEnum):
        Course              = 'Course'
        Series              = 'Series'
        Requirement         = 'Requirement'
        GeneralEducation    = 'GeneralEducation'
        Transferability     = 'Transferability'

class Course (ReceivingArticulation.Model):
    '''
    The receiving articulation is a single course. This model extends [Base Articulation][Base Articulation].

    :course:                    The course object
    :visibleCrossListedCourses: An array of courses that are cross-listed with the receiving course to show “Same as” on the articulation
    :courseAttributes:          An array of attributes associated with the course
    :​type:                      `Articulation.Type.Course`

    [Base Articulation]: https://prod.assistng.org/apidocs/docs/articulation/model/receiving#base-articulation-model
    [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/receiving#course-articulation)
    '''
    type:                       Literal[ReceivingArticulation.Type.Course]
    course:                     BaseCourse.Model
    visibleCrossListedCourses:  list[BaseCourse.Model] | None = None
    courseAttributes:           list[Attribute.Model] | None = None

class Series (ReceivingArticulation.Model):
    '''
    The receiving articulation is a series of courses. This model extends [Base Articulation][Base Articulation].

    :series:                    Details about the receiving series
    :visibleCrossListedCourses: An array of courses that are cross-listed with a specific course in the series
    :courseAttributes:          An array of attributes apply to a specific course on the series
    :seriesAttributes:          An array of attributes that apply to the series as a whole
    :​type:                      `Articulation.Type.Series`

    [Base Articulation]: https://prod.assistng.org/apidocs/docs/articulation/model/receiving#base-articulation-model
    [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/receiving#series-articulation)
    '''
    type:                       Literal[ReceivingArticulation.Type.Series]
    series:                     BaseSeries.Model
    visibleCrossListedCourses:  list[BaseSeries.Crosslisted.Model] | None = None
    courseAttributes:           list[BaseSeries.Attribute.Model] | None = None
    seriesAttributes:           list[Attribute.Model] | None = None

class Requirement (ReceivingArticulation.Model):
    '''
    The receiving articulation is a campus requirement. This model extends [Base Articulation][Base Articulation].

    :requirement:           Details about the receiving requirement
    :requirementAttributes: An array of attributes associated with the requirement
    :​type:                  `Articulation.Type.Requirement`

    [Base Articulation]: https://prod.assistng.org/apidocs/docs/articulation/model/receiving#base-articulation-model
    [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/receiving#requirement-articulation)
    '''
    type:                   Literal[ReceivingArticulation.Type.Requirement]
    requirement:            BaseRequirement.Model
    requirementAttributes:  list[Attribute.Model]

class GeneralEducation (ReceivingArticulation.Model):
    '''
    The receiving articulation is a Campus-based GE. This model extends [Base Articulation][Base Articulation].

    :generalEducationArea:              Details about the receiving general education area
    :generalEducationAreaAttributes:    An array of attributes associated with the general education area
    :​type:                              `Articulation.Type.GeneralEducation`
    
    [Base Articulation]: https://prod.assistng.org/apidocs/docs/articulation/model/receiving#base-articulation-model
    [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/receiving#generaleducation-articulation)
    '''
    type:                           Literal[ReceivingArticulation.Type.GeneralEducation]
    generalEducationArea:           BaseGeneralEducation.Model
    generalEducationAreaAttributes: list[Attribute.Model]

class Transferability (ReceivingArticulation.Model):
    '''
    The receiving articulation is a transferability area (CSUGE, CSUAI, or IGETC). This model extends [Base Articulation][Base Articulation]. This type of articulation has no additional fields and can only be added as a template asset for Major and General Education agreements.

    :​type:                  Indicates the type of receiving articulation from `Articulation.Type`  

    [Base Articulation]: https://prod.assistng.org/apidocs/docs/articulation/model/receiving#base-articulation-model
    [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/receiving#transferability-articulation)
    '''
    type:   Literal[ReceivingArticulation.Type.Transferability]

ReceivingArticulation.Models = ReceivingArticulation.annotated()