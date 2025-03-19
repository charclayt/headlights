from .MLModelService import DefaultClaimsModel, GenericModel

class ModelFactory:
    
    @staticmethod
    def build_model(name):
        if name == 'default':
            return DefaultClaimsModel()
        else:
            return GenericModel()
