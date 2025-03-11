"""
URL configuration for desd project.
"""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("ml/", views.ml_dashboard, name="ml_dashboard"),
    
    # Testing urls for dashboard features, to be replaced by more appropriate urls later
    path("test/record-upload", views.record_upload, name="upload"),
    
    # ML-related API endpoints
    path("api/models/", views.models_list, name="models_list"),
    path("api/upload-model/", views.upload_model, name="upload_model"),
    # Additional endpoints could be added here as needed
]
