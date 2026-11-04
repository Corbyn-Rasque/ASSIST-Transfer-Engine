import json
from enum                           import StrEnum
from pydantic                       import TypeAdapter

from sources.web.scraper            import Scraper

from sources.web.courses            import List as CourseList
from sources.web.institution        import Institution
from sources.web.agreements         import Agreement, Result, Reports, List as AgreementList
from sources.web.transferrability   import Availability, Area, Categories
from sources.web.year               import Year


ROOT    = 'https://assist.org/'
API     = ROOT + 'api/'

class Endpoint (StrEnum):
    AREAS           = API + 'transferability/areaTypes'
    COURSES         = API + 'transferability/courses'
    INSTITUTIONS    = API + 'institutions'
    AGREEMENTS      = API + 'articulation/Agreements'
    REPORTS         = API + 'agreements'
    CATEGORIES      = API + 'agreements/categories'
    YEARS           = API + 'AcademicYears'

class Request:
    scraper: Scraper

    def __init__(self):
        self.scraper = Scraper(ROOT)

    def areas(self) -> list[Area]:
        response = self.scraper.get(Endpoint.AREAS)
        return TypeAdapter(list[Area]).validate_json(response)

    def courses(self, 
                institutionId:              int, 
                academicYearId:             int, 
                listType:                   CourseList.Type
                ) -> CourseList:
        
        response = self.scraper.get(Endpoint.COURSES, params = {
            'institutionId':    institutionId,
            'academicYearId':   academicYearId,
            'listType':         listType.name,
        })
        return TypeAdapter(CourseList).validate_json(response)
    
    def institutions(self) -> list[Institution]:
        response = self.scraper.get(Endpoint.INSTITUTIONS)
        return TypeAdapter(list[Institution]).validate_json(response)

    def agreement(self, 
                  academicYearId:           int, 
                  sendingInstitutionId:     int, 
                  receivingInstitutionId:   int, 
                  agreement:                Agreement.Type,
                  filter:                   int | None = None
                  ) -> Result:
        
        response = self.scraper.get(Endpoint.AGREEMENTS + \
            f'?Key={academicYearId}/{receivingInstitutionId}/to/{sendingInstitutionId}/{agreement}{f'/{filter}' if filter else ''}'
        )
        data = json.loads(response)
        if isinstance(data['result']['articulations'], str):
            data['result']['articulations'] = json.loads(data['result']['articulations'])

        return TypeAdapter(Result).validate_python(data)

    def agreements(self, 
                   sendingInstitutionId: int
                   ) -> list[AgreementList]:
        
        response = self.scraper.get(Endpoint.INSTITUTIONS + \
            f'/{sendingInstitutionId}/agreements'
        )
        return TypeAdapter(list[AgreementList]).validate_json(response)

    def transferrability(self,
                         sendingInstitutionId: int
                         ) -> Availability:
        
        response = self.scraper.get(Endpoint.INSTITUTIONS + \
            f'/{sendingInstitutionId}/transferability/availableAcademicYears'
        )
        return TypeAdapter(Availability).validate_json(response)

    def reports(self, 
                receivingInstitutionId:     int, 
                sendingInstitutionId:       int, 
                academicYearId:             int, 
                categoryCode:               Reports.Type
                ) -> Reports:
        
        response = self.scraper.get(Endpoint.REPORTS, params = {
            'receivingInstitutionId':   receivingInstitutionId,
            'sendingInstitutionId':     sendingInstitutionId,
            'academicYearId':           academicYearId,
            'categoryCode':             categoryCode
        })
        return TypeAdapter(Reports).validate_json(response)

    def categories(self, 
                   receivingInstitutionId:  int, 
                   sendingInstitutionId:    int, 
                   academicYearId:          int
                   ) -> list[Categories]:

        response = self.scraper.get(Endpoint.CATEGORIES, params = {
            'receivingInstitutionId':   receivingInstitutionId,
            'sendingInstitutionId':     sendingInstitutionId,
            'academicYearId':           academicYearId
        })
        return TypeAdapter(list[Categories]).validate_json(response)

    def years(self) -> list[Year]:
        response = self.scraper.get(Endpoint.YEARS)
        return TypeAdapter(list[Year]).validate_json(response)

# request = Request()

# courselist = request.courses(124, 76, CourseList.Type.IGETC)

# print(*courselist.courseInformationList[1], sep = '\n')

# institutions = request.institutions()
# print(institutions[0])

# agreement = request.agreement(76, 124, 11, Agreement.Type.SENDINGPREFIX, 5768)
# print(agreement)

# agreements = request.agreements(124)
# print(agreements)

# transferrability = request.transferrability(124)
# print(transferrability)

# reports = request.reports(11, 124, 76, Reports.Type.MAJOR)
# print(reports)

# categories = request.categories(11, 124, 76)
# print(categories)

# years = request.years()
# print(years)