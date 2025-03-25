from django.test import TestCase
from django.contrib.auth.models import Group, Permission

from myapp.tests.test_BaseView import BaseViewTest
from myapp.tests.config import Views, Templates, TestData
from myapp.models import UserProfile

class FinanceDashboardTest(BaseViewTest, TestCase):

    URL = Views.FINANCE_DASHBOARD
    TEMPLATE = Templates.FINANCE

    def setUp(self):
        end_user_group = Group.objects.create(pk=UserProfile.GroupIDs.END_USER_ID, name="end user")
        end_user_group.save()
        
        finance_group = Group.objects.create(pk=UserProfile.GroupIDs.FINANCE_ID, name="finance")
        finance_permission = Permission.objects.get(codename="view_financereport")
        finance_group.permissions.add(finance_permission)
        finance_group.save()
        
        return BaseViewTest.setUp(self)

    def test_get_view(self):
        self.client.logout()
        self.TEMPLATE = Templates.LOGIN
        BaseViewTest.test_get_view(self)
        
        unique_name = TestData.NAME+"FINANCE_DASHBOARD_GET_VIEW_TEST"
        UserProfile.create_account(unique_name, TestData.EMAIL, TestData.PASSWORD, UserProfile.GroupIDs.FINANCE_ID)
        self.client.login(username=unique_name, password=TestData.PASSWORD)
        self.TEMPLATE = Templates.FINANCE
        BaseViewTest.test_get_view(self)
