from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory, TestCase

from myapp.tests.test_BaseView import BaseViewTest, USER_NAME, USER_PASSWORD
from myapp.tests.config import Views, Templates, TestData, ErrorCodes

from myapp.views.CustomerDashBoardView import PredictionFeedbackView
from myapp.models import Claim, Feedback, UploadedRecord

class CustomerDashboardTest(BaseViewTest, TestCase):

    URL = Views.CUSTOMER_DASHBOARD
    TEMPLATE = Templates.CUSTOMER

    def setUp(self):
        return BaseViewTest.setUp(self)

    def test_get_view(self):
        self.TEMPLATE = Templates.LOGIN
        self.client.logout()

        BaseViewTest.test_get_view(self)

        self.client.login(username=USER_NAME, password=USER_PASSWORD)
        self.TEMPLATE = Templates.CUSTOMER

        BaseViewTest.test_get_view(self)

    def test_get_uploaded_record_does_not_exist(self):
        session = self.client.session
        session['uploaded_record_id'] = 9999 # Assuming 9999 is an invalid ID
        session.save()

        BaseViewTest.test_get_view(self)

        # Check if the session key is removed
        self.assertNotIn('uploaded_record_id', self.client.session)

    def test_post_view_valid(self):
        claim = Claim.objects.first()
        form_data = {'uploaded_claims': claim.claim_id}

        BaseViewTest._test_post_view_response(self, payload=form_data)

        # Delete the uploaded record from the database
        UploadedRecord.objects.filter(user_id=self.user_profile).delete()

    def test_post_view_invalid(self):
        form_data = {'uploaded_claims': 0}

        BaseViewTest._test_post_view_response(self, status=ErrorCodes.BAD_REQUEST, payload=form_data)

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
        
        # Test uploading a model with correct file type but incorrect columns
        with open('myapp/tests/data/InvalidTestClaimData.csv', "rb") as f:
            data = f.read()
            
        valid_file = SimpleUploadedFile("test.csv", data)
        payload = {'claims_file': valid_file}
        response = BaseViewTest._test_post_view_response(self, payload=payload)

        self.assertJSONEqual(
            response.content,
            {
                'status': "confirmationRequired",
                'message': "The following columns could not be found in the uploaded file: Gender\n\nThe following columns are either missnamed or invalid: ExcessCol"
            }
        )

        # Test uploading a model with correct file type and valid columns
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

class PredictionFeedbackTest(BaseViewTest, TestCase):
    
    URL = Views.PREDICTION_FEEDBACK
    TEMPLATE = Templates.PREDICTION_FEEDBACK
    
    def setUp(self):
        return BaseViewTest.setUp(self)
    
    def test_get_view(self):
        BaseViewTest.test_get_view(self)

    def test_valid_feedback_form(self):
        form = PredictionFeedbackView.form_class
        # Check if the form is the correct form
        self.assertEqual(form.Meta.model.__name__, "Feedback")

        # Check if the form is valid
        form_data = {'rating' : TestData.RATING, 'notes' : TestData.NAME}
        form = form(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_feedback_form(self):
        form = PredictionFeedbackView.form_class
        # Check if the form is the correct form
        self.assertEqual(form.Meta.model.__name__, "Feedback")

        # Check if the form is invalid with out of range rating
        form_data = {'rating' : 0, 'notes' : ""}
        form = form(data=form_data)
        self.assertFalse(form.is_valid())

    def test_post_view(self):
        factory = RequestFactory()
        form_data = {'rating' : TestData.RATING, 'notes' : TestData.NAME}

        request = factory.post(self.URL, form_data)
        request.user = self.user

        # Initialise SessionMiddleware
        middleware = SessionMiddleware(lambda x : None)
        middleware.process_request(request)
        request.session['uploaded_record_id'] = 1
        request.session.save()

        # Initialise MessageMiddleware
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = PredictionFeedbackView.as_view()(request)
        self.assertTrue(response)

        # Check if the feedback was saved to the database
        feedback = Feedback.objects.filter(user_id=self.user_profile)
        for f in feedback:
            self.assertEqual(f.rating, TestData.RATING)
            self.assertEqual(f.notes, TestData.NAME)

            # Check if the feedback was assigned to the uploaded record, and delete it
            uploaded_record = UploadedRecord.objects.get(feedback_id=f)
            self.assertEqual(uploaded_record.feedback_id, f)
            uploaded_record.delete()

            # Delete the feedback from the database
            f.delete()
