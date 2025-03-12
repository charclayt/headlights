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
from datetime import date
from .utility.SimpleResults import SimpleResult, SimpleResultWithPayload
import pandas as pd


class Claim(models.Model):
    claim_id = models.AutoField(db_column='ClaimID', primary_key=True)  
    settlement_value = models.FloatField(db_column='SettlementValue', blank=True, null=True)  
    accident_type = models.CharField(db_column='AccidentType', max_length=255, blank=True, null=True)  
    injury_prognosis = models.IntegerField(db_column='InjuryPrognosis', blank=True, null=True)  
    special_health_expenses = models.FloatField(db_column='SpecialHealthExpenses', blank=True, null=True)  
    special_reduction = models.FloatField(db_column='SpecialReduction', blank=True, null=True)  
    special_overage = models.FloatField(db_column='SpecialOverage', blank=True, null=True)  
    general_rest = models.FloatField(db_column='GeneralRest', blank=True, null=True)  
    special_additional_injury = models.FloatField(db_column='SpecialAdditionalInjury', blank=True, null=True)  
    special_earnings_loss = models.FloatField(db_column='SpecialEarningsLoss', blank=True, null=True)  
    special_usage_loss = models.FloatField(db_column='SpecialUsageLoss', blank=True, null=True)  
    special_medications = models.FloatField(db_column='SpecialMedications', blank=True, null=True)  
    special_asset_damage = models.FloatField(db_column='SpecialAssetDamage', blank=True, null=True)  
    special_rehabilitation = models.FloatField(db_column='SpecialRehabilitation', blank=True, null=True)  
    special_fixes = models.FloatField(db_column='SpecialFixes', blank=True, null=True)  
    general_fixed = models.FloatField(db_column='GeneralFixed', blank=True, null=True)  
    general_uplift = models.FloatField(db_column='GeneralUplift', blank=True, null=True)  
    special_loaner_vehicle = models.FloatField(db_column='SpecialLoanerVehicle', blank=True, null=True)  
    special_trip_costs = models.FloatField(db_column='SpecialTripCosts', blank=True, null=True)  
    special_journey_expenses = models.FloatField(db_column='SpecialJourneyExpenses', blank=True, null=True)  
    special_therapy = models.FloatField(db_column='SpecialTherapy', blank=True, null=True)  
    exceptional_circumstances = models.IntegerField(db_column='ExceptionalCircumstances', blank=True, null=True)  
    minor_psychological_injury = models.IntegerField(db_column='MinorPsychologicalInjury', blank=True, null=True)  
    dominant_injury = models.CharField(db_column='DominantInjury', max_length=255, blank=True, null=True)  
    whiplash = models.IntegerField(db_column='Whiplash', blank=True, null=True)  
    vehicle_type = models.CharField(db_column='VehicleType', max_length=255, blank=True, null=True)  
    weather_conditions = models.CharField(db_column='WeatherConditions', max_length=255, blank=True, null=True)  
    accident_date = models.IntegerField(db_column='AccidentDate', blank=True, null=True)  
    claim_date = models.IntegerField(db_column='ClaimDate', blank=True, null=True)  
    vehicle_age = models.IntegerField(db_column='VehicleAge', blank=True, null=True)  
    driver_age = models.IntegerField(db_column='DriverAge', blank=True, null=True)  
    number_of_passengers = models.IntegerField(db_column='NumberOfPassengers', blank=True, null=True)  
    accident_description = models.CharField(db_column='AccidentDescription', max_length=255, blank=True, null=True)  
    injury_description = models.CharField(db_column='InjuryDescription', max_length=255, blank=True, null=True)  
    police_report_filed = models.IntegerField(db_column='PoliceReportFiled', blank=True, null=True)  
    witness_present = models.IntegerField(db_column='WitnessPresent', blank=True, null=True)  
    gender = models.CharField(db_column='Gender', max_length=255, blank=True, null=True)  

    class Meta:
        managed = True
        db_table = 'Claim'
    
    def create_claim_from_series(datarow: pd.Series):
        claim = Claim()
        claim.settlement_value = datarow['SettlementValue']
        claim.accident_type = datarow['AccidentType']
        claim.injury_prognosis = datarow['InjuryPrognosis']
        claim.special_health_expenses = datarow['SpecialHealthExpenses']
        claim.special_reduction = datarow['SpecialReduction']
        claim.special_overage = datarow['SpecialOverage']
        claim.general_rest = datarow['GeneralRest']
        claim.special_additional_injury = datarow['SpecialAdditionalInjury']
        claim.special_earnings_loss = datarow['SpecialEarningsLoss']
        claim.special_usage_loss = datarow['SpecialUsageLoss']
        claim.special_medications = datarow['SpecialMedications']
        claim.special_asset_damage = datarow['SpecialAssetDamage']
        claim.special_rehabilitation = datarow['SpecialRehabilitation']
        claim.special_fixes = datarow['SpecialFixes']
        claim.general_fixed = datarow['GeneralFixed']
        claim.general_uplift = datarow['GeneralUplift']
        claim.special_loaner_vehicle = datarow['SpecialLoanerVehicle']
        claim.special_trip_costs = datarow['SpecialTripCosts']
        claim.special_journey_expenses = datarow['SpecialJourneyExpenses']
        claim.special_therapy = datarow['SpecialTherapy']
        claim.exceptional_circumstances = datarow['ExceptionalCircumstances']
        claim.minor_psychological_injury = datarow['MinorPsychologicalInjury']
        claim.dominant_injury = datarow['DominantInjury']
        claim.whiplash = datarow['Whiplash']
        claim.vehicle_type = datarow['VehicleType']
        claim.weather_conditions = datarow['WeatherConditions']
        claim.accident_date = datarow['AccidentDate']
        claim.claim_date = datarow['ClaimDate']
        claim.vehicle_age = datarow['VehicleAge']
        claim.driver_age = datarow['DriverAge']
        claim.number_of_passengers = datarow['NumberOfPassengers']
        claim.accident_description = datarow['AccidentDescription']
        claim.injury_description = datarow['InjuryDescription']
        claim.police_report_filed = datarow['PoliceReportFiled']
        claim.witness_present = datarow['WitnessPresent']
        claim.gender = datarow['Gender']
        
        return claim
    
    @staticmethod
    def create_claims_from_dataframe(df: pd.DataFrame) -> list:
        claims = []
        for index, datarow in df.iterrows():
            claims.append(Claim.create_claim_from_series(datarow))
            
        return claims
    
    @staticmethod
    def validate_columns(df: pd.DataFrame) -> SimpleResult:
        result = SimpleResult()
        
        attributes = Claim._meta.get_fields()
        db_column_names = []
        for attr in attributes:
            if hasattr(attr, 'db_column'):
                db_column_names.append(attr.db_column)
        db_column_names.pop(0) # Remove the primary key
        
        csv_columns = df.columns

        excess_columns = []
        for column in csv_columns:
            if column in db_column_names:
                db_column_names.remove(column)
            else:
                excess_columns.append(column)
                
        missing_columns = db_column_names[:]

        if len(missing_columns) > 0 :
            result.add_error_message_and_mark_unsuccessful(f"Missing Columns: {', '.join(missing_columns)}")
            
        if len(excess_columns) > 0:
            result.add_error_message_and_mark_unsuccessful(f"Excess Columns: {', '.join(missing_columns)}")
            
        return result

