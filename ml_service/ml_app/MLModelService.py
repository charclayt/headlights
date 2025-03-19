from abc import ABC, abstractmethod
import numpy as np
import os
import pandas as pd
import pickle
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

"""
    Abstract base class for concrete ML classes to inherit from
"""
class MLModel(ABC):
    def __init__(self, model):
        super().__init__()
        self.model_row = model
    
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
    def __init__(self, model):
        super().__init__(model=model)

    def preprocess_data(self, claims_data):
        preprocessor = PreProcessing(model_id=self.model_id, data=claims_data)
        return preprocessor.apply_preprocessing()

    def predict(self, data):
        # TODO: discuss whether we need both of these models
        data = pd.DataFrame(data, index=[0])
        data = self.preprocess_data(data)

        model_dir = os.path.join('/shared/', self.model_row['filepath'])

        pipeline = self.load_model(model_dir)
        
        prediction = np.expm1(pipeline.predict(data))
        
        return prediction
    
"""
    Fallback generic model.
    It is assumed that there are no specific pre-processing steps if none are specified
""" 
class GenericModel(MLModel):
    def __init__(self, model):
        super().__init__(model=model)

    def preprocess_data(self, claims_data):
        return claims_data

    def predict(self, name, data):
        data = pd.DataFrame(data, index=[0])
        data = self.preprocess_data(data)

        model_dir = os.path.join('/shared/', self.model_row['filepath'])

        pipeline = self.load_model(model_dir)
        
        prediction = pipeline.predict(data)
        
        return prediction
    
"""
Interact with preprocessing steps stored in the database, apply to models within their preprocessing step.
"""
class PreProcessing():
    def __init__(self, model_id, data):
        self.model_id = model_id
        self.data = data
        self.errors = []

    def get_preprocessing_steps(self):
        # this will get the steps from the database
        # Use models to get all of the preprocessing steps for the supplied model.

        # use mapping table to convert IDs into calls to functions
        pass

    def apply_preprocessing(self):
        steps = self.get_preprocessing_steps()

        for step in steps:
            step()

        return self.data

    def create_days_between_col(self):
        # Determine difference between AccidentDate and ClaimDate and create new column.
        # Raise ValueError if there is missing data.
        if 'AccidentDate' in self.data.columns and 'ClaimDate' in self.data.columns:
            self.data['DaysBetweenAccidentAndClaim'] = self.data['ClaimDate'] - self.data['AccidentDate']
        else:
            self.errors.append("create_days_between_col: 'AccidentDate' and 'ClaimDate' are not present in this data.")
        
    def one_hot_encode(self):
        try:
            # Identify categorical and numerical columns
            categorical_cols = self.data.select_dtypes(include=['object', 'string']).columns.tolist()
            numerical_cols = self.data.select_dtypes(include=['int64', 'float64']).columns.tolist()

            # Define numerical and categorical transformer pipelines
            numerical_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ])

            categorical_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
            ])

            # Combine transformers into one pipeline
            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', numerical_transformer, numerical_cols),
                    ('cat', categorical_transformer, categorical_cols)
            ])

            # Execute pipeline on inputted data
            self.data = preprocessor.fit(self.data)
        except:
            self.errors.append(("one_hot_encode: Process failed")) 
