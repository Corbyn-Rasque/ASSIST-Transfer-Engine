from api.types import Monomorphic

class Attribute:
    class Model (Monomorphic):
        '''
        Attributes are notes that can be placed anywhere on an articulation. The placement of the attribute depends on where it appears on the in the Articulation model.

        :content:   The text of the attribute
        :position:  The position this attribute should appear
        
        [Documentation](https://prod.assistng.org/apidocs/docs/articulation/model/attribute#attribute-model)
        '''
        content:  str
        position: int