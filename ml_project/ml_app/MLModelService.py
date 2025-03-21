from abc import ABC, abstractmethod
import logging
import numpy as np
import os
import pickle

from django.conf import settings

from .models import PreprocessingModelMap

logger = logging.getLogger(__name__)

"""
    Abstract base class for concrete ML classes to inherit from
"""
class MLModel(ABC):
    def __init__(self, model):
        super().__init__()
        self.model_row = model
    
    def load_model(self):
        model_path = os.path.join(settings.BASE_DIR, self.model_row.filepath)
        with open(model_path, "rb") as file:
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
    Most preprocessing steps are handled in the pipeline in the training stage.
    Some steps are called in the PreProcessing Class.
    TODO: Discuss with JackP about moving away from Factory pattern.
"""
class ClaimsModel(MLModel):
    def __init__(self, model):
        super().__init__(model=model)

    def preprocess_data(self, claims_data):
        preprocessor = PreProcessing(model_id=self.model_row.model_id, data=claims_data)
        return preprocessor.apply_preprocessing()

    def predict(self, data):
        data = self.preprocess_data(data)
        pipeline = self.load_model()

        log_prediction = pipeline.predict(data)
        prediction = np.expm1(log_prediction[0])

        logger.info(f"Successful prediction for model: {self.model_row.model_id}")
        return prediction
 
"""
Interact with preprocessing steps stored in the database, apply to models within their preprocessing step.
"""
class PreProcessing():
    def __init__(self, model_id, data):
        self.model_id = model_id
        self.data = data
        self.steps = []

    def apply_preprocessing(self):
        # Get all of the preprocessing mappings for the supplied model.
        preprocessing_model_maps = PreprocessingModelMap.objects.filter(model_id=self.model_id).select_related('preprocessing_step_id')

        # Use mapping table to access preprocessing IDs, then add those processes to the queue (could be an actual q instead of list)
        for model_map in preprocessing_model_maps:
            preprocessing_step = model_map.preprocessing_step_id
            self.steps.append(preprocessing_step.preprocess_name)

        # Iterate through preprocessing steps, raising an exception if any fail.
        for step_str in self.steps:
            method = getattr(self, step_str, None)

            if method and callable(method):
                method()
            else:
                raise Exception(f"Unknown or non-callable preprocessing step: {step_str} for model: {self.model_id}")

        logger.info(f"Preprocessing applied for model: {self.model_id}")
        return self.data

    def create_days_between_col(self):
        # Determine difference between AccidentDate and ClaimDate and create new column.
        # Raise ValueError if there is missing data.
        if 'AccidentDate' in self.data.columns and 'ClaimDate' in self.data.columns:
            self.data['DaysBetweenAccidentAndClaim'] = self.data['ClaimDate'] - self.data['AccidentDate']
        else:
            raise Exception(f"'AccidentDate' and 'ClaimDate' are not present in this data for model: {self.model_id}")
