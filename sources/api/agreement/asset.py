from __future__ import annotations

from uuid       import UUID
from enum       import StrEnum
from typing     import TYPE_CHECKING, ClassVar, Literal, TypeAlias

from sources.api.agreement.attribute        import Attribute
from sources.api.agreement.advisement       import Advisement
from sources.api.agreement.instruction      import Instruction
from sources.api.agreement.series           import Series as BaseSeries
from sources.api.agreement.generaleducation import GeneralEducation as BaseGeneralEducation
from sources.api.agreement.requirement      import Requirement as BaseRequirement
from sources.api.course                     import Course as BaseCourse

from sources.api.types import Monomorphic, Polymorphic, Models

class _Transferability:
    class Model (Monomorphic):
        '''
        This model contains the details of a transferability object such as CSUGE, CSUAI, and IGETC.

        :areaType:  The type of transferability area from `Transferability.Area`
        :name:      The name of the transferability
        :code:      The transferability code or short name

        [Documentatation](https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#transferability-model)
        '''
        areaType:   _Transferability.Area
        name:       str
        code:       str

    class Area (StrEnum):
        '''
        ```
        Tranferability.Area: CSUGE | CSUAI | IGETC | CALGETC
        ```
        '''
        CSUGE   = 'CSUGE'
        CSUAI   = 'CSUAI'
        IGETC   = 'IGETC'
        CALGETC = 'CALGETC' # Added per web scraper

