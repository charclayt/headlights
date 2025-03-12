from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from myapp.tests.test_BaseView import BaseViewTest, USER_NAME, USER_PASSWORD
from myapp.models import Model, UploadedRecord
from myapp.tests.config import Views, Templates, TestData, ErrorCodes

class MLDashboardPageTest(BaseViewTest, TestCase):

    URL = Views.MACHINE_LEARNING
    TEMPLATE = Templates.MACHINE_LEARNING
    MODEL = Model

    def setUp(self):
        return BaseViewTest.setUp(self)

    def test_get_view(self):
        self.TEMPLATE = Templates.LOGIN
        self.client.logout()

        # Test getting page without being logged in redirects to login template
        BaseViewTest.test_get_view(self)
        
        self.client.login(username=USER_NAME, password=USER_PASSWORD)
        self.TEMPLATE = Templates.MACHINE_LEARNING

        # Test getting page when logged in returns the machine learning template
        BaseViewTest.test_get_view(self)

    def test_model_list(self):
        self.URL = Views.API_MODELS_LIST

        # Remove existing objects, and dependent objects
        UploadedRecord.objects.all().delete()
        Model.objects.all().delete()

        # Test getting the model list returns a JSON response with no models
        BaseViewTest._test_get_json_response(self, status=ErrorCodes.OK, response={'status': 'success', 'message': 'no models found'})

        # Create a model object
        Model.objects.create(model_id = 1,
                             model_name = TestData.NAME,
                             notes = "",
                             filepath = "",
                             price_per_prediction = 0)

        # Test getting the model list returns a JSON response with the model created in test_Models
        BaseViewTest._test_get_json_response(self, status=ErrorCodes.OK, response={'status': 'success', 'models': [{'id': 1, 'name': TestData.NAME, 'notes': "", 'filepath': ""}]})

    def test_model_upload(self):
        self.URL = Views.API_UPLOAD_MODEL

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
