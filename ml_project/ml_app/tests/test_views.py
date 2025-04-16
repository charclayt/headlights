# Temporary test until front-end functionality added to MLDashboard to predict
# TODO: move test to myapp/tests/views/test_MLDashboardPage.py when predict FE implemented.
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
import logging
import os
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch

from ml_app.models import PredictionModel, PreprocessingStep, PreprocessingModelMap

class ModelListTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = 'api/models/'

        filepath = '/shared/media/models/limited_model.pkl'
        if os.getenv('GITHUB_ACTIONS') == 'true':
            filepath = '../dataset/limited_model.pkl'

        self.model = PredictionModel.objects.create(
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

        logging.disable(logging.ERROR)
    
    def tearDown(self):
        logging.disable(logging.NOTSET)
        return super().tearDown()

    def test_get_model_success(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('test_model', response.data['models_list']['name'])
        self.assertEqual('create_days_between_col', response.data['models_list']['preprocessingSteps'])


class ModelPredictTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/model/predict/'

        filepath = '/shared/media/models/limited_model.pkl'
        if os.getenv('GITHUB_ACTIONS') == 'true':
            filepath = '../dataset/limited_model.pkl'

        self.model = PredictionModel.objects.create(
            model_id=1,
            model_name='test_model',
            model_type='default',
            notes='',
            filepath=filepath)

        logging.disable(logging.ERROR)

    def tearDown(self):
        logging.disable(logging.NOTSET)
        return super().tearDown()
    
    def test_missing_model_id(self):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'PredictionModel ID not supplied')
    
    def test_non_existent_model(self):
        response = self.client.post(self.url, {'model_id': 99999}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'PredictionModel supplied does not exist')
    
    def test_empty_data(self):
        response = self.client.post(self.url, {'model_id': 1, 'data': {}}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'PredictionModel name not supplied')
    
    def test_internal_server_error_on_model_build(self):
        PredictionModel.objects.create(model_id=2)

        response = self.client.post(self.url, {'model_id': 2, 'data': {'feature1': 1}}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Failed to load model: 2')
    
    def test_successful_prediction(self):
        with patch('ml_app.MLModelService.ClaimsModel.predict', return_value={'result': 0.95}):
            response = self.client.post(self.url, {'model_id': 1, 'data': {'feature1': 1}}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('data', response.data)
            self.assertEqual(response.data['data']['prediction'], {'result': 0.95})

class ModelUploadTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.url = 'api/upload-model/'

        self.test_file = SimpleUploadedFile(
            "test_model.pkl", b"fake-model-content", content_type="application/octet-stream"
        )
        
        self.preprocessingStep = PreprocessingStep.objects.create(
            preprocessing_step_id = 1,
            preprocess_name = 'create_days_between_col'
        )

        logging.disable(logging.ERROR)

    def test_model_upload_success(self):
        data = {
            'model_name': 'TestModel',
            'notes': 'test notes',
            'selected_steps': [self.preprocessingStep.preprocessing_step_id]
        }

        response = self.client.post(self.url, data={
            **data,
            'model_file': self.test_file
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertTrue(PredictionModel.objects.filter(model_name='TestModel').exists())
