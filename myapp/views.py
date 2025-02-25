from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import requests
import os
import logging
from .models import Model, Claim, Uploadedrecord, Bod

def model_check_on_startup():
    """Check if any ML models are available on startup"""
    logger.info("Checking for available ML models on startup...")
    try:
        ML_SERVICE_URL = os.environ.get('ML_SERVICE_URL', 'http://ml-service:5000')
        response = requests.get(f"{ML_SERVICE_URL}/api/models", timeout=5)
        response_data = response.json()
        
        if response_data.get('status') == 'error' and 'no models provided' in response_data.get('message', ''):
            logger.warning("No ML models available in the system")
        else:
            num_models = len(response_data.get('models', []))
            logger.info(f"Found {num_models} ML models in the system")
    except requests.RequestException as e:
        logger.error(f"Error connecting to ML service on startup: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error checking ML models on startup: {str(e)}")

# Configure logging
logger = logging.getLogger(__name__)

# Get ML service URL from environment or use default
ML_SERVICE_URL = os.environ.get('ML_SERVICE_URL', 'http://ml-service:5000')

def index(request):
    """Simple index page view"""
    return render(request, 'myapp/index.html')

@require_http_methods(["GET"])
def models_list(request):
    """List all available ML models"""
    try:
        # Call the ML service to get the models
        response = requests.get(f"{ML_SERVICE_URL}/api/models")
        response_data = response.json()
        
        return JsonResponse(response_data)
    except requests.RequestException as e:
        logger.error(f"Error connecting to ML service: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': f"Failed to connect to ML service: {str(e)}"
        }, status=500)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': f"An unexpected error occurred: {str(e)}"
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def predict(request):
    """Make a prediction using an ML model"""
    try:
        # Parse the request body
        data = json.loads(request.body)
        
        # Call the ML service to make a prediction
        response = requests.post(
            f"{ML_SERVICE_URL}/api/predict",
            json=data
        )
        
        # Return the ML service response
        return JsonResponse(response.json(), status=response.status_code)
    except requests.RequestException as e:
        logger.error(f"Error connecting to ML service: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': f"Failed to connect to ML service: {str(e)}"
        }, status=500)
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': "Invalid JSON in request body"
        }, status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
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
        if not user_id:
            return JsonResponse({
                'status': 'error',
                'message': "User ID is required"
            }, status=400)
            
        # Get the latest model from the database
        try:
            latest_model = Model.objects.latest('modelid')
        except Model.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': "no models provided"
            }, status=404)
            
        # Call the ML service to make a prediction
        response = requests.post(
            f"{ML_SERVICE_URL}/api/predict",
            json={
                'model_id': latest_model.modelid,
                'claim_data': data.get('claim_data', {})
            }
        )
        
        if response.status_code != 200:
            return JsonResponse(response.json(), status=response.status_code)
            
        prediction_data = response.json()
        
        # Create a new Claim record
        # Note: In a real implementation, you would extract all the claim fields
        # from data['claim_data'] and populate the Claim object properly
        new_claim = Claim.objects.create(
            # Populate with actual claim data
            accidenttype=data.get('claim_data', {}).get('accident_type', ''),
            injuryprognosis=data.get('claim_data', {}).get('injury_prognosis', 0)
            # Add other fields as needed
        )
        
        # Get the user
        try:
            user = Bod.objects.get(bodid=user_id)
        except Bod.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': f"User with ID {user_id} not found"
            }, status=404)
            
        # Create an UploadedRecord to track this prediction
        uploaded_record = Uploadedrecord.objects.create(
            bodid=user,
            claimid=new_claim,
            modelid=latest_model,
            predictedsettlement=prediction_data.get('prediction', {}).get('settlement_value', 0.0)
        )
        
        # Return the prediction result along with the record IDs
        return JsonResponse({
            'status': 'success',
            'claim_id': new_claim.claimid,
            'record_id': uploaded_record.uploadedrecordid,
            'prediction': prediction_data.get('prediction', {})
        })
    except requests.RequestException as e:
        logger.error(f"Error connecting to ML service: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': f"Failed to connect to ML service: {str(e)}"
        }, status=500)
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': "Invalid JSON in request body"
        }, status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': f"An unexpected error occurred: {str(e)}"
        }, status=500)