class _Asset (Models):
    class Models: pass

    class Model (Polymorphic):
        '''
        The base template asset model in which other types of template assets are derived.

        :position:  The position this template asset should appear on the agreement
        :area:      The area on an Articulation Template from `Asset.Area`. Certain elements are only allowed to be placed in some areas
        :​type:      The type of asset from `Asset.Type`.

        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-asset)
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

    class GeneralText (Model, Models):
        '''
        The template asset is general text. This model extends [Template Asset][Template Asset].
        
        :content:   HTML content for the Requirement Title section
        :​type:      `Asset.Type.GeneralText`

        [Template Asset]: https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-asset
        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-general-text)
        '''
        type:       Literal[_Asset.Type.GeneralText] # type: ignore[assignment]
        content:    str

    class GeneralTitle (Model, Models):
        '''
        The template asset is a requirement title. This model extends [Template Asset][Template Asset].
        
        :content:   The requirement title itself
        :​type:      `Asset.Type.GeneralTitle`

        [Template Asset]: https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-asset
        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-requirement-title)
        '''
        type:       Literal[_Asset.Type.GeneralTitle] # type: ignore[assignment]
        content:    str

    class RequirementTitle (Model, Models):
        '''
        The template asset is a requirement title. This model extends [Template Asset][Template Asset].
        
        :content:   The requirement title itself
        :​type:      `Asset.Type.RequirementTitle`

        [Template Asset]: https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-asset
        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-requirement-title)
        '''
        type:       Literal[_Asset.Type.RequirementTitle] # type: ignore[assignment]
        content:    str

class _Item (Models):
    class Models: pass

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

    Transferability:        ClassVar[TypeAlias] = _Transferability

class _SectionHeader (_Item.Model, _Item.Models):
    '''
    This type of group item is `SectionHeader` and extends [Template Group Item][Template Group Item].

    :content:   The section header text itself
    :​type:      `Group.Item.Type.SectionHeader`
    
    [Template Group Item]: https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-item
    [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-item-section-header)
    '''
    type:       Literal[_Item.Type.SectionHeader] # type: ignore[assignment]
    content:    str

class _Section (_Item.Model, _Item.Models):
    '''
    This type of group item is `Section` and extends [Template Group Item][Template Group Item].
    
    :id:            *undocumented*
    :rows:          The section rows which belong to this template group item
    :advisements:   The advisements associated with this template group item
    :​type:          `Group.Item.Type.SectionHeader`

    [Template Group Item]: https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-item
    [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-item-section)
    '''
    type:       Literal[_Item.Type.Section] # type: ignore[assignment]
    rows:       list[_Section.Row.Model]
    attributes: list[Attribute.Model]

    class Cell (Models):
        class Models: pass

        class Model (Polymorphic):
            '''
            This is the base model for Template Group Section Cells. The other cell types derive from this model.

            :id:            [ Undocumented, found in example JSON ]
            :position:      The position this cell should appear on the section row
            :attributes:    The attributes associated to this cell
            :​type:          The type of cell from `Group.Section.Cell.Type`

            [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-section-cell)
            '''
            id:         UUID
            type:       _Section.Cell.Type
            position:   int
            attributes: list[Attribute.Model]
            
        class Type (StrEnum):
            '''
            ```
            Group.Section.Cell.Type: Course | Series | Requirement | GeneralEducation | CSUGE | CSUAI | IGETC | CALGETC
            ```
            '''
            Course              = 'Course'
            Series              = 'Series'
            Requirement         = 'Requirement'
            GeneralEducation    = 'GeneralEducation'
            CSUGE               = 'CSUGE'
            CSUAI               = 'CSUAI'
            IGETC               = 'IGETC'
            CALGETC             = 'CALGETC' # Added per web scraper

    class Course (Cell.Model, Cell.Models):
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
        type:                       Literal[_Section.Cell.Type.Course] # type: ignore[assignment]
        course:                     BaseCourse.Model
        visibleCrossListedCourses:  list[BaseCourse.Cell.Crosslisted.Model]
        requisites:                 list[BaseCourse.Cell.Requisite.Model]
        courseAttributes:           list[Attribute.Model]

    class Series (Cell.Model, Cell.Models):
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
        type:                       Literal[_Section.Cell.Type.Series] # type: ignore[assignment]
        series:                     BaseSeries.Model
        requisites:                 list[BaseSeries.Cell.Requisite.Model]
        visibleCrossListedCourses:  list[BaseSeries.Cell.Crosslisted.Model]
        seriesAttributes:           list[Attribute.Model]
        courseAttributes:           list[BaseSeries.Attribute.Model]

    class GeneralEducation (Cell.Model, Cell.Models):
        '''
        This type of cell is a `GeneralEducation`. This model extends [Template Group Section Cell][Template Group Section Cell].
        
        :generalEducationArea:              Details about the receiving general education area in this cell
        :generalEducationAreaAttributes:    The attributes associated with this general education area
        :​type:                              `Group.Section.Cell.Type.GeneralEducation`

        [Template Group Section Cell]: https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-section-cell
        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-section-general-education-cell)
        '''
        type:                           Literal[_Section.Cell.Type.GeneralEducation] # type: ignore[assignment]
        generalEducationArea:           BaseGeneralEducation.Model
        generalEducationAreaAttributes: list[Attribute.Model]

    class CSUGE (Cell.Model, Cell.Models):
        '''
        This type of cell is a `CSUGE`. This model extends [Template Group Section Cell][Template Group Section Cell].

        :csuge: The CSUGE transferability model
        :​type:  `Group.Section.Cell.Type.CSUGE`
        
        [Template Group Section Cell]: https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-section-cell
        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-section-csuge-cell)
        '''
        type:           Literal[_Section.Cell.Type.CSUGE] # type: ignore[assignment]
        csuge:          _Transferability.Model

    class CSUAI (Cell.Model, Cell.Models):
        '''
        This type of cell is a `CSUAI`. This model extends [Template Group Section Cell][Template Group Section Cell].

        :csuai: The CSUAI transferability model
        :​type:  `Group.Section.Cell.Type.CSUGE`
        
        [Template Group Section Cell]: https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-section-cell
        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-section-csuai-cell)
        '''
        type:           Literal[_Section.Cell.Type.CSUAI] # type: ignore[assignment]
        csuai:          _Transferability.Model

    class IGETC (Cell.Model, Cell.Models):
        '''
        This type of cell is a `IGETC`. This model extends [Template Group Section Cell][Template Group Section Cell].

        :igetc: The IGETC transferability model
        :​type:  `Group.Section.Cell.Type.IGETC`
        
        [Template Group Section Cell]: https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-section-cell
        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-section-igetc-cell)
        '''
        type:           Literal[_Section.Cell.Type.IGETC] # type: ignore[assignment]
        igetc:          _Transferability.Model

    class CALGETC (Cell.Model, Cell.Models):
        '''
        This type of cell is a `CALGETC`. This model extends [Template Group Section Cell][Template Group Section Cell]. Not yet in the API documentation; added per web scraper.

        :calgetc:   The Cal-GETC transferability model
        :​type:      `Group.Section.Cell.Type.CALGETC`

        [Template Group Section Cell]: https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-section-cell
        '''
        type:           Literal[_Section.Cell.Type.CALGETC] # type: ignore[assignment]
        calgetc:        _Transferability.Model

    class Requirement (Cell.Model, Cell.Models):
        '''
        This type of cell is a `Requirement`. This model extends [Template Group Section Cell][Template Group Section Cell].

        :requirement:           The campus requirement
        :requirementAttributes: An array of attributes associated with the requirement
        :​type:                  `Group.Section.Cell.Type.Requirement`

        [Template Group Section Cell]: https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group-section-cell
        '''
        type:                   Literal[_Section.Cell.Type.Requirement] # type: ignore[assignment]
        requirement:            BaseRequirement.Model
        requirementAttributes:  list[Attribute.Model]

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
            cells:      list[_SectionCells] # Course | Series | ..., resolved below once all cell types are defined
            attributes: list[Attribute.Model]

class _Group (_Asset.Model, _Asset.Models):
    '''
    The template asset is a requirement group. This model extends [Template Asset][Template Asset].

    :hideSectionLetters: 
    :​type:     `Asset.Type.RequirementGroup`

    [Template Asset]: https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-asset
    [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-group)
    '''
    type:                           Literal[_Asset.Type.RequirementGroup]  # type: ignore[assignment]
    hideSectionLetters:             bool
    sections:                       list[_GroupItems] # Section | SectionHeader, resolved below once both are defined
    attributes:                     list[Attribute.Model]
    showConjunctionBetweenSections: bool
    instruction:                    Instruction.Model | None
    advisements:                    list[Advisement.Models]

    Item:           ClassVar[TypeAlias] = _Item
    SectionHeader:  ClassVar[TypeAlias] = _SectionHeader
    Section:        ClassVar[TypeAlias] = _Section

# This class exists for a clean, navigable structure that avoids foward reference issues.
class Asset (_Asset):
    Group = _Group

Asset.Models                    = _Asset.annotated()                    # type: ignore[assignment]
Asset.Group.Item.Models         = _Item.annotated()                     # type: ignore[assignment]
Asset.Group.Section.Cell.Models = Asset.Group.Section.Cell.annotated()  # type: ignore[assignment]

# Resolve the forward references in `_Group.sections` and `_Section.Row.Model.cells`
if TYPE_CHECKING:
    _GroupItems:    TypeAlias = _SectionHeader | _Section
    _SectionCells:  TypeAlias = (_Section.Course | _Section.Series | _Section.GeneralEducation | _Section.CSUGE
                                 | _Section.CSUAI | _Section.IGETC | _Section.CALGETC | _Section.Requirement)
else:
    _GroupItems   = Asset.Group.Item.Models
    _SectionCells = Asset.Group.Section.Cell.Models

_Item.Model.model_rebuild()
_Section.model_rebuild()
_Section.Row.Model.model_rebuild()
_Group.model_rebuild()
_Asset.Model.model_rebuild()

class PublishedAgreement:
    class Model (Monomorphic):
        '''
        This model represents a template asset for “All” Agreements. This model is used to represent the individual agreements that make up the “All” agreement.

        :name:      The name of the agreement (usually a major or a GE)
        :assets:    The template assets on the agreement.
        '''
        name:           str
        templateAssets: list[Asset.Models]

PublishedAgreement.Model.model_rebuild()