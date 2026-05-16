from api.types import Monomorphic

class Requirement:
    class Model (Monomorphic):
        '''
        Campus Requirements provide a mechanism to communicate and articulate broader campus requirements that exist outside of individual courses.

        :name:  The name of the requirement

        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/requirement#requirement-model)
        '''
        name: str