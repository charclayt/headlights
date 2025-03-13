from django.urls import path
from ml_app.views import MLDashboardView, ModelListView, UploadModelView, HealthCheckView

urlpatterns = [
    path("", MLDashboardView.as_view(), name="ml_dashboard"),
    path("api/models/", ModelListView.as_view(), name="models_list"),
    path("api/upload-model/", UploadModelView.as_view(), name="upload_model"),
    path("health/", HealthCheckView.as_view(), name="health_check"),
]