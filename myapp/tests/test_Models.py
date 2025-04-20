from django.test import TestCase
from django.contrib.auth.models import User

from myapp.tests.config import TestData
from myapp.models import Claim, ContactInfo, Company, UserProfile, FinanceReport, \
                            Feedback, DatabaseLog, PredictionModel, OperationLookup, TableLookup, \
                            TrainingDataset, UploadedRecord, PreprocessingStep, \
                            PreprocessingModelMap

class TestModels(TestCase):
    @classmethod
    def setUp(cls):
        # Create a test user
        user = User.objects.create_user(username=TestData.EMAIL, password="testpassword1")
        user.save()

        # Create model objects

        Claim.objects.create(claim_id = 1,
                             settlement_value = TestData.VALUE,
                             accident_type = "",
                             injury_prognosis = 0,
                             special_health_expenses = 0,
                             special_reduction = 0,
                             special_overage = 0,
                             general_rest = 0,
                             special_additional_injury = 0,
                             special_earnings_loss = 0,
                             special_usage_loss = 0,
                             special_medications = 0,
                             special_asset_damage = 0,
                             special_rehabilitation = 0,
                             special_fixes = 0,
                             general_fixed = 0,
                             general_uplift = 0,
                             special_loaner_vehicle = 0,
                             special_trip_costs = 0,
                             special_journey_expenses = 0,
                             special_therapy = 0,
                             exceptional_circumstances = 0,
                             minor_psychological_injury = 0,
                             dominant_injury = "",
                             whiplash = 0,
                             vehicle_type = "",
                             weather_conditions = "",
                             accident_date = 0,
                             claim_date = 0,
                             vehicle_age = 0,
                             driver_age = 0,
                             number_of_passengers = 0,
                             accident_description = "",
                             injury_description = "",
                             police_report_filed = 0,
                             witness_present = 0,
                             gender = "")
        
        ContactInfo.objects.create(contact_info_id = 1,
                                   phone = TestData.PHONE,
                                   email = TestData.EMAIL,
                                   address = TestData.ADDRESS,)
        
        Company.objects.create(company_id = 1,
                               contact_info_id = ContactInfo.objects.get(contact_info_id = 1),
                               name = TestData.NAME)
        
        UserProfile.objects.create(user_profile_id = 1,
                                   auth_id = User.objects.get(username = TestData.EMAIL),
                                   contact_info_id = ContactInfo.objects.get(contact_info_id = 1),
                                   company_id = Company.objects.get(company_id = 1),
                                   is_company_owner = True)
        
        FinanceReport.objects.create(finance_report_id = 1,
                                     user_id = UserProfile.objects.get(user_profile_id = 1),
                                     year = TestData.YEAR,
                                     month = 0,
                                     cost_incurred = 0,
                                     generated_invoice = "This is a test invoice",
                                     company_id = Company.objects.get(company_id = 1),
                                     created_at = TestData.PAST_DATETIME)
        
        Feedback.objects.create(feedback_id = 1,
                                user_id = UserProfile.objects.get(user_profile_id = 1),
                                rating = TestData.RATING,
                                notes = "no notes")
        
        OperationLookup.objects.create(operation_id = 1,
                                       operation_name = TestData.NAME)
        
        TableLookup.objects.create(table_id = 1,
                                   table_name = TestData.NAME)

        DatabaseLog.objects.create(database_log_id = 1,
                                   log_time = TestData.PAST_DATETIME,
                                   user_id = UserProfile.objects.get(user_profile_id = 1),
                                   affected_table_id = TableLookup.objects.get(table_id = 1),
                                   operation_performed = OperationLookup.objects.get(operation_id = 1),
                                   successful = 0,
                                   notes = "")

        PredictionModel.objects.create(model_id = 1,
                             model_name = TestData.NAME,
                             notes = "",
                             filepath = "",
                             price_per_prediction = 0)
        
        
        TrainingDataset.objects.create(training_dataset_id = 1,
                                       claim_id = Claim.objects.get(claim_id = 1))
        
        UploadedRecord.objects.create(uploaded_record_id = 1,
                                      user_id = UserProfile.objects.get(user_profile_id = 1),
                                      claim_id = Claim.objects.get(claim_id = 1),
                                      feedback_id = Feedback.objects.get(feedback_id = 1),
                                      model_id = PredictionModel.objects.get(model_id = 1),
                                      predicted_settlement = 0,
                                      upload_date = TestData.PAST_DATE)
        
        PreprocessingStep.objects.create(preprocessing_step_id = 1,
                                         preprocess_name = TestData.NAME)
        
        PreprocessingModelMap.objects.create(preprocessing_model_map_id = 1,
                                             preprocessing_step_id = PreprocessingStep.objects.get(preprocessing_step_id = 1),
                                             model_id = PredictionModel.objects.get(model_id = 1))
        
        
        
    # Test the models, ensure they are created correctly and the first field is correct

    def test_model_claim(self):
        claim = Claim.objects.get(claim_id=1)
        self.assertTrue(claim.__str__().startswith(str(claim.claim_id)))
        self.assertTrue(claim.settlement_value, TestData.VALUE)

    def test_model_contact_info(self):
        contact_info = ContactInfo.objects.get(contact_info_id=1)
        self.assertTrue(contact_info.__str__().startswith(contact_info.email))
        self.assertTrue(contact_info.email, TestData.EMAIL)

    def test_model_company(self):
        company = Company.objects.get(company_id=1)
        self.assertTrue(company.__str__().startswith(company.name))
        self.assertTrue(company.name, TestData.NAME)

    def test_model_user_profile(self):
        user_profile = UserProfile.objects.get(user_profile_id=1)
        self.assertTrue(user_profile.__str__().startswith(user_profile.auth_id.username))
        self.assertTrue(user_profile.auth_id.username, TestData.EMAIL)

    def test_model_finance_report(self):
        finance_report = FinanceReport.objects.get(finance_report_id=1)
        self.assertTrue(finance_report.__str__().startswith(str(finance_report.year)))
        self.assertTrue(finance_report.year, TestData.YEAR)

    def test_model_feedback(self):
        feedback = Feedback.objects.get(feedback_id=1)
        self.assertTrue(feedback.__str__().startswith(str(feedback.rating)))
        self.assertTrue(feedback.rating, TestData.RATING)

    def test_model_database_log(self):
        database_log = DatabaseLog.objects.get(database_log_id=1)
        self.assertTrue(database_log.__str__().startswith(database_log.log_time.strftime("%Y-%m-%d %H:%M:%S")))
        self.assertTrue(database_log.log_time, TestData.PAST_DATETIME)

    def test_model_model(self):
        model = PredictionModel.objects.get(model_id=1)
        self.assertTrue(model.__str__().startswith(model.model_name))
        self.assertTrue(model.model_name, TestData.NAME)

    def test_model_operation_lookup(self):
        operation_lookup = OperationLookup.objects.get(operation_id=1)
        self.assertTrue(operation_lookup.__str__().startswith(operation_lookup.operation_name))
        self.assertTrue(operation_lookup.operation_name, TestData.NAME)

    def test_model_table_lookup(self):
        table_lookup = TableLookup.objects.get(table_id=1)
        self.assertTrue(table_lookup.__str__().startswith(table_lookup.table_name))
        self.assertTrue(table_lookup.table_name, TestData.NAME)

    def test_model_training_dataset(self):
        training_dataset = TrainingDataset.objects.get(training_dataset_id=1)
        self.assertTrue(training_dataset.__str__().startswith(str(training_dataset.claim_id.claim_id)))
        self.assertTrue(training_dataset.claim_id.settlement_value, TestData.VALUE)

    def test_model_uploaded_record(self):
        uploaded_record = UploadedRecord.objects.get(uploaded_record_id=1)
        self.assertTrue(uploaded_record.__str__().startswith(uploaded_record.user_id.auth_id.username))
        self.assertTrue(uploaded_record.user_id.auth_id.username, TestData.EMAIL)

    def test_model_preprocessing_step(self):
        preprocess_step = PreprocessingStep.objects.get(preprocessing_step_id=1)
        self.assertTrue(preprocess_step.__str__().startswith(preprocess_step.preprocess_name))
        self.assertEqual(preprocess_step.preprocess_name, TestData.NAME)
        
    def test_model_preprocessing_model_map(self):
        preprocess_model_map = PreprocessingModelMap.objects.get(preprocessing_model_map_id=1)
        self.assertTrue(preprocess_model_map.__str__().startswith(preprocess_model_map.preprocessing_step_id.preprocess_name))
        self.assertEqual(preprocess_model_map.preprocessing_step_id.preprocess_name, TestData.NAME)
