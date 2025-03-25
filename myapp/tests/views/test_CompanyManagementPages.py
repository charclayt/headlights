from django.test import TestCase
from django.contrib.auth.models import Group, Permission

import json

from myapp.tests.test_BaseView import BaseViewTest
from myapp.tests.config import Views, Templates, TestData
from myapp.models import UserProfile, Company

class CompanyDetailsTest(BaseViewTest, TestCase):

    URL = Views.COMPANY_DETAILS
    TEMPLATE = Templates.COMPANY_DETAILS

    def setUp(self):
        self.TEMPLATE = Templates.COMPANY_DETAILS
        
        end_user_group = Group.objects.create(pk=UserProfile.GroupIDs.END_USER_ID, name="end user")
        end_user_group.save()
        
        finance_group = Group.objects.create(pk=UserProfile.GroupIDs.FINANCE_ID, name="finance")
        finance_permission = Permission.objects.get(codename="view_financereport")
        finance_group.permissions.add(finance_permission)
        finance_group.save()
        
        return BaseViewTest.setUp(self)

    def test_get_view(self):
        unique_name = TestData.NAME+"COMPANY_DETAILS_VIEW_TEST_FAIL_1"
        self.TEMPLATE = Templates.LOGIN
        UserProfile.create_account(unique_name, TestData.EMAIL, TestData.PASSWORD, UserProfile.GroupIDs.END_USER_ID)    
        self.client.login(username=unique_name, password=TestData.PASSWORD)
        BaseViewTest.test_get_view(self)
        
        unique_name = TestData.NAME+"COMPANY_DETAILS_VIEW_TEST_FAIL_2"
        self.TEMPLATE = Templates.HOME
        user = UserProfile.create_account(unique_name, TestData.EMAIL, TestData.PASSWORD, UserProfile.GroupIDs.FINANCE_ID).payload
        self.client.login(username=unique_name, password=TestData.PASSWORD)
        BaseViewTest.test_get_view(self)
        
        self.TEMPLATE = Templates.COMPANY_DETAILS
        Company.create_new_company(user, unique_name)
        self.client.login(username=unique_name, password=TestData.PASSWORD)
        BaseViewTest.test_get_view(self)
        
    def test_edit_company_details(self):
        unique_name = TestData.NAME+"EDIT_COMPANY_DETAILS_TEST"
        userProfile: UserProfile = UserProfile.create_account(unique_name, TestData.EMAIL, TestData.PASSWORD, UserProfile.GroupIDs.FINANCE_ID).payload
        company = Company.create_new_company(userProfile, unique_name).payload
        self.client.login(username=unique_name, password=TestData.PASSWORD)
        
        new_email = TestData.EMAIL+"123"
        new_name = unique_name+"123"
        payload = {"companyName":new_name, "email": new_email, "phone": TestData.PHONE, "address": TestData.ADDRESS}
        response = BaseViewTest._test_post_view_response(self, payload=payload)
        
        company = Company.objects.get(company_id=company.pk)
        
        self.assertEqual(response.templates[0].name, self.TEMPLATE)
        self.assertEqual(company.contact_info_id.email, new_email)
        self.assertEqual(company.name, new_name)
        

class CompanyEmployeeManagementTest(BaseViewTest, TestCase):
    
    URL = Views.COMPANY_MANAGE_EMPLOYEES
    TEMPLATE = Templates.COMPANY_USER_MANAGEMENT
    
    def setUp(self):
        self.TEMPLATE = Templates.COMPANY_USER_MANAGEMENT
        
        end_user_group = Group.objects.create(pk=UserProfile.GroupIDs.END_USER_ID, name="end user")
        end_user_group.save()
        
        finance_group = Group.objects.create(pk=UserProfile.GroupIDs.FINANCE_ID, name="finance")
        finance_permission = Permission.objects.get(codename="view_financereport")
        finance_group.permissions.add(finance_permission)
        finance_group.save()
        
        return BaseViewTest.setUp(self)
    
    def test_get_view(self):
        unique_name = TestData.NAME+"COMPANY_EMPLOYEES_VIEW_TEST_FAIL_1"
        self.TEMPLATE = Templates.LOGIN
        UserProfile.create_account(unique_name, TestData.EMAIL, TestData.PASSWORD, UserProfile.GroupIDs.END_USER_ID)    
        self.client.login(username=unique_name, password=TestData.PASSWORD)
        BaseViewTest.test_get_view(self)
        
        unique_name = TestData.NAME+"COMPANY_EMPLOYEES_VIEW_TEST_FAIL_2"
        self.TEMPLATE = Templates.HOME
        user = UserProfile.create_account(unique_name, TestData.EMAIL, TestData.PASSWORD, UserProfile.GroupIDs.FINANCE_ID).payload
        self.client.login(username=unique_name, password=TestData.PASSWORD)
        BaseViewTest.test_get_view(self)
        
        self.TEMPLATE = Templates.COMPANY_USER_MANAGEMENT
        Company.create_new_company(user, unique_name)
        self.client.login(username=unique_name, password=TestData.PASSWORD)
        BaseViewTest.test_get_view(self)
        
    def test_add_and_remove_employee(self):
        owner_name = TestData.NAME+"COMPANY_EMPLOYEES_ADD_REMOVE_TEST_OWNER"
        company_owner: UserProfile = UserProfile.create_account(owner_name, TestData.EMAIL, TestData.PASSWORD, UserProfile.GroupIDs.FINANCE_ID).payload
        company = Company.create_new_company(company_owner, owner_name).payload
        self.client.login(username=owner_name, password=TestData.PASSWORD)
        
        employee_name = TestData.NAME+"COMPANY_EMPLOYEES_ADD_REMOVE_TEST_EMPLOYEE"
        employee_user = UserProfile.create_account(employee_name, TestData.EMAIL, TestData.PASSWORD, UserProfile.GroupIDs.END_USER_ID).payload
        
        payload = json.dumps({'action': 'add', 'user': employee_user.user_profile_id})
        response = BaseViewTest._test_post_view_response(self, payload=payload, content_type="application/json")
        self.assertJSONEqual(
            response.content,
            {
                'status': 'success',
            }
        )
        
        employee_user = UserProfile.objects.get(user_profile_id=employee_user.user_profile_id)
        self.assertEqual(employee_user.company_id.company_id, company.company_id)
        
        payload = json.dumps({'action': 'remove', 'user': employee_user.user_profile_id})
        response = BaseViewTest._test_post_view_response(self, payload=payload, content_type="application/json")
        self.assertJSONEqual(
            response.content,
            {
                'status': 'success',
            }
        )
        
        employee_user = UserProfile.objects.get(user_profile_id=employee_user.user_profile_id)
        self.assertEqual(employee_user.company_id, None)
