from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
import os
import logging
from unittest.mock import patch, MagicMock

from myapp.tests.test_BaseView import BaseViewTest, USER_NAME, USER_PASSWORD
from myapp.models import PredictionModel, UploadedRecord, PreprocessingStep, PreprocessingModelMap
from myapp.tests.config import Views, Templates, TestData, ErrorCodes

@override_settings(MEDIA_ROOT='/tmp/test_media')
class MLDashboardPageTest(BaseViewTest, TestCase):

    URL = Views.MACHINE_LEARNING
    TEMPLATE = Templates.MACHINE_LEARNING
    MODEL = PredictionModel

    def setUp(self):
        self.upload_url = reverse('upload_model')
        logging.disable(logging.ERROR)
        return BaseViewTest.setUp(self)

    def tearDown(self):
        logging.disable(logging.NOTSET)

        # Clean up test media directory
        if os.path.exists('/tmp/test_media'):
            for root, dirs, files in os.walk('/tmp/test_media', topdown=False):
                for file in files:
                    os.remove(os.path.join(root, file))
                for dir in dirs:
                    os.rmdir(os.path.join(root, dir))
            os.rmdir('/tmp/test_media')

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
        self.client.logout()
        
        # Test uploading a model without being logged in
        valid_file = SimpleUploadedFile("test.pkl", b"file_content", content_type="application/octet-stream")
        payload = {'model_name': TestData.NAME, 'notes': "", 'model_file': valid_file}
        response = self.client.post(path=self.upload_url, data=payload, follow=True)
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

    def test_upload_no_file(self):
        response = self.client.post(self.upload_url, {'notes': "", 'model_name': TestData.NAME})
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {
            'status': "error",
            'message': "No model file provided"
        })
    
    def test_upload_invalid_file_type(self):
        invalid_file = SimpleUploadedFile("test.txt", b"file_content", content_type="text/plain")
        payload = {'model_name': TestData.NAME, 'notes': "", 'model_file': invalid_file}
        response = self.client.post(path=self.upload_url, data=payload, follow=True)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {
            'status': "error",
            'message': "Invalid file format. Only .pkl files are allowed."
        })

    def test_upload_valid_file(self):
        valid_file = SimpleUploadedFile("test.pkl", b"file_content", content_type="application/octet-stream")
        payload = {'model_name': TestData.NAME, 'notes': "", 'model_file': valid_file}
        response = self.client.post(path=self.upload_url, data=payload, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'status': "success",
            'message': "PredictionModel uploaded successfully",
        })

        model = PredictionModel.objects.first()
        self.assertIsNotNone(model)
        self.assertEqual(model.model_name, TestData.NAME)
