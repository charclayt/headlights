# This is an auto-generated Django model module.

# Remember to migrate to the database using the following:
#   manage.py makemigrations <app_name>
#   manage.py migrate <app_name>

# If this doesn't work you may need to reset your migrations
#   delete all files in the migrations folder except __init__.py
#   run python manage.py migrate --fake <app_name> zero

# Changes made to the database can turned into models using the following:
#   python manage.py inspectdb > models.py

from django.contrib.auth.models import User
from django.db import models

class Claim(models.Model):
    claim_id = models.AutoField(db_column='ClaimID', primary_key=True)  # Field name made lowercase.
    settlement_value = models.FloatField(db_column='SettlementValue', blank=True, null=True)  # Field name made lowercase.
    accident_type = models.CharField(db_column='AccidentType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    injury_prognosis = models.IntegerField(db_column='InjuryPrognosis', blank=True, null=True)  # Field name made lowercase.
    special_health_expenses = models.FloatField(db_column='SpecialHealthExpenses', blank=True, null=True)  # Field name made lowercase.
    special_reduction = models.FloatField(db_column='SpecialReduction', blank=True, null=True)  # Field name made lowercase.
    special_overage = models.FloatField(db_column='SpecialOverage', blank=True, null=True)  # Field name made lowercase.
    general_rest = models.FloatField(db_column='GeneralRest', blank=True, null=True)  # Field name made lowercase.
    special_additional_injury = models.FloatField(db_column='SpecialAdditionalInjury', blank=True, null=True)  # Field name made lowercase.
    special_earnings_loss = models.FloatField(db_column='SpecialEarningsLoss', blank=True, null=True)  # Field name made lowercase.
    special_usage_loss = models.FloatField(db_column='SpecialUsageLoss', blank=True, null=True)  # Field name made lowercase.
    special_medications = models.FloatField(db_column='SpecialMedications', blank=True, null=True)  # Field name made lowercase.
    special_asset_damage = models.FloatField(db_column='SpecialAssetDamage', blank=True, null=True)  # Field name made lowercase.
    special_rehabilitation = models.FloatField(db_column='SpecialRehabilitation', blank=True, null=True)  # Field name made lowercase.
    special_fixes = models.FloatField(db_column='SpecialFixes', blank=True, null=True)  # Field name made lowercase.
    general_fixed = models.FloatField(db_column='GeneralFixed', blank=True, null=True)  # Field name made lowercase.
    general_uplift = models.FloatField(db_column='GeneralUplift', blank=True, null=True)  # Field name made lowercase.
    special_loaner_vehicle = models.FloatField(db_column='SpecialLoanerVehicle', blank=True, null=True)  # Field name made lowercase.
    special_trip_costs = models.FloatField(db_column='SpecialTripCosts', blank=True, null=True)  # Field name made lowercase.
    special_journey_expenses = models.FloatField(db_column='SpecialJourneyExpenses', blank=True, null=True)  # Field name made lowercase.
    special_therapy = models.FloatField(db_column='SpecialTherapy', blank=True, null=True)  # Field name made lowercase.
    exceptional_circumstances = models.IntegerField(db_column='ExceptionalCircumstances', blank=True, null=True)  # Field name made lowercase.
    minor_psychological_injury = models.IntegerField(db_column='MinorPsychologicalInjury', blank=True, null=True)  # Field name made lowercase.
    dominant_injury = models.CharField(db_column='DominantInjury', max_length=255, blank=True, null=True)  # Field name made lowercase.
    whiplash = models.IntegerField(db_column='Whiplash', blank=True, null=True)  # Field name made lowercase.
    vehicle_type = models.CharField(db_column='VehicleType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    weather_conditions = models.CharField(db_column='WeatherConditions', max_length=255, blank=True, null=True)  # Field name made lowercase.
    accident_date = models.IntegerField(db_column='AccidentDate', blank=True, null=True)  # Field name made lowercase.
    claim_date = models.IntegerField(db_column='ClaimDate', blank=True, null=True)  # Field name made lowercase.
    vehicle_age = models.IntegerField(db_column='VehicleAge', blank=True, null=True)  # Field name made lowercase.
    driver_age = models.IntegerField(db_column='DriverAge', blank=True, null=True)  # Field name made lowercase.
    number_of_passengers = models.IntegerField(db_column='NumberOfPassengers', blank=True, null=True)  # Field name made lowercase.
    accident_description = models.CharField(db_column='AccidentDescription', max_length=255, blank=True, null=True)  # Field name made lowercase.
    injury_description = models.CharField(db_column='InjuryDescription', max_length=255, blank=True, null=True)  # Field name made lowercase.
    police_report_filed = models.IntegerField(db_column='PoliceReportFiled', blank=True, null=True)  # Field name made lowercase.
    witness_present = models.IntegerField(db_column='WitnessPresent', blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Claim'


class Feedback(models.Model):
    feedback_id = models.AutoField(db_column='FeedbackID', primary_key=True)  # Field name made lowercase.
    user_id = models.ForeignKey(User, models.PROTECT, db_column='UserID', blank=True, null=True)  # Field name made lowercase.
    rating = models.IntegerField(db_column='Rating', blank=True, null=True)  # Field name made lowercase.
    notes = models.CharField(db_column='Notes', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Feedback'


class DatabaseLog(models.Model):
    database_log_id = models.AutoField(db_column='DatabaseLogID', primary_key=True)  
    log_time = models.DateTimeField(db_column='LogTime', blank=True, null=True)  
    user_id = models.ForeignKey(UserProfile, models.PROTECT, db_column='UserID', blank=True, null=True)  
    affected_table_id = models.ForeignKey('TableLookup', models.PROTECT, db_column='AffectedTableID', blank=True, null=True)  
    operation_performed = models.ForeignKey('OperationLookup', models.PROTECT, db_column='OperationPerformed', blank=True, null=True)  
    successful = models.BooleanField(db_column='Successful', blank=True, null=True)  
    notes = models.CharField(db_column='Notes', max_length=255, blank=True, null=True)  

    class Meta:
        managed = True
        db_table = 'DatabaseLog'


class Model(models.Model): # I think we should rename this as model is referenced a lot throughout Django
    model_id = models.AutoField(db_column='ModelID', primary_key=True)  # Field name made lowercase.
    model_name = models.CharField(db_column='ModelName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    notes = models.CharField(db_column='Notes', max_length=255, blank=True, null=True)  # Field name made lowercase.
    filepath = models.CharField(db_column='FilePath', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Model'


class OperationLookup(models.Model):
    operation_id = models.AutoField(db_column='OperationID', primary_key=True)  # Field name made lowercase.
    operation_name = models.CharField(db_column='OperationName', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'OperationLookup'


class TableLookup(models.Model):
    table_id = models.AutoField(db_column='TableID', primary_key=True)  # Field name made lowercase.
    table_name = models.CharField(db_column='TableName', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'TableLookup'


class TrainingDataset(models.Model):
    training_dataset_id = models.AutoField(db_column='TrainingDatasetID', primary_key=True)  # Field name made lowercase.
    claim_id = models.ForeignKey(Claim, models.PROTECT, db_column='ClaimID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'TrainingDataset'


class UploadedRecord(models.Model):
    uploaded_record_id = models.AutoField(db_column='UploadedRecordID', primary_key=True)  # Field name made lowercase.
    user_id = models.ForeignKey(User, models.PROTECT, db_column='UserID', blank=True, null=True)  # Field name made lowercase.
    claim_id = models.ForeignKey(Claim, models.PROTECT, db_column='ClaimID', blank=True, null=True)  # Field name made lowercase.
    feedback_id = models.ForeignKey(Feedback, models.PROTECT, db_column='FeedbackID', blank=True, null=True)  # Field name made lowercase.
    model_id = models.ForeignKey(Model, models.PROTECT, db_column='ModelID', blank=True, null=True)  # Field name made lowercase.
    predicted_settlement = models.FloatField(db_column='PredictedSettlement', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'UploadedRecord'
