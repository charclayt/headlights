from django.contrib import admin
from .models import Claim, Feedback, DatabaseLog, PredictionModel, OperationLookup, TableLookup, TrainingDataset, UploadedRecord, UserProfile, Company, ContactInfo, FinanceReport

# Register your models here.
@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = (
        "ClaimID", "SettlementValue", "AccidentType", "InjuryPrognosis",
        "SpecialHealthExpenses", "SpecialReduction", "SpecialOverage", "GeneralRest",
        "SpecialAdditionalInjury", "SpecialEarningsLoss", "SpecialUsageLoss",
        "SpecialMedications", "SpecialAssetDamage", "SpecialRehabilitation", "SpecialFixes",
        "GeneralFixed", "GeneralUplift", "SpecialLoanerVehicle", "SpecialTripCosts",
        "SpecialJourneyExpenses", "SpecialTherapy", "ExceptionalCircumstances",
        "MinorPsychologicalInjury", "DominantInjury", "Whiplash", "VehicleType",
        "WeatherConditions", "AccidentDate", "ClaimDate", "VehicleAge",
        "DriverAge", "NumberOfPassengers", "AccidentDescription", "InjuryDescription",
        "PoliceReportFiled", "WitnessPresent", "Gender"
    )

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback_id', 'user_id', 'rating', 'notes')

@admin.register(DatabaseLog)
class LogAdmin(admin.ModelAdmin):
    list_display = ('database_log_id', 'log_time', 'user_id', 'affected_table_id', 'operation_performed', 'successful', 'notes')

@admin.register(PredictionModel)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('model_id', 'model_name', 'notes', 'filepath', 'price_per_prediction')

@admin.register(OperationLookup)
class OperationLookupAdmin(admin.ModelAdmin):
    list_display = ('operation_id', 'operation_name')

@admin.register(TableLookup)
class TableLookupAdmin(admin.ModelAdmin):
    list_display = ('table_id', 'table_name')

@admin.register(TrainingDataset)
class TrainingDatasetAdmin(admin.ModelAdmin):
    list_display = ('training_dataset_id', 'claim_id')

@admin.register(UploadedRecord)
class UploadedRecordAdmin(admin.ModelAdmin):
    list_display = ('uploaded_record_id', 'user_id', 'claim_id', 'feedback_id', 'model_id', 'predicted_settlement', 'upload_date')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_profile_id', 'auth_id', 'contact_info_id', 'company_id')
    
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_id', 'contact_info_id', 'name')
    
@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('contact_info_id', 'phone', 'email', 'address')
    
@admin.register(FinanceReport)
class FinanceReportAdmin(admin.ModelAdmin):
    list_display = ('finance_report_id', 'user_id', 'year', 'month', 'cost_incurred', 'generated_invoice')
    
