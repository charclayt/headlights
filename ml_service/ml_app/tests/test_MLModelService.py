import numpy as np
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
        model = PredictionModel.objects.create(
            model_id=1,
            model_name='test_model',
            model_type='default',
            notes='',
            filepath='/shared/media/models/limited_model.pkl')
        
        step = PreprocessingStep.objects.create(
            preprocessing_step_id = 1,
            preprocess_name = 'create_days_between_col'
        )

        PreprocessingModelMap.objects.create(
            preprocessing_model_map_id = 1,
            preprocessing_step_id=step,
            model_id=model
        )

    def test_predict_success(self):
        model = ClaimsModel(PredictionModel.objects.get(model_id=1))
        model.load_model()
        result = model.predict(pd.DataFrame([self.payload]))

        self.assertTrue(type(result) == np.float64, f"Non float value returned, got {type(result)}")
