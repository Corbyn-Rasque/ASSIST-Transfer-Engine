from __future__ import annotations

from uuid       import UUID
from enum       import StrEnum
from typing     import ClassVar, Literal, TypeAlias

from api.agreement.attribute        import Attribute
from api.agreement.advisement       import Advisement
from api.agreement.instruction      import Instruction
from api.agreement.series           import Series as BaseSeries
from api.agreement.generaleducation import GeneralEducation as BaseGeneralEducation
from api.course                     import Course as BaseCourse, CourseCellCrosslisted, CourseCellRequisite

from api.types import Monomorphic, Polymorphic

class Transferability:
    class Model (Monomorphic):
        '''
        This model contains the details of a transferability object such as CSUGE, CSUAI, and IGETC.

        :areaType:  The type of transferability area from `Transferability.Area`
        :name:      The name of the transferability
        :code:      The transferability code or short name
        '''
        areaType:   Transferability.Area
        name:       str
        code:       str

    class Area (StrEnum):
        '''
        ```
        Tranferability.Area: CSUGE | CSUAI | IGETC
        ```
        '''
        CSUGE = 'CSUGE'
        CSUAI = 'CSUAI'
        IGETC = 'IGETC'

class _Asset:
    class Model (Polymorphic):
        '''
        The base template asset model in which other types of template assets are derived.

        :position: The position this template asset should appear on the agreement
        :​type: The type of asset from `Asset.Type`.
        '''
        type:       _Asset.Type
        position:   int
        area:       _Asset.Area
 
    class Type (StrEnum): 
        GeneralTitle        = 'GeneralTitle'
        GeneralText         = 'GeneralText'
        RequirementGroup    = 'RequirementGroup'
        RequirementTitle    = 'RequirementTitle'

    class Area (StrEnum):
        General             = 'General'
        Requirements        = 'Requirements'

    class GeneralText (Model):
        '''
        The template asset is general text. This model extends [Template Asset][Template Asset].
        
        :content:   HTML content for the Requirement Title section
        :​type:      `Asset.Type.GeneralText`

        [Template Asset]: https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-asset
        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-general-text)
        '''
        type:       Literal[_Asset.Type.GeneralText]
        content:    str

    class GeneralTitle (Model):
        '''
        The template asset is a requirement title. This model extends [Template Asset][Template Asset].
        
        :content:   The requirement title itself
        :​type:      `Asset.Type.GeneralTitle`

        [Template Asset]: https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-asset
        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-requirement-title)
        '''
        type:       Literal[_Asset.Type.GeneralTitle]
        content:    str

    class RequirementTitle (Model):
        '''
        The template asset is a requirement title. This model extends [Template Asset][Template Asset].
        
        :content:   The requirement title itself
        :​type:      `Asset.Type.RequirementTitle`

        [Template Asset]: https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-asset
        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-requirement-title)
        '''
        type:       Literal[_Asset.Type.RequirementTitle]
        content:    str

class _Item:
    class Model (Polymorphic):
        '''
        The base model for template group items. Other template group items are derived from this model.

        :position:      The position that this template group item should appear in the group
        :​type:          The type of template group item from `Group.Item.Type`
        :attributes:    The attributes associated to this template group item

        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-item)
        '''
        type:       _Item.Type
        position:   int
        attributes: list[Attribute.Model]
    
    class Type (StrEnum):
        Section         = 'Section'
        SectionHeader   = 'SectionHeader'

class _SectionHeader (_Item.Model):
    '''
    This type of group item is `SectionHeader` and extends [Template Group Item][Template Group Item].

    :content:   The section header text itself
    :​type:      `Group.Item.Type.SectionHeader`
    
    [Template Group Item]: https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-item
    [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-item-section-header)
    '''
    type:       Literal[_Item.Type.SectionHeader]
    content:    str

