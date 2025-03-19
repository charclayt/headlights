from django.contrib import admin
from .models import PredictionModel

@admin.register(PredictionModel)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('model_id', 'model_name', 'model_type', 'notes', 'filepath', 'price_per_prediction')
