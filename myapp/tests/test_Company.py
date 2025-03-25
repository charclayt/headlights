from django.test import TestCase
from django.contrib.auth.models import Group

from myapp.models import UserProfile, Company
from myapp.tests.config import TestData


class TestCompany(TestCase):
    def setUp(self):
        end_user_group = Group.objects.create(pk=UserProfile.GroupIDs.END_USER_ID, name="end user")
        end_user_group.save()
        
    def test_create_company(self):
        valid_name = TestData.NAME+"1"
        result = UserProfile.create_account(valid_name, TestData.EMAIL, TestData.PASSWORD, UserProfile.GroupIDs.END_USER_ID)
        user: UserProfile = result.payload
        
        result = Company.create_new_company(user, valid_name)
        
        self.assertTrue(result.success, "Company creation was unsuccessful")
        self.assertTrue(user.is_company_owner, "User was not assigned as a company owner")
        self.assertEqual(user.company_id.company_id, result.payload.company_id)
