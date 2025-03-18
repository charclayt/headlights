from abc import ABC, abstractmethod
import pandas as pd
import pickle
import numpy as np
import os
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .models import Model

"""
    Abstract base class for concrete ML classes to inherit from
"""
class MLModel(ABC):
    
    def load_model(self, path):
        with open(path, "rb") as file:
            pipeline = pickle.load(file)
        return pipeline
    
    @abstractmethod
    def preprocess_data(self, data):
        pass
    
    @abstractmethod
    def predict(self):
        pass

"""
    Class for the default claim model. 
    Most preprocessing steps are handled in the pipeline in the training stage
"""
class DefaultClaimsModel(MLModel):
    
    def preprocess_data(self, claims_data):
        if 'AccidentDate' in claims_data.columns and 'ClaimDate' in claims_data.columns:
            claims_data['DaysBetweenAccidentAndClaim'] = claims_data['ClaimDate'] - claims_data['AccidentDate']
        return claims_data

    def predict(self, name, data):
        data = pd.DataFrame(data, index=[0])
        data = self.preprocess_data(data)
        model_row = Model.objects.filter(model_name=name).values()[0]

        model_dir = os.path.join('/shared/', model_row['filepath'])

        pipeline = self.load_model(model_dir)
        
        prediction = np.expm1(pipeline.predict(data))
        
        return prediction
    
"""
    Fallback generic model.
    It is assumed that there are no specific preproccessing steps if none are specified
""" 
class GenericModel(MLModel):

    def preprocess_data(self, claims_data):
        return claims_data

    def predict(self, name, data):
        data = pd.DataFrame(data, index=[0])
        data = self.preprocess_data(data)
        model_row = Model.objects.filter(model_name=name).values()[0]

        model_dir = os.path.join('/shared/', model_row['filepath'])

        pipeline = self.load_model(model_dir)
        
        prediction = pipeline.predict(data)
        
        return prediction



