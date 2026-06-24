from enum                       import StrEnum
from pydantic                   import TypeAdapter

from sources.web.scraper        import Scraper
from sources.web.area           import Area
from sources.web.courses        import List
from sources.web.institution    import Institution
from sources.web.agreements     import Agreement, Result, Reports

API = 'https://assist.org/api'

class Endpoint (StrEnum):
    AREAS           = API + '/transferability/areaTypes'
    COURSES         = API + '/transferability/courses'
    INSTITUTIONS    = API + '/institutions'
    AGREEMENTS      = API + '/articulation/Agreements'
    REPORTS         = API + '/agreements'

class Request:
    scraper: Scraper

    def __init__(self, scraper: Scraper):
        self.scraper = scraper


    def areas(self) -> list[Area]:
        response = self.scraper.get(Endpoint.AREAS)
        return TypeAdapter(list[Area]).validate_json(response.text)


    def courses(self, 
                institutionId:              int, 
                academicYearId:             int, 
                listType:                   List.Type
                ) -> List:
        
        response = self.scraper.get(Endpoint.COURSES, params = {
            'institutionId':    institutionId,
            'academicYearId':   academicYearId,
            'listType':         listType.name,
        })
        return TypeAdapter(List).validate_json(response.text)
    

    def institutions(self) -> list[Institution]:
        response = self.scraper.get(Endpoint.INSTITUTIONS)
        return TypeAdapter(list[Institution]).validate_json(response.text)


    def agreement(self, 
                  academicYearId:           int, 
                  sendingInstitutionId:     int, 
                  receivingInstitutionId:   int, 
                  type:                     Agreement.Type,
                  filter:                   int | None = None
                  ) -> Result:
        
        response = self.scraper.get(Endpoint.AGREEMENTS + \
            f'?Key={academicYearId}/{sendingInstitutionId}/to/{receivingInstitutionId}/{type}/{filter or ''}'
        )
        return TypeAdapter(Result).validate_json(response.text)


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
        return TypeAdapter(Reports).validate_json(response.text)

# scraper = Scraper('https://assist.org')
# request = Request(scraper)

# courses = request.courses(124, 76, List.Type.CALGETC)
# print(courses)

# institutions = request.institutions()
# print(institutions[0])

# agreements = request.agreement(76, 124, 11, Agreement.Type.SENDINGPREFIX, 5768)
# print(agreements)

# reports = request.reports(11, 124, 76, Reports.Type.MAJOR)
# print(reports)