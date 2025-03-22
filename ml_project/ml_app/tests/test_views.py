# Temporary test until front-end functionality added to MLDashboard to predict
# TODO: move test to myapp/tests/views/test_MLDashboardPage.py when predict FE implemented.

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
import logging
import os
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch

from ml_app.models import PredictionModel

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
