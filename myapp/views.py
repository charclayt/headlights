from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import os
import logging
import pickle
from .models import Model, Claim, Uploadedrecord, Bod

# Configure logging
logger = logging.getLogger(__name__)

def index(request):
    """Simple index page view"""
    # Get all models to display on the page
    models = Model.objects.all()
    return render(request, 'myapp/index.html', {'models': models})

@require_http_methods(["GET"])
def models_list(request):
    """List all available ML models directly from Django database"""
    try:
        # Get all models from the database
        models = Model.objects.all()
        
        # Convert models to a list of dictionaries
        models_list = [
            {
                'id': model.modelid,
                'name': model.modelname,
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
        
        # Return the list of models
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

@csrf_exempt
@require_http_methods(["POST"])
def upload_model(request):
    """Upload a new ML model"""
    try:
        # Get model name and notes from the request
        model_name = request.POST.get('model_name')
        notes = request.POST.get('notes', '')
        
        # Check if model file was provided
        if 'model_file' not in request.FILES:
            return JsonResponse({
                'status': 'error',
                'message': 'No model file provided'
            }, status=400)
        
        # Get the model file
        model_file = request.FILES['model_file']
        
        # Check if file has a valid extension (e.g., .pkl)
        if not model_file.name.endswith('.pkl'):
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
            modelname=model_name,
            notes=notes,
            filepath=file_path
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Model uploaded successfully',
            'model_id': model.modelid
        })
    except Exception as e:
        logger.error(f"Error uploading model: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': f"An unexpected error occurred: {str(e)}"
        }, status=500)
        
        
@csrf_exempt
@require_http_methods(["POST"])
def predict(request):
    """Make a prediction using a model"""
    try:
        # Parse the request body
        data = json.loads(request.body)
        
        # Extract model_id and claim_data from the request
        model_id = data.get('model_id')
        claim_data = data.get('claim_data', {})
        
        if not model_id:
            return JsonResponse({
                'status': 'error',
                'message': 'No model_id provided'
            }, status=400)
        
        # Find the model in the database
        try:
            model = Model.objects.get(modelid=model_id)
        except Model.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': f'Model with ID {model_id} not found'
            }, status=404)
        
        # PLACEHOLDER: Here you would load the model and make a prediction
        # In a real implementation, you would load the model using pickle or joblib
        # and apply it to the claim_data
        
        # Example placeholder:
        """
        model_path = model.filepath
        with open(model_path, 'rb') as f:
            ml_model = pickle.load(f)
            
        # Prepare the data for prediction
        # This would depend on your specific model requirements
        
        # Make the prediction
        prediction = ml_model.predict(processed_data)
        """
        
        # For now, return a placeholder prediction
        prediction_result = {
            'settlement_value': 15000.00,  # Placeholder value
            'confidence': 0.85             # Placeholder confidence score
        }
        
        return JsonResponse({
            'status': 'success',
            'prediction': prediction_result,
            'model_name': model.modelname
        })
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON in request body'
        }, status=400)
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': f"An unexpected error occurred: {str(e)}"
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def submit_claim(request):
    """Submit a claim and get a settlement prediction"""
    try:
        # Parse the request body
        data = json.loads(request.body)
        
        # Extract the user_id from the request
        user_id = data.get('user_id')
        claim_data = data.get('claim_data', {})
        
        if not user_id:
            return JsonResponse({
                'status': 'error',
                'message': 'User ID is required'
            }, status=400)
            
        # Get the latest model from the database
        try:
            latest_model = Model.objects.latest('modelid')
        except Model.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'No models available'
            }, status=404)
        
        # PLACEHOLDER: Here you would process the claim data and make a prediction
        # Similar to the predict function above
        
        # Create a new Claim record
        # Extract claim fields from claim_data
        # Note: These would need to match your actual database schema
        new_claim = Claim.objects.create(
            accidenttype=claim_data.get('accident_type', ''),
            injuryprognosis=claim_data.get('injury_prognosis', 0),
            specialhealthexpenses=claim_data.get('special_health_expenses', 0.0),
            # Add other fields as needed
        )
        
        # Get the user
        try:
            user = Bod.objects.get(bodid=user_id)
        except Bod.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': f'User with ID {user_id} not found'
            }, status=404)
            
        # PLACEHOLDER: Generate a prediction result
        # In a real implementation, you would use the latest_model to make a prediction
        predicted_settlement = 12500.00  # Placeholder value
        
        # Create an UploadedRecord to track this prediction
        uploaded_record = Uploadedrecord.objects.create(
            bodid=user,
            claimid=new_claim,
            modelid=latest_model,
            predictedsettlement=predicted_settlement
        )
        
        # Return the prediction result along with the record IDs
        return JsonResponse({
            'status': 'success',
            'claim_id': new_claim.claimid,
            'record_id': uploaded_record.uploadedrecordid,
            'prediction': {
                'settlement_value': predicted_settlement,
                'confidence': 0.80  # Placeholder confidence score
            }
        })
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON in request body'
        }, status=400)
    except Exception as e:
        logger.error(f"Claim submission error: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': f"An unexpected error occurred: {str(e)}"
        }, status=500)

def model_check_on_startup():
    """Check if any ML models are available on startup"""
    logger.info("Checking for available ML models on startup...")
    try:
        # Get all models from the database
        models_count = Model.objects.count()
        logger.info(f"Found {models_count} ML models in the system")
    except Exception as e:
        logger.error(f"Unexpected error checking ML models on startup: {str(e)}")

class MLUtils:
    """Utility class for ML operations"""
    
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
    
    @staticmethod
    def preprocess_data(claim_data):
        """Preprocess claim data for prediction"""
        # PLACEHOLDER: In a real implementation, you would transform the claim data
        # into the format expected by your model
        return claim_data
    
    @staticmethod
    def make_prediction(model, processed_data):
        """Make a prediction using the model"""
        # PLACEHOLDER: In a real implementation, you would call the model's predict method
        # with the processed data
        return {
            'settlement_value': 10000.00,  # Placeholder
            'confidence': 0.75            # Placeholder
        }