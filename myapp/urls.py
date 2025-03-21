"""
URL configuration for desd project.
"""
from django.urls import path

from myapp.views.IndexView import IndexView
from myapp.views.MLDashboardView import MLDashboardView, ModelListView, UploadModelView
from myapp.views.CustomerDashBoardView import CustomerDashboardView, ClaimUploadView
from myapp.views.AccountManagementView import AccountCreationView, AccountContactDetailsView


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("ml/", MLDashboardView.as_view() , name="ml_dashboard"),
    
    # Customer dashboard URLs
    path("customer/", CustomerDashboardView.as_view(), name="customer_dashboard"),  
    path("customer/record-upload/", ClaimUploadView.as_view(), name="upload_claims"),
    path("customer/record-upload/<int:ignore_validation>/", ClaimUploadView.as_view(), name="upload_claims"),
    
    # Account management URLs
    path("account/create/", AccountCreationView.as_view(), name="account_creation"),
    path("account/contact-details", AccountContactDetailsView.as_view(), name="contact_details"),
    
    # ML-related API endpoints
    path("api/models/", ModelListView.as_view(), name="models_list"),
    path("api/upload-model/", UploadModelView.as_view(), name="upload_model"),
    # Additional endpoints could be added here as needed
]
