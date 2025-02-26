from django.contrib import admin
from .models import Bod, Claim, Feedback, Log, Model, OperationLookup, PermissionLevel, TableLookup, TrainingDataset, UploadedRecord 

# Register your models here.
@admin.register(Bod)
class BodAdmin(admin.ModelAdmin):
    list_display = ('bod_id', 'username', 'permission_id')

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('claim_id', 'settlement_value', 'accident_type', 'injury_prognosis', 'special_health_expenses', 'special_reduction', 'special_overage', 'general_rest', 'special_additional_injury', 'special_earnings_loss', 'special_usage_loss', 'special_medications', 'special_asset_damage', 'special_rehabilitation', 'special_fixes', 'general_fixed', 'general_uplift', 'special_loaner_vehicle', 'special_trip_costs', 'special_journey_expenses', 'special_therapy', 'exceptional_circumstances', 'minor_psychological_injury', 'dominant_injury', 'whiplash', 'vehicle_type', 'weather_conditions', 'accident_date', 'claim_date', 'vehicle_age', 'driver_age', 'number_of_passengers', 'accident_description', 'injury_description', 'police_report_filed', 'witness_present', 'gender')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback_id', 'bod_id', 'rating', 'notes')

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('log_id', 'log_time', 'bod_id', 'affected_table_id', 'operation_performed', 'successful', 'notes')

@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('model_id', 'model_name', 'notes', 'filepath')

@admin.register(OperationLookup)
class OperationLookupAdmin(admin.ModelAdmin):
    list_display = ('operation_id', 'operation_name')

@admin.register(PermissionLevel)
class PermissionLevelAdmin(admin.ModelAdmin):
    list_display = ('permission_id', 'system_permission_level', 'ml_permission_level', 'notes')

@admin.register(TableLookup)
class TableLookupAdmin(admin.ModelAdmin):
    list_display = ('table_id', 'table_name')

@admin.register(TrainingDataset)
class TrainingDatasetAdmin(admin.ModelAdmin):
    list_display = ('training_dataset_id', 'claim_id')

@admin.register(UploadedRecord)
class UploadedRecordAdmin(admin.ModelAdmin):
    list_display = ('uploaded_record_id', 'bod_id', 'claim_id', 'feedback_id', 'model_id', 'predicted_settlement')
