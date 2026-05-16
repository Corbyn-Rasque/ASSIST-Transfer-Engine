from __future__ import annotations

from enum       import StrEnum
from typing     import Literal, TypeAlias

from api.types      import Polymorphic

class Advisement:
    class Model (Polymorphic):
        '''
        The advisement model can be composed on various places on the articulation. This is the base advisement model from which other advisement types are derived.

        :position:      The position in the array that the advisement should display
        :Type:          The type of advisement from the `AdvisementBasemodel.Type` enum.
        :selectionType: The type of selection for the advisement from the `Advisment.Selection` enum.
        <!-- :type:     The type of advisement from the `AdvisementBasemodel.Type` enum.
        -->

        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/advisement#advisement-base-model)
        '''
        position:       int
        type:           Advisement.Type
        selectionType:  Advisement.Selection

    class Type (StrEnum):
        '''
        ```
        Advisement.Type : NInNDifferentAreas | NInAnyNAreas | AdditionalNToReach | NFromUnits | NFollowing | NToNFollowing
        ```
        '''
        NInNDifferentAreas  = 'NInNDifferentAreas'
        NInAnyNAreas        = 'NInAnyNAreas'
        AdditionalNToReach  = 'AdditionalNToReach'
        NFromUnits          = 'NFromUnits'
        NFollowing          = 'NFollowing'
        NToNFollowing       = 'NToNFollowing'

    class Selection (StrEnum):
        '''
        ```
        Advisement.Selection : Select | Complete | Include
        ```
        '''
        Select      = 'Select'
        Complete    = 'Complete'
        Include     = 'Include'

    class Unit:
        class Type (StrEnum):
            '''
            ```
            Advisement.Unit.Type: Course | Unit | Series | Sequence | Semester | SemesterUnit | Quarter | QuarterUnit | Trimester | TrimesterUnit | CourseOrCombinatino | Row | OrMoreCourses | OrMoreUnits
            ```
            '''
            Course              = 'Course'
            Unit                = 'Unit'
            Series              = 'Series'
            Sequence            = 'Sequence'
            Semester            = 'Semester'
            SemesterUnit        = 'SemesterUnit'
            Quarter             = 'Quarter'
            QuarterUnit         = 'QuarterUnit'
            Trimester           = 'Trimester'
            TrimesterUnit       = 'TrimesterUnit'
            CourseOrCombination = 'CourseOrCombination'
            Row                 = 'Row'
            OrMoreCourses       = 'OrMoreCourses'
            OrMoreUnits         = 'OrMoreUnits'

    class Area:
        class Type (StrEnum):
            '''
            ```
            Advisement.Area.Type: none | Areas | Concentrations | Emphases | Specializations
            ```
            '''
            none            = 'None'
            Areas           = 'Areas'
            Concentrations  = 'Concentrations'
            Emphases        = 'Emphases'
            Specializations = 'Specializations'

    Quantifier: TypeAlias = Unit.Type

class CompleteAdditionalUnits (Advisement.Model):
    '''
    This model represents a sub instruction to complete additional units to reach N total.

    :amount:    The amount of additional units needed to reach
    :​type:      Advisement.Type.AdditionalNToReach

    [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/advisement#complete-additional-units-advisement)
    '''
    type:   Literal[Advisement.Type.AdditionalNToReach]
    amount: int

class NInAnyNAreas (Advisement.Model):
    '''
    This model represents a sub instruction for selecting N Course(s)/Unit(s) from any N of the following area(s). Extends [Advisement Model][Advisement].

    :amount:            The N amount
    :amountUnitType:    The type of unit for the amount from [Course, Unit, Series, Sequence, Semester, SemesterUnit, Quarter, QuarterUnit, Trimester, TrimesterUnit, CourseOrCombination, Row, OrMoreCourses, OrMoreUnits]
    :areaAmount:        The area amount
    'areaType:          The type of unit for the area from [None, Areas, Concentrations, Emphases, Specializations]
    :​type:              `Advisement.Type.NInAnyNAreas`

    [Advisement]: https://prod.assistng.org/apidocs/docs/articulation/model/advisement#advisement-base-model
    [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/advisement#n-in-any-n-areas-advisement)
    '''
    type:           Literal[Advisement.Type.NInAnyNAreas]
    amount:         int
    amountUnitType: Advisement.Unit.Type
    areaAmount:     int
    areaType:       Advisement.Area.Type

