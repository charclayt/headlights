from django.test import TestCase
from django.contrib.auth.models import Group

from myapp.tests.test_BaseView import BaseViewTest
from myapp.tests.config import Views, Templates, TestData
from myapp.models import UserProfile

class ContactDetailsPageTest(BaseViewTest, TestCase):

    URL = Views.CONTACT_DETAILS
    TEMPLATE = Templates.CONTACT_DETAILS

    def setUp(self):
        end_user_group = Group.objects.create(pk=UserProfile.GroupIDs.END_USER_ID, name="end user")
        end_user_group.save()
        
        return BaseViewTest.setUp(self)

    def test_get_view(self):
        unique_name = TestData.NAME+"CONTACT_DETAILS_VIEW_TEST"
        UserProfile.create_account(unique_name, TestData.EMAIL, TestData.PASSWORD, UserProfile.GroupIDs.END_USER_ID)
        self.client.login(username=unique_name, password=TestData.PASSWORD)
        
        BaseViewTest.test_get_view(self)
        
    def test_edit_contact_details(self):
        unique_name = TestData.NAME+"EDIT_CONTACT_DETAILS_TEST"
        userProfile: UserProfile = UserProfile.create_account(unique_name, TestData.EMAIL, TestData.PASSWORD, UserProfile.GroupIDs.END_USER_ID).payload
        self.client.login(username=unique_name, password=TestData.PASSWORD)
        
        new_email = TestData.EMAIL+"123"
        payload = {"email": new_email, "phone": TestData.PHONE, "address": TestData.ADDRESS}
        response = BaseViewTest._test_post_view_response(self, payload=payload)
        
        userProfile = UserProfile.objects.get(user_profile_id=userProfile.pk)
        
        self.assertEqual(response.templates[0].name, self.TEMPLATE)
        self.assertEqual(userProfile.contact_info_id.email, new_email)
