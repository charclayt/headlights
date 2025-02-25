"""
URL configuration for desd project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from myapp import views as myapp_views  # Import myapp views directly

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', RedirectView.as_view(url='/app/')),
    path('app/', include('myapp.urls')),
    
    # Add direct API routes at the root level
    path('api/models/', myapp_views.models_list, name="api_models_list"),
    path('api/predict/', myapp_views.predict, name="api_predict"),
    path('api/submit-claim/', myapp_views.submit_claim, name="api_submit_claim"),
]