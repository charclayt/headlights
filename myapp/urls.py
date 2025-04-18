"""
URL configuration for desd project.
"""
from django.urls import path

from myapp.views.CustomerDashBoardView import CustomerDashboardView, ClaimUploadView, PredictionFeedbackView, ProcessClaimsFileView
from myapp.views.IndexView import IndexView
from myapp.views.MLDashboardView import MLDashboardView, UploadModelView
from myapp.views.AccountManagementView import AccountCreationView, AccountContactDetailsView
from myapp.views.FinanceDashboardViews import FinanceDashboardView, CompanyDetailsView, CompanyManageEmployeesView, download_invoice


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("ml/", MLDashboardView.as_view() , name="ml_dashboard"),
    
    # Customer dashboard URLs
    path("customer/", CustomerDashboardView.as_view(), name="customer_dashboard"),  
    path("customer/record-upload/", ClaimUploadView.as_view(), name="upload_claims"),
    path("customer/record-upload/<int:ignore_validation>/", ClaimUploadView.as_view(), name="upload_claims"),
    path("customer/prediction-feedback/", PredictionFeedbackView.as_view(), name="prediction_feedback"),
    path("customer/claims-processing/", ProcessClaimsFileView.as_view(), name="claims_preprocessing"),
    path("customer/claims-processing/<int:ignore_validation>/", ProcessClaimsFileView.as_view(), name="claims_preprocessing"),
    
    # Account management URLs
    path("account/create/", AccountCreationView.as_view(), name="account_creation"),
    path("account/contact-details/", AccountContactDetailsView.as_view(), name="contact_details"),
    
    # Finance URLs
    path("finance/", FinanceDashboardView.as_view(), name="finance_dashboard"),
    path("finance/company-details/", CompanyDetailsView.as_view(), name="company_details"),
    path("finance/manage-employees/", CompanyManageEmployeesView.as_view(), name="company_manage_employees"),
    path("finance/invoice-download/<int:invoice_id>/", download_invoice, name="invoice_download"),
    
    # ML-related API endpoints
    path("api/upload-model/", UploadModelView.as_view(), name="upload_model"),
    # Additional endpoints could be added here as needed
]