class NInNDifferentAreas (Advisement.Model):
    '''
    This model represents a sub instruction for selecting N course(s)/Unit(s) in N area(s). Extends [Advisement Model][Advisement].

    :amount:            The N amount
    :amountUnitType:    The type of unit for the amount from [Course, Unit, Series, Sequence, Semester, SemesterUnit, Quarter, QuarterUnit, Trimester, TrimesterUnit, CourseOrCombination, Row, OrMoreCourses, OrMoreUnits]
    :areaAmount:        The area amount
    'areaType:          The type of unit for the area from [None, Areas, Concentrations, Emphases, Specializations]
    :​type:              `Advisement.Type.NInNDifferentAreas`

    [Advisement]: https://prod.assistng.org/apidocs/docs/articulation/model/advisement#advisement-base-model
    [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/advisement#n-in-n-different-areas-advisement)
    '''
    type:           Literal[Advisement.Type.NInNDifferentAreas]
    amount:         int
    amountUnitType: Advisement.Unit.Type
    areaAmount:     int
    areaType:       Advisement.Area.Type

class NFromUnits (Advisement.Model):
    '''
    This model represents a sub instruction for selecting at least N course(s)/Unit(s) from this section. Extends [Advisement Model][Advisement].

    :amount:            The N amount
    :amountQuantifier:  The amount quantifier type from [None, UpTo, AtLeast]
    :amountUnitType:    The type of unit for the amount from [Course, Unit, Series, Sequence, Semester, SemesterUnit, Quarter, QuarterUnit, Trimester, TrimesterUnit, CourseOrCombination, Row, OrMoreCourses, OrMoreUnits]
    :​type:              `Advisement.Type.NFromUnits`
    
    [Advisement]: https://prod.assistng.org/apidocs/docs/articulation/model/advisement#advisement-base-model
    [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/advisement#n-from-units-advisement)
    '''
    type:               Literal[Advisement.Type.NFromUnits]
    amount:             int
    amountQuantifier:   Advisement.Quantifier
    amountUnitType:     Advisement.Unit.Type

class NFollowing (Advisement.Model):
    '''
    This model represents a sub instruction for selecting N course(s)/Unit(s) from the following. Extends [Advisement Model][Advisement].

    :amount:            The N amount
    :amountUnitType:    The type of unit for the amount from [Course, Unit, Series, Sequence, Semester, SemesterUnit, Quarter, QuarterUnit, Trimester, TrimesterUnit, CourseOrCombination, Row, OrMoreCourses, OrMoreUnits]
    :​type:              `Advisement.Type.NFollowing`

    [Advisement]: https://prod.assistng.org/apidocs/docs/articulation/model/advisement#advisement-base-model
    [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/advisement#n-following-advisement)
    '''
    type:               Literal[Advisement.Type.NFollowing]
    amount:             int
    amountUnitType:     Advisement.Unit.Type

class NToNFollowing (Advisement.Model):
    '''
    This model represents a sub instruction for selecting N to N course(s)/Unit(s) from the following. Extends [Advisement Model][Advisement].

    :fromAmount:        The minimum amount
    :toAmount:          The maximum amount
    :unitType:          The type of unit for the amount from [Course, Unit, Series, Sequence, Semester, SemesterUnit, Quarter, QuarterUnit, Trimester, TrimesterUnit, CourseOrCombination, Row, OrMoreCourses, OrMoreUnits]
    :​type:              `Advisement.Type.NToNFollowing`

    [Advisement]: https://prod.assistng.org/apidocs/docs/articulation/model/advisement#advisement-base-model
    [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/advisement#n-to-n-following-advisement)
    '''
    type:               Literal[Advisement.Type.NToNFollowing]
    fromAmount:         int
    toAmount:           int
    unitType:           Advisement.Unit.Type