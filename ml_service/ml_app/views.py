from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

import logging
import pickle
import os

from ml_app.models import Model

# Configure logging
logger = logging.getLogger(__name__)


def model_check_on_startup() -> None:
    """
    This method checks if any ML models are available on startup.
    """

    logger.info("Checking for available ML models on startup...")

    try:
        # Get all models from the database
        models_count = Model.objects.count()
        logger.info(f"Found {models_count} ML models in the system")
    except Exception as e:
        logger.error(f"Unexpected error checking ML models on startup: {str(e)}")


@method_decorator(login_required, name="dispatch")
class MLDashboardView(View):
    """
    This class handles the rendering and processing of the machine learning dashboard page.
    """

    template_name = "ml/ml.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handles the GET request for the machine learning dashboard page.

        Args:
            request: the GET request object.

        Returns:
            render: the ml.html template.
        """

        # Get all models to display on the page
        models = Model.objects.all()

        logger.info(f"{request.user} accessed the machine learning dashboard page.")
        return render(request, self.template_name, {'models': models})


@method_decorator(require_http_methods(["GET"]), name="dispatch")
class ModelListView(View):
    """
    This class handles the listing of all available ML models directly from the Django database.
    """

    def get(self, request: HttpRequest) -> JsonResponse:
        """
        Handles the GET request for listing all available ML models.

        Args:
            request: the GET request object.

        Raises:
            Exception: if an error occurs while retrieving the models.

        Returns:
            JsonResponse: a JSON response containing the list of models or no models found.
        """

        try:
            # Get all models from the database
            models = Model.objects.all()

            models_list = [
                {
                    'id': model.model_id,
                    'name': model.model_name,
                    'notes': model.notes,
                    'filepath': model.filepath
                }
                for model in models
            ]
            
            # If no models found, return a specific message
            if not models_list:
                return JsonResponse({
                    'status': 'success',
                    'message': 'no models found'
                })
            
            logger.info(f"Successfully retrieved {len(models_list)} models from the database.")
            return JsonResponse({
                'status': 'success',
                'models': models_list
            })

        except Exception as e:
            logger.error(f"Error getting models: {str(e)}")

            return JsonResponse({
                'status': 'error',
                'message': f"An unexpected error occurred: {str(e)}"
            }, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class UploadModelView(View):
    """
    This class handles the uploading of a new ML model.
    """

    def post(self, request: HttpRequest) -> JsonResponse:
        """
        Handles the POST request for uploading a new ML model.

        Args:
            request: the POST request object.

        Raises:
            Exception: if an error occurs while uploading the model.

        Returns:
            JsonResponse: a JSON response indicating success or failure of the upload.
        """

        try:
            # Get model name and notes from the request
            model_name = request.POST.get('model_name')
            notes = request.POST.get('notes', '')
            
            # Check if model file was provided
            if 'model_file' not in request.FILES:
                logger.info("No model provided in the request.")
                return JsonResponse({
                    'status': 'error',
                    'message': 'No model file provided'
                }, status=400)
            
            # Get the model file
            model_file = request.FILES['model_file']
            
            # Check if file has a valid extension (e.g., .pkl)
            if not model_file.name.endswith('.pkl'):
                logger.info("Invalid file format. Only .pkl files are allowed.")
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid file format. Only .pkl files are allowed.'
                }, status=400)
            
            # Create a directory to store models if it doesn't exist
            upload_dir = os.path.join('media', 'models')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Save the file
            file_path = os.path.join(upload_dir, model_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in model_file.chunks():
                    destination.write(chunk)
            
            # Create a new model record in the database
            model = Model.objects.create(
                model_name=model_name,
                notes=notes,
                filepath=file_path
            )
            
            logger.info("Model uploaded successfully.")
            return JsonResponse({
                'status': 'success',
                'message': 'Model uploaded successfully',
                'model_id': model.model_id
            })
        
        except Exception as e:
            logger.error(f"Error uploading model: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f"An unexpected error occurred: {str(e)}"
            }, status=500)


class MLUtils:
    """
    Utility class for ML operations
    """
    
    @staticmethod
    def load_model(model_path):
        """Load a machine learning model from file"""
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            return model
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return None
        
class HealthCheckView(View):
    """
    Simple health check endpoint to verify the service is running.
    """
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({'status': 'healthy'})