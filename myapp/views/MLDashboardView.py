from django import forms
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings

import logging
import requests

from myapp.models import PreprocessingStep, UploadedRecord

# Configure logging
logger = logging.getLogger(__name__)


class UploadModelForm(forms.Form):
    model_name = forms.CharField(
        label="Model Name",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'modelName',
            'class': 'form-control'
        })
    )
    
    notes = forms.CharField(
        label="Notes",
        max_length=255,
        required=False,
        widget=forms.Textarea(attrs={
            'id': 'modelNotes',
            'rows': 3,
            'class': 'form-control',
        })
    )

    data_processing_options = forms.MultipleChoiceField(
        label="Select preprocessing steps",
        required=False,
        widget=forms.SelectMultiple(attrs={
            'id': 'preprocessingSteps',
            'class': 'form-select',
            'multiple': 'multiple',
        })
    )

    model_file = forms.FileField(
        label="Model File (.pkl)",
        required=True,
        widget=forms.ClearableFileInput(attrs={
            'id': 'modelFile',
            'accept': '.pkl',
            'class': 'form-control',
        })
    )

    price_per_prediction = forms.IntegerField(
        label="Price Per Prediction",
        required=True,
        widget=forms.NumberInput(attrs={
            'id': 'pricePerPrediction',
            'class': 'form-control',
        })
    )

    def __init__(self, *args, **kwargs):
        preprocessing_steps = kwargs.pop('preprocessing_steps', [])
        super().__init__(*args, **kwargs)
        self.fields['data_processing_options'].choices = [
            (step.preprocessing_step_id, step.preprocess_name) for step in preprocessing_steps
        ]


@method_decorator([login_required, permission_required("myapp.add_predictionmodel")], name="dispatch")
class MLDashboardView(View):
    """
    This class handles rendering the machine learning dashboard page.
    """

    template_name = "engineer.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handles the GET request for the machine learning dashboard page.
        Renders the ML dashboard template.
        """
        logger.info(f"{request.user} accessed the machine learning dashboard page.")
        try:
            # sends authenticated request to ML service, it just
            ml_service_url = getattr(settings, 'ML_SERVICE_URL', 'http://ml-service:8001')
            response = requests.get(f"{ml_service_url}/api/models/")
            response_data = response.json()

            for x in response_data['models']:
                if isinstance(x['preprocessingSteps'], list):
                    x['preprocessingSteps'] = ", ".join(x['preprocessingSteps'])

            num_predictions = UploadedRecord.objects.all().count()
            preprocessing_steps = PreprocessingStep.objects.all()
            form = UploadModelForm(preprocessing_steps=preprocessing_steps)
        
            preprocessing_data = []
            for i in preprocessing_steps:
                entry = {
                    "id": i.preprocessing_step_id,
                    "name": i.preprocess_name
                }
                preprocessing_data.append(entry)

            context = {
                'form': form,
                'models': response_data.get('models', []),
                'preprocessing_steps': preprocessing_data,
                'num_predictions': num_predictions,
            }

            return render(request, self.template_name, context=context)
        except Exception as e:
            logger.error(f"Error getting models from ML service: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f"Error communicating with ML service: {str(e)}"
            }, status=500)
    
    def post(self, request: HttpRequest) -> JsonResponse:
        """
        Handles the POST request for uploading a new ML model.
        Proxies the request to the ML service.
        """

        if not request.user.is_authenticated:
            return JsonResponse(
                {'status': 'error', 'message': 'Authentication required'},
                status=401
            )

        try:
            ml_service_url = getattr(settings, 'ML_SERVICE_URL', 'http://ml-service:8001')
            # Forward files and data to the ML service
            model_file = request.FILES.get('model_file')
            
            if not model_file:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No model file provided'
                }, status=400)
            
            # Create multipart form data request
            files = {'model_file': (model_file.name, model_file, model_file.content_type)}
            data = dict(request.POST.items())
            
            # Send request to ML service
            response = requests.post(
                f"{ml_service_url}/api/upload-model/",
                files=files,
                data=data
            )
            
            if response.status_code == 200:
                self.request.session['ml_upload_message'] = 'success'
            else:
                self.request.session['ml_upload_message'] = 'failure'

            return redirect("engineer")

        except Exception as e:
            logger.error(f"Error uploading model to ML service: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f"Error communicating with ML service: {str(e)}"
            }, status=500)    
