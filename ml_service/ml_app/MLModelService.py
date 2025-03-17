from abc import ABC, abstractmethod

class MLModel(ABC):
    
    @abstractmethod
    def load_model(self, path):
        pass
    
    @abstractmethod
    def preprocess_data(self, data):
        pass
    
    @abstractmethod
    def predict(self):
        pass
    
class DefaultClaimsModel(MLModel):

    def load_model(self, path):
        pass
    
    def preprocess_data(self, data):
        pass

    def predict(self):
        pass
        