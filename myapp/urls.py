"""
URL configuration for desd project.
"""
from django.contrib import admin
from django.urls import path, include
from myapp import views as myapp_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", myapp_views.index, name="index"),
    
    # ML-related API endpoints
    path("api/models/", myapp_views.models_list, name="models_list"),
    path("api/predict/", myapp_views.predict, name="predict"),
    path("api/submit-claim/", myapp_views.submit_claim, name="submit_claim"),
]