from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from myapp.tests.test_BaseView import BaseViewTest, USER_NAME, USER_PASSWORD
from myapp.tests.config import Views, Templates

class CustomerDashboardTest(BaseViewTest, TestCase):

    URL = Views.CUSTOMER_DASHBOARD
    TEMPLATE = Templates.CUSTOMER

    def setUp(self):
        return BaseViewTest.setUp(self)

    def test_get_view(self):
        self.client.login(username=USER_NAME, password=USER_PASSWORD)
        

class CustomerUploadTest(BaseViewTest, TestCase):
    
    URL = Views.CUSTOMER_UPLOAD
    TEMPLATE = Templates.CUSTOMER
    
    def setUp(self):
        return BaseViewTest.setUp(self)
    
    def test_get_view(self):
        BaseViewTest.test_get_view(self)

    def test_claim_upload(self):

        # Test uploading a model with incorrect file type
        invalid_file = SimpleUploadedFile("test.txt", b"file_content", content_type="text/plain")
        payload = {'claims_file': invalid_file}
        response = BaseViewTest._test_post_view_response(self, payload=payload)
        self.assertJSONEqual(
            response.content,
            {
                'status': "error",
                'message': "Invalid file type"
            }
        )

        # Test uploading a model with correct file type
        with open('myapp/tests/data/TestClaimData.csv', "rb") as f:
            data = f.read()
            
        valid_file = SimpleUploadedFile("test.csv", data)
        payload = {'claims_file': valid_file}
        response = BaseViewTest._test_post_view_response(self, payload=payload)
            
        self.assertJSONEqual(
            response.content,
            {
                'status': "success",
                'message': "",
            }
        )