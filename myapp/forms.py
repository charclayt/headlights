from django import forms
from django.core.validators import FileExtensionValidator

class RecordUploadForm(forms.Form):
    file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['csv'])],
                           widget=forms.FileInput(attrs={'accept':'.csv'}))