from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group, Permission

import logging

from myapp.tests.test_BaseView import BaseViewTest
from myapp.tests.config import Views, Templates, TestData
from myapp.models import UserProfile

class FinanceDashboardTest(BaseViewTest, TestCase):

    URL = Views.FINANCE_DASHBOARD
    TEMPLATE = Templates.FINANCE

    def setUp(self):
        logging.disable(logging.ERROR)

        end_user_group = Group.objects.create(pk=UserProfile.GroupIDs.END_USER_ID, name="end user")
        end_user_group.save()
        
        finance_group = Group.objects.create(pk=UserProfile.GroupIDs.FINANCE_ID, name="finance")
        finance_permission = Permission.objects.get(codename="view_financereport")
        finance_group.permissions.add(finance_permission)
        finance_group.save()
        
        BaseViewTest.setUp(self)

        self.client.logout()
        self.TEMPLATE = Templates.LOGIN
        BaseViewTest.test_get_view(self)
        
        unique_name = TestData.NAME+"FINANCE_DASHBOARD_GET_VIEW_TEST"
        UserProfile.create_account(unique_name, TestData.EMAIL, TestData.PASSWORD, UserProfile.GroupIDs.FINANCE_ID)
        self.client.login(username=unique_name, password=TestData.PASSWORD)
        self.TEMPLATE = Templates.FINANCE

    def test_get_view(self):
        BaseViewTest.test_get_view(self)

    def test_post_view_success(self):
        payload = {
            'company': 1,
            'month': '4',
            'year': '2025',
        }

        BaseViewTest._test_post_view_response(self, payload=payload)

    def test_post_view_failure_no_content(self):
        BaseViewTest._test_post_view_response(self, status=400)

    def test_post_view_failure_bad_company(self):
        payload= {
            'company': 999,
            'month': '4',
            'year': '2025',
        }
        BaseViewTest._test_post_view_response(self, status=400, payload=payload)

    def test_invoice_download_success(self):
        response = self.client.get(reverse('invoice_download', args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment; filename=invoice_1.pdf', response['Content-Disposition'])

        self.assertTrue(response.content.startswith(b'%PDF'))

    def test_invoice_download_failure(self):
        response = self.client.get(reverse('invoice_download', args=[999]))

        self.assertContains(response, 'Failed to download invoice', status_code=400)
