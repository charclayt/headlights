import logging
import numpy as np
import os
import pandas as pd

from django.test import TestCase

from ml_app.MLModelService import ClaimsModel
from ml_app.models import PredictionModel, PreprocessingStep, PreprocessingModelMap

class MLModelServiceTest(TestCase):
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.payload = {
            "AccidentType": "Rear end",
            "InjuryPrognosis": 5,
            "SpecialHealthExpenses": 0,
            "SpecialReduction": 0,
            "SpecialOverage": 0,
            "GeneralRest": 0,
            "SpecialAdditionalInjury": 0,
            "SpecialEarningsLoss": 0,
            "SpecialUsageLoss": 0,
            "SpecialMedications": 0,
            "SpecialAssetDamage": 0,
            "SpecialRehabilitation": 0,
            "SpecialFixes": 0,
            "GeneralFixed": 520,
            "GeneralUplift": 0,
            "SpecialLoanerVehicle": 0,
            "SpecialTripCosts": 0,
            "SpecialJourneyExpenses": 0,
            "SpecialTherapy": 0,
            "ExceptionalCircumstances": 0,
            "MinorPsychologicalInjury": 1,
            "DominantInjury": "Arms",
            "Whiplash": 1,
            "VehicleType": "Motorcycle",
            "WeatherConditions": "Rainy",
            "AccidentDate": 2023314,
            "ClaimDate": 2023163,
            "VehicleAge": 13,
            "DriverAge": 33,
            "NumberOfPassengers": 4,
            "AccidentDescription": "Side collision at an intersection.",
            "InjuryDescription": "Whiplash and minor bruises.",
            "PoliceReportFiled": 1,
            "WitnessPresent": 1,
            "Gender": "Male"
        }

    def setUp(self):
        logging.disable(logging.INFO)

        filepath = '/shared/media/models/limited_model.pkl'
        if os.getenv('GITHUB_ACTIONS') == 'true':
            filepath = '../dataset/limited_model.pkl'

        self.prediction_model = PredictionModel.objects.create(
            model_id=1,
            model_name='test_model',
            model_type='default',
            notes='',
            filepath=filepath)
        
        step = PreprocessingStep.objects.create(
            preprocessing_step_id = 1,
            preprocess_name = 'create_days_between_col'
        )

        PreprocessingModelMap.objects.create(
            preprocessing_model_map_id = 1,
            preprocessing_step_id=step,
            model_id=self.prediction_model
        )

        self.claims_model = ClaimsModel(PredictionModel.objects.get(model_id=1))
        self.claims_model.load_model()

    def tearDown(self):
        logging.disable(logging.NOTSET)
        return super().tearDown()

    def test_predict_success(self):
        result = self.claims_model.predict(pd.DataFrame([self.payload]))

        self.assertTrue(type(result) is np.float64, f"Non float value returned, got {type(result)}")

    def test_bad_preprocessing_step(self):
        new_step = PreprocessingStep.objects.create(
            preprocessing_step_id = 2,
            preprocess_name = 'bad_step'
        )

        PreprocessingModelMap.objects.create(
            preprocessing_model_map_id = 2,
            preprocessing_step_id=new_step,
            model_id=self.prediction_model
        )

        with self.assertRaises(Exception) as context:
            self.claims_model.predict(pd.DataFrame([self.payload]))

        self.assertIn("Unknown or non-callable preprocessing step", str(context.exception))

    def test_create_days_col_failure(self):
        # get payload without required columns
        payload = self.payload

        del payload['ClaimDate']

        with self.assertRaises(Exception) as context:
            self.claims_model.predict(pd.DataFrame([payload]))

        self.assertIn("'AccidentDate' or 'ClaimDate' are not present in this data for model", str(context.exception))
