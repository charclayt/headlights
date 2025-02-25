import requests
import logging
import os
import json
from django.conf import settings

logger = logging.getLogger(__name__)

class MLServiceClient:
    """Client for communicating with the ML microservice"""
    
    def __init__(self):
        self.base_url = os.getenv('ML_SERVICE_URL', 'http://ml-service:5000')
    
    def health_check(self):
        """Check if ML service is healthy"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except requests.RequestException as e:
            logger.error(f"ML service health check failed: {e}")
            return False
    
    def check_models(self):
        """Check if any models are available"""
        try:
            response = requests.get(f"{self.base_url}/models/check", timeout=5)
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error checking models: {e}")
            return {'model_available': False, 'message': 'ML service unavailable'}
    
    def get_models(self):
        """Get list of available models"""
        try:
            response = requests.get(f"{self.base_url}/models", timeout=5)
            return response.json().get('models', [])
        except requests.RequestException as e:
            logger.error(f"Error getting models: {e}")
            return []
    
    def upload_model(self, model_file, model_name, notes=''):
        """Upload a new model to the ML service"""
        try:
            files = {'model_file': model_file}
            data = {'model_name': model_name, 'notes': notes}
            
            response = requests.post(
                f"{self.base_url}/models/upload",
                files=files,
                data=data,
                timeout=30  # Longer timeout for file upload
            )
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Model upload error: {e}")
            return {'error': str(e)}