from flask import Flask, jsonify, request
import os
import mysql.connector
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection():
    """Create a connection to the database"""
    return mysql.connector.connect(
        host=os.environ.get('DATABASE_HOST', 'db'),
        user=os.environ.get('DATABASE_USERNAME', 'dbuser'),
        password=os.environ.get('DATABASE_PASSWORD', 'dbpassword'),
        database=os.environ.get('DATABASE_NAME', 'dockerdjango')
    )

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'ml-service'})

@app.route('/api/db-info', methods=['GET'])
def db_info():
    """Get information about the database structure"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get list of tables
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = %s
        """, (os.environ.get('DATABASE_NAME', 'dockerdjango'),))
        
        tables = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'database': os.environ.get('DATABASE_NAME', 'dockerdjango'),
            'tables': [table['TABLE_NAME'] for table in tables]
        })
    except Exception as e:
        logger.error(f"Database info error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/models', methods=['GET'])
def get_models():
    """Get available ML models from the database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # First check if the table exists and what case it might be using
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME LIKE %s
        """, (os.environ.get('DATABASE_NAME', 'dockerdjango'), '%model%'))
        
        tables = cursor.fetchall()
        logger.info(f"Found tables matching 'model': {tables}")
        
        if not tables:
            return jsonify({'status': 'error', 'message': 'Model table not found in database'})
        
        # Use the actual table name with backticks to handle case sensitivity
        table_name = tables[0]['TABLE_NAME']
        logger.info(f"Using table name: {table_name}")
        
        # Query the Model table using backticks for case-sensitive table names
        cursor.execute(f"SELECT * FROM `{table_name}`")
        models = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        if not models:
            return jsonify({'status': 'error', 'message': 'no models provided'})
        
        return jsonify({
            'status': 'success',
            'models': models
        })
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    """Make a prediction using the specified model"""
    data = request.get_json()
    
    if not data:
        return jsonify({'status': 'error', 'message': 'No data provided'}), 400
    
    model_id = data.get('model_id')
    
    if not model_id:
        return jsonify({'status': 'error', 'message': 'No model_id provided'}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # First check if the table exists and what case it might be using
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME LIKE %s
        """, (os.environ.get('DATABASE_NAME', 'dockerdjango'), '%model%'))
        
        tables = cursor.fetchall()
        
        if not tables:
            return jsonify({'status': 'error', 'message': 'Model table not found in database'}), 500
        
        # Use the actual table name with backticks to handle case sensitivity
        table_name = tables[0]['TABLE_NAME']
        
        # Check if model exists
        cursor.execute(f"SELECT * FROM `{table_name}` WHERE modelid = %s", (model_id,))
        model = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not model:
            return jsonify({'status': 'error', 'message': f'Model with ID {model_id} not found'}), 404
        
        # For now, just return a placeholder prediction
        # In a real implementation, you would load the model and make a prediction
        return jsonify({
            'status': 'success',
            'prediction': {
                'model_name': model['modelname'] if 'modelname' in model else model.get('ModelName', 'Unknown'),
                'settlement_value': 0.0,  # Placeholder
                'confidence': 0.0         # Placeholder
            }
        })
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)