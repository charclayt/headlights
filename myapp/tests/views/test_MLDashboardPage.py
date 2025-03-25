from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch, MagicMock

from myapp.tests.test_BaseView import BaseViewTest, USER_NAME, USER_PASSWORD
from myapp.models import PredictionModel, UploadedRecord, PreprocessingStep, PreprocessingModelMap
from myapp.tests.config import Views, Templates, TestData, ErrorCodes
from django.urls import reverse

import logging

class MLDashboardPageTest(BaseViewTest, TestCase):

    URL = Views.MACHINE_LEARNING
    TEMPLATE = Templates.MACHINE_LEARNING
    MODEL = PredictionModel

    def setUp(self):
        logging.disable(logging.ERROR)
        return BaseViewTest.setUp(self)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_get_view(self):
        self.TEMPLATE = Templates.LOGIN
        self.client.logout()

        # Test getting page without being logged in redirects to login template
        BaseViewTest.test_get_view(self)
        
        self.client.login(username=USER_NAME, password=USER_PASSWORD)
        self.TEMPLATE = Templates.MACHINE_LEARNING

        # Test getting page when logged in returns the machine learning template
        BaseViewTest.test_get_view(self)
    
    def test_unauthenticated_model_list(self):
        self.URL = Views.API_MODELS_LIST
        self.client.logout()
        
        # Test getting the model list without being logged in
        response = self.client.get(path=reverse(self.URL), follow=True)
        self.assertEqual(response.status_code, ErrorCodes.UNAUTHORIZED)  # Changed from OK to UNAUTHORIZED
        self.assertJSONEqual(
            response.content,
            {
                'status': 'error',
                'message': 'Authentication required'
            }
        )

    def test_unauthenticated_model_upload(self):
        self.URL = Views.API_UPLOAD_MODEL
        self.client.logout()
        
        # Test uploading a model without being logged in
        valid_file = SimpleUploadedFile("test.pkl", b"file_content", content_type="application/octet-stream")
        payload = {'model_name': TestData.NAME, 'notes': "", 'model_file': valid_file}
        response = self.client.post(path=reverse(self.URL), data=payload, follow=True)
        self.assertEqual(response.status_code, ErrorCodes.UNAUTHORIZED)  # Changed from OK to UNAUTHORIZED
        self.assertJSONEqual(
            response.content,
            {
                'status': 'error',
                'message': 'Authentication required'
            }
        )

    @patch('myapp.views.MLDashboardView.requests.get')
    def test_model_list(self, mock_get):
        self.URL = Views.API_MODELS_LIST

        # Configure the mock to return a specific response when called with expected URL
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'success', 'message': 'no models found'}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Remove existing objects, and dependent objects
        UploadedRecord.objects.all().delete()
        PreprocessingModelMap.objects.all().delete()
        PreprocessingStep.objects.all().delete()
        PredictionModel.objects.all().delete()

        # Test getting the model list returns a JSON response with no models
        BaseViewTest._test_get_json_response(self, status=ErrorCodes.OK, response={'status': 'success', 'message': 'no models found'})

        # Create a model object
        PredictionModel.objects.create(model_id = 1,
                             model_name = TestData.NAME,
                             notes = "",
                             filepath = "",
                             price_per_prediction = 0)

        # Configure the mock to return a response with the created model
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'success', 'models': [{'id': 1, 'name': TestData.NAME, 'notes': "", 'filepath': ""}]}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Test getting the model list returns a JSON response with the model created
        BaseViewTest._test_get_json_response(self, status=ErrorCodes.OK, response={'status': 'success', 'models': [{'id': 1, 'name': TestData.NAME, 'notes': "", 'filepath': ""}]})

    @patch('myapp.views.MLDashboardView.requests.post')
    def test_model_upload(self, mock_post):
        self.URL = Views.API_UPLOAD_MODEL

        # First test case - no file provided
        # Set up mock for first case (bad request - no file)
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': "error", 'message': "No model file provided"}
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        # Test uploading a model without file
        payload = {'notes': "", 'filepath': ""}
        response = BaseViewTest._test_post_view_response(self, status=ErrorCodes.BAD_REQUEST, payload=payload)
        self.assertJSONEqual(
            response.content,
            {
                'status': "error",
                'message': "No model file provided"
            }
        )

        # Second test case - incorrect file type
        # Set up mock for second case (bad request - invalid file type)
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': "error", 'message': "Invalid file format. Only .pkl files are allowed."}
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        # Test uploading a model with incorrect file type
        invalid_file = SimpleUploadedFile("test.txt", b"file_content", content_type="text/plain")
        payload = {'model_name': TestData.NAME, 'notes': "", 'model_file': invalid_file}
        response = BaseViewTest._test_post_view_response(self, status=ErrorCodes.BAD_REQUEST, payload=payload)
        self.assertJSONEqual(
            response.content,
            {
                'status': "error",
                'message': "Invalid file format. Only .pkl files are allowed."
            }
        )

        # Third test case - successful upload
        # Set up mock for third case (success)
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': "success", 'message': "Model uploaded successfully", 'model_id': 2}
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Test uploading a model with correct file type
        valid_file = SimpleUploadedFile("test.pkl", b"file_content", content_type="application/octet-stream")
        payload = {'model_name': TestData.NAME, 'notes': "", 'model_file': valid_file}
        response = BaseViewTest._test_post_view_response(self, payload=payload)
        self.assertJSONEqual(
            response.content,
            {
                'status': "success",
                'message': "Model uploaded successfully",
                'model_id': 2 # Model ID should be 2 as the first model was created in test_Models
            }
        )

    @patch('myapp.views.MLDashboardView.requests.get')
    def test_model_list_exception(self, mock_get):
        self.URL = Views.API_MODELS_LIST

        # Configure the mock to raise an exception
        mock_get.side_effect = Exception("Test exception")

        # Test getting the model list when an exception occurs
        response = self.client.get(path=reverse(self.URL), follow=True)
        self.assertEqual(response.status_code, ErrorCodes.SERVER_ERROR)
        self.assertJSONEqual(
            response.content,
            {
                'status': 'error',
                'message': 'Error communicating with ML service: Test exception'
            }
        )

    @patch('myapp.views.MLDashboardView.requests.post')
    def test_model_upload_exception(self, mock_post):
        self.URL = Views.API_UPLOAD_MODEL

        # Configure the mock to raise an exception
        mock_post.side_effect = Exception("Test exception")

        # Test uploading a model when an exception occurs
        valid_file = SimpleUploadedFile("test.pkl", b"file_content", content_type="application/octet-stream")
        payload = {'model_name': TestData.NAME, 'notes': "", 'model_file': valid_file}
        response = self.client.post(path=reverse(self.URL), data=payload, follow=True)
        self.assertEqual(response.status_code, ErrorCodes.SERVER_ERROR)
        self.assertJSONEqual(
            response.content,
            {
                'status': 'error',
                'message': 'Error communicating with ML service: Test exception'
            }
        )
