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
from django.conf import settings
from django.conf.urls.static import static

from desd.settings import DEBUG
from myapp.views.ErrorView import Error_400, Error_403, Error_404, Error_500
from myapp.views.MLDashboardView import UploadModelView

handler400 = Error_400.as_view()
handler403 = Error_403.as_view()
handler404 = Error_404.as_view()
handler500 = Error_500.as_view()

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    
    # Root redirects to app/
    path('', RedirectView.as_view(url='/app/')),
    
    # Include myapp URLs under both /app/ and /myapp/ paths
    path('app/', include('myapp.urls')),
    path('myapp/', include('myapp.urls')),  # Added this line to handle /myapp/ URLs
    
    # Add direct API routes at the root level
    path('api/upload-model/', UploadModelView.as_view(), name="api_upload_model"),
]

# Add media URL to serve uploaded files
if DEBUG:
    urlpatterns.extend([
        path('400', handler400, name='400'),
        path('403', handler403, name='403'),
        path('404', handler404, name='404'),
        path('500', handler500, name='500')]
    )
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
