from django.db import models

class PredictionModel(models.Model):
    model_id = models.AutoField(db_column='ModelID', primary_key=True)  
    model_name = models.CharField(db_column='ModelName', max_length=255, blank=True, null=True)
    model_type = models.CharField(db_column='ModelType', max_length=255, blank=True, null=True)
    notes = models.CharField(db_column='Notes', max_length=255, blank=True, null=True)  
    filepath = models.CharField(db_column='FilePath', max_length=255, blank=True, null=True)  
    price_per_prediction = models.FloatField(db_column='PricePerPrediction', blank=True, null=True)

    class Meta:
        managed = False  # ensures Django doesn't try to create or modify the table
        db_table = 'PredictionModel'

    def __str__(self) -> str:
        """
        This function returns a PredictionModel in a neat string format.
        """
        return f"{self.model_id} | {self.model_name} | {self.model_type} | {self.notes} | {self.filepath} | {self.price_per_prediction}"
    

class PreprocessingStep(models.Model):
    preprocessing_step_id = models.AutoField(db_column='PreprocessingStepID', primary_key=True)
    preprocess_name = models.CharField(db_column='PreprocessName', max_length=255, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'PreprocessingStep'
    
    def __str__(self) -> str:
        """
        This function returns an PreprocessingStep in a neat string format.
        """
        return f"{self.preprocess_name}"


class PreprocessingModelMap(models.Model):
    preprocessing_model_map_id = models.AutoField(db_column='PreprocessingModelMapID', primary_key=True)
    preprocessing_step_id = models.ForeignKey(PreprocessingStep, models.PROTECT, db_column='PreprocessingStepID', blank=True, null=True)
    model_id = models.ForeignKey(PredictionModel, models.PROTECT, db_column='ModelID', blank=True, null=True)
    
    def __str__(self) -> str:
        """
        This function returns an PreprocessingStep in a neat string format.
        """
        return f"{self.preprocessing_step_id} | {self.model_id}"
    
    class Meta:
        managed = False
        db_table = 'PreprocessingModelMap'
