"""
Inference Script for Stress Detection Model
Handles loading the trained model and making predictions
"""

import os
import pickle
import numpy as np
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class StressPredictor:
    """
    Encapsulates the stress detection model for inference
    """
    
    def __init__(self, model_path: str = None):
        """
        Initialize the predictor with a trained model
        
        Args:
            model_path: Path to the trained model pickle file
        """
        if model_path is None:
            model_path = os.getenv('MODEL_PATH')
            if model_path is None:
                # Create path relative to current file
                current_dir = os.path.dirname(os.path.abspath(__file__))
                model_path = os.path.join(current_dir, '..', 'ml_logic', 'models', 'stress_model.pkl')
                model_path = os.path.abspath(model_path)  # Normalize the path
        
        self.model_path = model_path
        self.model = None
        self.label_encoder = None
        self.feature_names = [
            'heart_rate',
            'ecg',
            'emg',
            'gsr',
            'resp'
        ]
        self.stress_classes = ['low', 'medium', 'high']
        
        self.load_model()
    
    def load_model(self):
        """Load the trained model from disk"""
        try:
            if not os.path.exists(self.model_path):
                logger.warning(f"Model not found at {self.model_path}")
                logger.info("Using mock model for demonstration")
                self.model = self._create_mock_model()
            else:
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                logger.info(f"Model loaded successfully from {self.model_path}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            logger.info("Falling back to mock model")
            self.model = self._create_mock_model()
    
    def _create_mock_model(self):
        """
        Create a mock model for demonstration when actual model is not available
        This is useful for testing the API without the actual trained model
        """
        from sklearn.ensemble import RandomForestClassifier
        
        # Create a simple mock model
        mock_model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        )
        
        # Generate synthetic training data for demonstration
        X_mock = np.random.rand(100, 5) * 100
        y_mock = np.random.choice([0, 1, 2], 100)  # 0=low, 1=medium, 2=high
        
        mock_model.fit(X_mock, y_mock)
        return mock_model
    
    def validate_input(self, data: Dict) -> Tuple[bool, str]:
        """
        Validate input data format and values
        
        Args:
            data: Input dictionary with feature values
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        required_features = self.feature_names
        
        # Check if all required features are present
        missing_features = [f for f in required_features if f not in data]
        if missing_features:
            return False, f"Missing features: {missing_features}"
        
        # Check if values are numeric and within reasonable ranges
        for feature in required_features:
            try:
                value = float(data[feature])
                if value < 0:
                    return False, f"Feature '{feature}' must be non-negative"
            except (ValueError, TypeError):
                return False, f"Feature '{feature}' must be a number"
        
        return True, ""
    
    def predict(self, data: Dict) -> Dict:
        """
        Make a stress prediction based on input features
        
        Args:
            data: Dictionary containing physiological measurements
                  Example: {
                      'heart_rate': 75,
                      'ecg': 0.5,
                      'emg': 0.3,
                      'gsr': 0.2,
                      'resp': 0.4
                  }
        
        Returns:
            Dictionary with prediction results:
            {
                'stress_level': 'low',
                'confidence': 0.95,
                'probabilities': {
                    'low': 0.95,
                    'medium': 0.04,
                    'high': 0.01
                }
            }
        """
        # Validate input
        is_valid, error_msg = self.validate_input(data)
        if not is_valid:
            return {
                'error': error_msg,
                'stress_level': None,
                'confidence': 0.0
            }
        
        try:
            # Extract features in correct order
            features = np.array([[
                float(data[feature]) for feature in self.feature_names
            ]])
            
            # Make prediction
            prediction = self.model.predict(features)[0]
            probabilities = self.model.predict_proba(features)[0]
            
            # Convert to class labels
            stress_level = self.stress_classes[prediction]
            confidence = float(max(probabilities))
            
            # Create probability dictionary
            prob_dict = {
                self.stress_classes[i]: float(prob)
                for i, prob in enumerate(probabilities)
            }
            
            return {
                'stress_level': stress_level,
                'confidence': round(confidence, 4),
                'probabilities': {k: round(v, 4) for k, v in prob_dict.items()},
                'features_used': self.feature_names
            }
        
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return {
                'error': f"Prediction failed: {str(e)}",
                'stress_level': None,
                'confidence': 0.0
            }
    
    def batch_predict(self, data_list: list) -> list:
        """
        Make predictions for multiple inputs
        
        Args:
            data_list: List of input dictionaries
        
        Returns:
            List of prediction results
        """
        return [self.predict(data) for data in data_list]


# Initialize the predictor as a singleton
_predictor = None


def get_predictor() -> StressPredictor:
    """Get or create the predictor instance"""
    global _predictor
    if _predictor is None:
        _predictor = StressPredictor()
    return _predictor
