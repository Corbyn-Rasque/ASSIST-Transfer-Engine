from __future__ import annotations

from datetime   import datetime
from enum       import StrEnum

from api.types import Monomorphic

class Agreement:
    class Model (Monomorphic):
        '''
        The published agreement data model composes many JSON object strings. The objects are meant to serve as a snapshot in time of the captured articulations between two institutions at the time of publishing. Depending on the agreement type, the `articulations` and `templateAssets` JSON strings will contain different types of data. The details are below.

        :name:                  The name of the agreement
        :​type:                  The type of agreement from `Agreement.Type`  
        :publishDate:           The date and time when the articulation was published
        :receivingInstitution:  The **JSON string** of an [Institution][Institution], the receiving institution in the agreement
        :sendingInstitution:    The **JSON string** of an [Institution][Institution], the sending institution in the agreement
        :academicYear:          The **JSON string** of an [Academic Year][Academic Year] for this agreement
        :templateAssets:        The **JSON string** of [Template Asset][Template Asset], only populated when the agreement is a Major or General Education. For “All” agreements (i.e. All Majors), the type is [Published Agreement Template Assets][Published Agreement Template Assets] instead
        :articulations:         The **JSON string** of an array of articulations in the agreement. For Department and Prefix agreements, the type articulation is the [Base Articulation Model][Base Articulation Model]. For Major and General Education agreements, the type of articulation is [Template Cell Articulation Model][Template Cell Articulation Model] instead.
        :catalogYear:           The **JSON string** an object representing the catalog year for both receiving and sending institutions
        
        [Institution]: https://prod.assistng.org/apidocs/docs/institutions/get#institution-model  
        [Academic Year]: https://prod.assistng.org/apidocs/docs/acadmicyears/get#academic-year-model
        [Template Asset]: https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#template-asset
        [Published Agreement Template Assets]: https://prod.assistng.org/apidocs/docs/articulation/model/template-assets#published-agreement-template-asset
        [Template Cell Articulation Model]: https://prod.assistng.org/apidocs/docs/articulation/model/templates#template-cell-articulation-model
        [Base Articulation Model]: https://prod.assistng.org/apidocs/docs/articulation/model/receiving#base-articulation-model

        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model#published-agreement-data-model)
        '''
        name:                   str
        type:                   Agreement.Type
        publishDate:            datetime
        receivingInstitution:   str
        sendingInstitution:     str
        academicYear:           str
        templateAssets:         str
        articulations:          str
        catalogYear:            str

    class Type (StrEnum):
        '''
        ```
        Agreement.Type: Major | Department | Prefix | GeneralEducation
        ```
        '''
        Major               = 'Major'
        Department          = 'Department'
        Prefix              = 'Prefix'
        GeneralEducation    = 'GeneralEducation'