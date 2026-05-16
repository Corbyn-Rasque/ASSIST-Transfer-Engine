from api.types import Monomorphic

class GeneralEducation:
    class Model (Monomorphic):
        '''
        Campus-Based GE provide a mechanism to communicate and articulate broader campus-specific general education requirements that exist outside of individual courses.

        :code:  The shortened representation of the General Education Area
        :name:  The name of the General Education Area

        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/ge#generaleducationarea-model)
        '''
        code: str
        name: str