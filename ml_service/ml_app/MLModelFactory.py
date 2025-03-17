from .MLModelService import DefaultClaimsModel

class ModelFactory:
    
    @staticmethod
    def build_model(name):
        if name == 'default':
            return DefaultClaimsModel()
        else:
            raise Exception("Invalid model name")
