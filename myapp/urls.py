"""
URL configuration for desd project.
"""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    
    # ML-related API endpoints
    path("api/models/", views.models_list, name="models_list"),
    path("api/predict/", views.predict, name="predict"),
    path("api/submit-claim/", views.submit_claim, name="submit_claim"),
    path("api/upload-model/", views.upload_model, name="upload_model"),
    # Additional endpoints could be added here as needed
    # For example:
    # path("api/evaluate-model/<int:model_id>/", views.evaluate_model, name="evaluate_model"),
]