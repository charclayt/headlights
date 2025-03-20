from abc import ABC, abstractmethod
import numpy as np
import os
import pandas as pd
import pickle

from .models import PreprocessingModelMap

import logging

logger = logging.getLogger(__name__)

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
        preprocessor = PreProcessing(model_id=self.model_row.model_id, data=claims_data)
        return preprocessor.apply_preprocessing()

    def predict(self, data):
        # TODO: discuss whether we need both of these models
        data = self.preprocess_data(data)

        model_dir = os.path.join('/shared/', self.model_row.filepath)

        pipeline = self.load_model(model_dir)

        # TODO: work out why pipeline needs 37 columns...
        data = data[0].copy()

        logger.warning(data)

        prediction = pipeline.predict(data)

        logger.warning(prediction)
        
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
        
        log_prediction = pipeline.predict(data)

        prediction = np.expm1(log_prediction)
        
        return prediction
    
"""
Interact with preprocessing steps stored in the database, apply to models within their preprocessing step.
"""
class PreProcessing():
    def __init__(self, model_id, data):
        self.model_id = model_id
        self.data = data
        self.steps = []

        # TODO: handle errors
        self.errors = []

    def apply_preprocessing(self):
        # Get all of the preprocessing mappings for the supplied model.
        preprocessing_model_maps = PreprocessingModelMap.objects.filter(model_id=self.model_id).select_related('preprocessing_step_id')

        # Use mapping table to access preprocessing IDs, then add those processes to the queue (could be an actual q instead of list)
        for model_map in preprocessing_model_maps:
            preprocessing_step = model_map.preprocessing_step_id
            logger.warning(preprocessing_step)
            self.steps.append(preprocessing_step.preprocess_name)

        for step_str in self.steps:
            method = getattr(self, step_str, None)

            if method and callable(method):
                method()
            else:
                self.errors.append(f"Unknown or non-callable preprocessing step: {step_str}")

        logger.warning('preprocessing applied')
        return self.data, self.errors

    def create_days_between_col(self):
        # Determine difference between AccidentDate and ClaimDate and create new column.
        # Raise ValueError if there is missing data.
        if 'AccidentDate' in self.data.columns and 'ClaimDate' in self.data.columns:
            self.data['DaysBetweenAccidentAndClaim'] = self.data['ClaimDate'] - self.data['AccidentDate']
        else:
            self.errors.append("create_days_between_col: 'AccidentDate' and 'ClaimDate' are not present in this data.")
