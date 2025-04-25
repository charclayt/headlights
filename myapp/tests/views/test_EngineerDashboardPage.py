from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from myapp.tests.test_BaseView import BaseViewTest
from myapp.models import PredictionModel, UserProfile
from myapp.tests.config import Views, Templates, TestData, ErrorCodes
from django.urls import reverse
from unittest.mock import patch

import logging

class EngineerDashboardPageTest(BaseViewTest, TestCase):

    URL = Views.MACHINE_LEARNING
    TEMPLATE = Templates.ENGINEER
    MODEL = PredictionModel

    def setUp(self):
        logging.disable(logging.ERROR)
        BaseViewTest.setUp(self)

        User = get_user_model()
        auth_id = User.objects.create_user(
            username='engineer',
            email='engineer@example.com',
            password='password'
        )
        UserProfile.objects.create(auth_id=auth_id)

        engineer_permission = Permission.objects.get(codename='add_predictionmodel')
        auth_id.user_permissions.add(engineer_permission)

        self.client.login(username='engineer', password='password')
        self.TEMPLATE = Templates.ENGINEER

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_get_view(self):
        BaseViewTest.test_get_view(self)

    def test_unauthenticated_model_upload(self):
        self.URL = Views.API_UPLOAD_MODEL
        self.client.logout()
        
        # Test uploading a model without being logged in
        valid_file = SimpleUploadedFile("test.pkl", b"file_content", content_type="application/octet-stream")
        payload = {'model_name': TestData.NAME, 'notes': "", 'model_file': valid_file}
        response = self.client.post(path=reverse(self.URL), data=payload)

        self.assertEqual(response.status_code, ErrorCodes.REDIRECT)

    @patch('myapp.views.EngineerDashboardView.requests.post')
    def test_post_view_success(self, mock_post):
        mock_post.return_value.status_code = 200

        file_data = SimpleUploadedFile(
            "test_model.pkl",
            b"File binary data",
            content_type="application/octet-stream"
        )

        response = self.client.post(
            reverse(self.URL),
            data={'model_file': file_data},
            format='multipart'
        )

        self.assertEqual(response.status_code, 302)
        mock_post.assert_called_once()
        self.assertIn("/api/upload-model/", mock_post.call_args[0][0])

    def test_post_view_failure_no_model_file(self):
        BaseViewTest._test_post_view_response(self, payload={}, status=400)