class _Section (_Item.Model):
    '''
    This type of group item is `Section` and extends [Template Group Item][Template Group Item].
    
    :id:            *undocumented*
    :rows:          The section rows which belong to this template group item
    :advisements:   The advisements associated with this template group item
    :​type:          `Group.Item.Type.SectionHeader`

    [Template Group Item]: https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-item
    [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-item-section)
    '''
    id:         UUID
    type:       Literal[_Item.Type.Section]
    rows:       list[_Section.Row.Model]
    attributes: list[Attribute.Model]

    class Cell:
        class Model (Polymorphic):
            '''
            This is the base model for Template Group Section Cells. The other cell types derive from this model.

            :position:      The position this cell should appear on the section row
            :attributes:    The attributes associated to this cell
            :​type:          The type of cell from `Group.Section.Cell.Type`

            [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-section-cell)
            '''
            type:       _Section.Cell.Type
            position:   int
            attributes: list[Attribute.Model]
            
        class Type (StrEnum):
            '''
            ```
            Group.Section.Cell.Type: Course | Series | Requirement | GeneralEducation | CSUGE | CSUAI | IGETC
            ```
            '''
            Course              = 'Course'
            Series              = 'Series'
            Requirement         = 'Requirement'
            GeneralEducation    = 'GeneralEducation'
            CSUGE               = 'CSUGE'
            CSUAI               = 'CSUAI'
            IGETC               = 'IGETC'

    class Course (Cell.Model):
        '''
        This type of cell is a `Course`. This model extends [Template Group Section Cell][Template Group Section Cell].
        
        :course:                    The course object of this cell
        :visibleCrossListedCourses: The cross listed courses for this course
        :requisites:                The pre-requisite and co-requisite courses associated with this course
        :courseAttributes:          The attributes associated to the course in this cell
        :​type:                      `Group.Section.Cell.Type.Course`

        [Template Group Section Cell]: https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-section-cell
        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-section-course-cell)
        '''
        type:                       Literal[_Section.Cell.Type.Course]
        course:                     BaseCourse.Model
        visibleCrossListedCourses:  list[CourseCellCrosslisted.Model]
        requisites:                 list[CourseCellRequisite.Model]
        courseAttributes:           list[Attribute.Model]

    class Series (Cell.Model):
        '''
        This type of cell is a `Series`. This model extends [Template Group Section Cell][Template Group Section Cell].

        :series:                    Details about the series
        :requisites:                PreRequisites and CoRequisites which belong to a course in the series
        :visibleCrossListedCourses: The array of cross listed courses which belong to a course in the series
        :seriesAttributes:          The array of attributes that apply to the series as a whole
        :courseAttributes:          An array of attributes apply to a specific course on the series
        :​type:                      `Group.Section.Cell.Type.Series`
        
        [Template Group Section Cell]: https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-section-cell
        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-section-series-cell)
        '''
        type:                       Literal[_Section.Cell.Type.Series]
        series:                     BaseSeries.Model
        requisites:                 list[BaseSeries.Cell.Requisite.Model]
        visibleCrossListedCourses:  list[BaseSeries.Cell.Crosslisted.Model]
        seriesAttributes:           list[Attribute.Model]
        courseAttributes:           list[BaseSeries.Attribute.Model]

    class GeneralEducation (Cell.Model):
        '''
        This type of cell is a `GeneralEducation`. This model extends [Template Group Section Cell][Template Group Section Cell].
        
        :generalEducationArea:              Details about the receiving general education area in this cell
        :generalEducationAreaAttributes:    The attributes associated with this general education area
        :​type:                              `Group.Section.Cell.Type.GeneralEducation`

        [Template Group Section Cell]: https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-section-cell
        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-section-general-education-cell)
        '''
        type:                           Literal[_Section.Cell.Type.GeneralEducation]
        generalEducationArea:           BaseGeneralEducation
        generalEducationAreaAttributes: list[Attribute]

    class CSUGE (Cell.Model):
        '''
        This type of cell is a `CSUGE`. This model extends [Template Group Section Cell][Template Group Section Cell].

        :csuge: The CSUGE transferability model
        :​type:  `Group.Section.Cell.Type.CSUGE`
        
        [Template Group Section Cell]: https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-section-cell
        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-section-csuge-cell)
        '''
        type:           Literal[_Section.Cell.Type.CSUGE]
        csuge:          Transferability

    class CSUAI (Cell.Model):
        '''
        This type of cell is a `CSUAI`. This model extends [Template Group Section Cell][Template Group Section Cell].

        :csuai: The CSUAI transferability model
        :​type:  `Group.Section.Cell.Type.CSUGE`
        
        [Template Group Section Cell]: https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-section-cell
        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-section-csuai-cell)
        '''
        type:           Literal[_Section.Cell.Type.CSUAI]
        csuai:          Transferability

    class IGETC (Cell.Model):
        '''
        This type of cell is a `IGETC`. This model extends [Template Group Section Cell][Template Group Section Cell].

        :igetc: The IGETC transferability model
        :​type:  `Group.Section.Cell.Type.IGETC`
        
        [Template Group Section Cell]: https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-section-cell
        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-section-igetc-cell)
        '''
        type:           Literal[_Section.Cell.Type.IGETC]
        igetc:          Transferability

    class Row:
        class Model (Monomorphic):
            '''
            This model represents the section row on a template group.

            :position:      The position that this section row should appear in the template row item section
            :cells:         The cells associated to this section row which is polymorphic to the type of cell it is
            :attributes:    The attributes associated to this section row

            [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-section-row)
            '''
            position:   int
            cells:      list[_Section.Cell.Model]
            attributes: list[Attribute.Model]

class _Group (_Asset.Model):
    '''
    The template asset is a requirement group. This model extends [Template Asset][Template Asset].

    :hideSectionLetters: 
    :​type:     `Asset.Type.RequirementGroup`

    [Template Asset]: https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-asset
    [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group)
    '''
    type:                           Literal[_Asset.Type.RequirementGroup]
    hideSectionLetters:             bool
    sections:                       list[_Item.Model]
    attributes:                     list[Attribute.Model]
    showConjunctionBetweenSections: bool
    instruction:                    Instruction.Model
    advisements:                    list[Advisement.Model]

    Item:           ClassVar[TypeAlias] = _Item
    SectionHeader:  ClassVar[TypeAlias] = _SectionHeader
    Section:        ClassVar[TypeAlias] = _Section

# This class exists for a clean, navigable structure that avoids foward reference issues.
class Asset (_Asset):
    class Group(_Group):
        Item:       ClassVar[TypeAlias] = _Item
        Section:    ClassVar[TypeAlias] = _Section

class PublishedAgreementAsset:
    class Model (Monomorphic):
        '''
        This model represents a template asset for “All” Agreements. This model is used to represent the individual agreements that make up the “All” agreement.

        :name:      The name of the agreement (usually a major or a GE)
        :assets:    The template assets on the agreement.
        '''
        name:   str
        assets: list[_Asset.Model]

_Item.Model.model_rebuild()
_Section.model_rebuild()
_Section.Row.Model.model_rebuild()
_Group.model_rebuild()
_Asset.Model.model_rebuild()
PublishedAgreementAsset.Model.model_rebuild()