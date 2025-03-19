from .MLModelService import DefaultClaimsModel, GenericModel

class PredictionModelFactory:
    
    @staticmethod
    def build_model(model):
        # TODO: rework this to not be hard coded if else
        if model.model_type == 'default':
            return DefaultClaimsModel(model)
        else:
            return GenericModel(model)