class ContactInfo(models.Model):
    contact_info_id = models.AutoField(db_column='ContactInfoID', primary_key=True)
    phone = models.CharField(db_column='Phone', max_length=255, blank=True, null=True)
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)
    address = models.CharField(db_column='Address', max_length=255, blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'ContactInfo'
    

class Company(models.Model):
    company_id = models.AutoField(db_column='CompanyID', primary_key=True)
    contact_info_id = models.ForeignKey(ContactInfo, models.PROTECT, db_column='ContactInfoID', blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'Company'
    

class UserProfile(models.Model):
    user_profile_id = models.AutoField(db_column='UserProfileID', primary_key=True)
    auth_id = models.ForeignKey(User, models.PROTECT, db_column='AuthID', blank=True, null=True)
    contact_info_id = models.ForeignKey(ContactInfo, models.PROTECT, db_column='ContactInfoID', blank=True, null=True)
    company_id = models.ForeignKey(Company, models.PROTECT, db_column='CompanyID', blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'UserProfile'


class FinanceReport(models.Model):
    finance_report_id = models.AutoField(db_column='FinanceReportID', primary_key=True)
    user_id = models.ForeignKey(UserProfile, models.PROTECT, db_column='UserID', blank=True, null=True) 
    year = models.IntegerField(db_column='Year', blank=True, null=True)  
    month = models.IntegerField(db_column='Month', blank=True, null=True)
    cost_incurred = models.FloatField(db_column='CostIncurred', blank=True, null=True)
    generated_invoice = models.CharField(db_column='GeneratedInvoice', max_length=255, blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'FinanceReport'


class Feedback(models.Model):
    feedback_id = models.AutoField(db_column='FeedbackID', primary_key=True)  
    user_id = models.ForeignKey(UserProfile, models.PROTECT, db_column='UserID', blank=True, null=True)  
    rating = models.IntegerField(db_column='Rating', blank=True, null=True)  
    notes = models.CharField(db_column='Notes', max_length=255, blank=True, null=True)  

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
    model_id = models.AutoField(db_column='ModelID', primary_key=True)  
    model_name = models.CharField(db_column='ModelName', max_length=255, blank=True, null=True)  
    notes = models.CharField(db_column='Notes', max_length=255, blank=True, null=True)  
    filepath = models.CharField(db_column='FilePath', max_length=255, blank=True, null=True)  
    price_per_prediction = models.FloatField(db_column='PricePerPrediction', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Model'


class OperationLookup(models.Model):
    operation_id = models.AutoField(db_column='OperationID', primary_key=True)  
    operation_name = models.CharField(db_column='OperationName', max_length=255, blank=True, null=True)  

    class Meta:
        managed = True
        db_table = 'OperationLookup'


class TableLookup(models.Model):
    table_id = models.AutoField(db_column='TableID', primary_key=True) 
    table_name = models.CharField(db_column='TableName', max_length=255, blank=True, null=True)  

    class Meta:
        managed = True
        db_table = 'TableLookup'


class TrainingDataset(models.Model):
    training_dataset_id = models.AutoField(db_column='TrainingDatasetID', primary_key=True)  
    claim_id = models.ForeignKey(Claim, models.PROTECT, db_column='ClaimID', blank=True, null=True)  

    class Meta:
        managed = True
        db_table = 'TrainingDataset'


class UploadedRecord(models.Model):
    uploaded_record_id = models.AutoField(db_column='UploadedRecordID', primary_key=True)  
    user_id = models.ForeignKey(UserProfile, models.PROTECT, db_column='UserID', blank=True, null=True)  
    claim_id = models.ForeignKey(Claim, models.PROTECT, db_column='ClaimID', blank=True, null=True)  
    feedback_id = models.ForeignKey(Feedback, models.PROTECT, db_column='FeedbackID', blank=True, null=True)  
    model_id = models.ForeignKey(Model, models.PROTECT, db_column='ModelID', blank=True, null=True)  
    predicted_settlement = models.FloatField(db_column='PredictedSettlement', blank=True, null=True)  
    upload_date = models.DateField(db_column='UploadDate', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'UploadedRecord'

    @staticmethod
    def upload_claims_from_file(file, user: UserProfile) -> SimpleResult:
        result = SimpleResult()
        
        csv = pd.read_csv(file)
        claimValidationResult = Claim.validate_columns(csv)
        if not claimValidationResult.success:
            result.add_messages_from_result_and_mark_unsuccessful_if_error_found(claimValidationResult)
            return result
            
        claims: list[Claim] = Claim.create_claims_from_dataframe(csv)
        for claim in claims:
            claim.save()
            
            uploadedRecord = UploadedRecord()
            uploadedRecord.user_id = None if not user else user.user_profile_id # TODO: remove this when account creation is implemented
            uploadedRecord.claim_id = claim.claim_id
            uploadedRecord.feedback_id = None
            uploadedRecord.model_id = None
            uploadedRecord.predicted_settlement = None
            uploadedRecord.upload_date = date.today()
            
            uploadedRecord.save()
            
        return result