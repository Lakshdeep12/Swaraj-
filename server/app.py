"""
Flask Application for Stress Detection API
Provides REST endpoints for stress prediction and health checks
"""

import os
import sys
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from predict import get_predictor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configuration
app.config['JSON_SORT_KEYS'] = False
PORT = int(os.getenv('PORT', 5000))
FLASK_ENV = os.getenv('FLASK_ENV', 'development')


@app.before_request
def before_request():
    """Initialize predictor on first request"""
    if not hasattr(app, 'predictor'):
        logger.info("Initializing predictor...")
        app.predictor = get_predictor()
        logger.info("Predictor initialized successfully")


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring and load balancers
    
    Returns:
        JSON with health status
    """
    return jsonify({
        'status': 'healthy',
        'service': 'stress-detection-api',
        'version': '1.0.0',
        'environment': FLASK_ENV
    }), 200


@app.route('/api/health', methods=['GET'])
def api_health():
    """
    API health endpoint with more detailed information
    
    Returns:
        JSON with detailed health status
    """
    return jsonify({
        'status': 'ok',
        'message': 'Stress Detection API is running',
        'model_status': 'loaded',
        'api_version': 'v1'
    }), 200


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Main prediction endpoint
    
    Expected JSON format:
    {
        "heart_rate": 75,
        "ecg": 0.5,
        "emg": 0.3,
        "gsr": 0.2,
        "resp": 0.4
    }
    
    Returns:
        JSON with stress prediction result
    """
    try:
        # Validate request has JSON data
        if not request.is_json:
            return jsonify({
                'error': 'Content-Type must be application/json',
                'received': request.content_type
            }), 400
        
        data = request.get_json()
        
        # Log prediction request
        logger.info(f"Prediction request received: {list(data.keys())}")
        
        # Make prediction using the predictor
        result = app.predictor.predict(data)
        
        # Check if prediction had an error
        if 'error' in result and result['error']:
            return jsonify(result), 400
        
        logger.info(f"Prediction completed: {result['stress_level']}")
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error in prediction endpoint: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Internal server error',
            'message': str(e) if FLASK_ENV == 'development' else 'An error occurred'
        }), 500


@app.route('/api/batch-predict', methods=['POST'])
def batch_predict():
    """
    Batch prediction endpoint for multiple inputs
    
    Expected JSON format:
    {
        "data": [
            {"heart_rate": 75, "ecg": 0.5, "emg": 0.3, "gsr": 0.2, "resp": 0.4},
            {"heart_rate": 85, "ecg": 0.6, "emg": 0.4, "gsr": 0.3, "resp": 0.5}
        ]
    }
    
    Returns:
        JSON with list of prediction results
    """
    try:
        if not request.is_json:
            return jsonify({
                'error': 'Content-Type must be application/json'
            }), 400
        
        data = request.get_json()
        
        if 'data' not in data or not isinstance(data['data'], list):
            return jsonify({
                'error': 'Request must contain "data" key with a list of predictions'
            }), 400
        
        if len(data['data']) == 0:
            return jsonify({
                'error': 'Data list cannot be empty'
            }), 400
        
        if len(data['data']) > 100:
            return jsonify({
                'error': 'Batch size limited to 100 predictions'
            }), 400
        
        # Make batch predictions
        results = app.predictor.batch_predict(data['data'])
        
        return jsonify({
            'count': len(results),
            'predictions': results
        }), 200
    
    except Exception as e:
        logger.error(f"Error in batch prediction endpoint: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Internal server error',
            'message': str(e) if FLASK_ENV == 'development' else 'An error occurred'
        }), 500


@app.route('/api/features', methods=['GET'])
def get_features():
    """
    Get information about required model features
    
    Returns:
        JSON with feature information
    """
    return jsonify({
        'features': app.predictor.feature_names,
        'stress_classes': app.predictor.stress_classes,
        'description': {
            'heart_rate': 'Heart rate in beats per minute (0-200)',
            'ecg': 'ECG signal normalized (0-1)',
            'emg': 'EMG signal normalized (0-1)',
            'gsr': 'Galvanic Skin Response normalized (0-1)',
            'resp': 'Respiration signal normalized (0-1)'
        }
    }), 200


@app.route('/', methods=['GET'])
def index():
    """Root endpoint with API information"""
    return jsonify({
        'application': 'Stress Detection API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'health': '/health',
            'api_health': '/api/health',
            'predict': '/api/predict (POST)',
            'batch_predict': '/api/batch-predict (POST)',
            'features': '/api/features (GET)'
        },
        'documentation': '/docs'
    }), 200


@app.route('/docs', methods=['GET'])
def docs():
    """API documentation endpoint"""
    return jsonify({
        'title': 'Stress Detection API Documentation',
        'version': '1.0.0',
        'description': 'API for predicting stress levels using physiological data',
        'endpoints': {
            '/health': {
                'method': 'GET',
                'description': 'Health check endpoint',
                'response': {
                    'status': 'healthy',
                    'service': 'stress-detection-api'
                }
            },
            '/api/predict': {
                'method': 'POST',
                'description': 'Predict stress level for single input',
                'request': {
                    'heart_rate': 'number',
                    'ecg': 'number',
                    'emg': 'number',
                    'gsr': 'number',
                    'resp': 'number'
                },
                'response': {
                    'stress_level': 'low|medium|high',
                    'confidence': 'number (0-1)',
                    'probabilities': {
                        'low': 'number',
                        'medium': 'number',
                        'high': 'number'
                    }
                }
            },
            '/api/batch-predict': {
                'method': 'POST',
                'description': 'Predict stress levels for multiple inputs',
                'request': {
                    'data': 'array of prediction objects'
                }
            },
            '/api/features': {
                'method': 'GET',
                'description': 'Get information about model features'
            }
        }
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'Please check the API documentation at /docs',
        'path': request.path
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        'error': 'Method not allowed',
        'path': request.path,
        'method': request.method
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}", exc_info=True)
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500


if __name__ == '__main__':
    # In production, use gunicorn instead of Flask's built-in server
    # gunicorn -w 4 -b 0.0.0.0:5000 app:app
    
    debug_mode = FLASK_ENV == 'development'
    logger.info(f"Starting Stress Detection API (DEBUG={debug_mode})")
    logger.info(f"Listening on 0.0.0.0:{PORT}")
    
    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=debug_mode,
        use_reloader=debug_mode
    )
