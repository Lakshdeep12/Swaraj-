"""
Model Training Script for Stress Detection
Trains a Random Forest classifier on stress detection data
"""
import os
import pickle
import numpy as np
import pandas as pd
import logging
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)
from preprocessing import load_data, preprocess_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ModelTrainer:
    """
    Handles training and evaluation of the stress detection model
    """
    
    def __init__(self, model_save_path=None):
        """
        Initialize the model trainer
        
        Args:
            model_save_path: Path where trained model will be saved
        """
        if model_save_path is None:
            # Create path relative to this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            model_save_path = os.path.join(current_dir, 'models', 'stress_model.pkl')
        
        self.model_save_path = model_save_path
        self.model = None
        self.metrics = {}
        
        # Ensure models directory exists
        model_dir = os.path.dirname(self.model_save_path)
        if model_dir:
            os.makedirs(model_dir, exist_ok=True)
    
    def train(self, X, y, test_size=0.2, random_state=42):
        """
        Train the Random Forest model
        
        Args:
            X: Features array
            y: Target labels array
            test_size: Proportion of data for testing
            random_state: Random seed for reproducibility
        
        Returns:
            Dictionary with training results
        """
        logger.info(f"Starting model training with {len(X)} samples")
        logger.info(f"Feature dimensions: {X.shape}")
        logger.info(f"Class distribution: {pd.Series(y).value_counts().to_dict()}")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=test_size,
            random_state=random_state,
            stratify=y
        )
        
        logger.info(f"Training set size: {len(X_train)}")
        logger.info(f"Testing set size: {len(X_test)}")
        
        # Initialize and train model
        logger.info("Initializing Random Forest Classifier...")
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=random_state,
            n_jobs=-1,
            class_weight='balanced'
        )
        
        logger.info("Training model...")
        self.model.fit(X_train, y_train)
        
        # Evaluate
        logger.info("Evaluating model...")
        self._evaluate(X_train, y_train, X_test, y_test)
        
        return {
            'status': 'success',
            'model': self.model,
            'metrics': self.metrics,
            'train_size': len(X_train),
            'test_size': len(X_test)
        }
    
    def _evaluate(self, X_train, y_train, X_test, y_test):
        """
        Evaluate model performance
        
        Args:
            X_train, y_train: Training data
            X_test, y_test: Testing data
        """
        # Predictions
        y_train_pred = self.model.predict(X_train)
        y_test_pred = self.model.predict(X_test)
        
        # Metrics
        self.metrics = {
            'train': {
                'accuracy': accuracy_score(y_train, y_train_pred),
                'precision': precision_score(y_train, y_train_pred, average='weighted', zero_division=0),
                'recall': recall_score(y_train, y_train_pred, average='weighted', zero_division=0),
                'f1': f1_score(y_train, y_train_pred, average='weighted', zero_division=0)
            },
            'test': {
                'accuracy': accuracy_score(y_test, y_test_pred),
                'precision': precision_score(y_test, y_test_pred, average='weighted', zero_division=0),
                'recall': recall_score(y_test, y_test_pred, average='weighted', zero_division=0),
                'f1': f1_score(y_test, y_test_pred, average='weighted', zero_division=0)
            }
        }
        
        # Log metrics
        logger.info("Training Metrics:")
        for metric, value in self.metrics['train'].items():
            logger.info(f"  {metric}: {value:.4f}")
        
        logger.info("Testing Metrics:")
        for metric, value in self.metrics['test'].items():
            logger.info(f"  {metric}: {value:.4f}")
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_test_pred)
        logger.info(f"Confusion Matrix:\n{cm}")
        
        # Classification report
        logger.info("Classification Report:")
        logger.info(classification_report(y_test, y_test_pred, zero_division=0))
        
        # Feature importance
        logger.info("Feature Importance:")
        importances = self.model.feature_importances_
        feature_names = ['heart_rate', 'ecg', 'emg', 'gsr', 'resp']
        for name, importance in zip(feature_names, importances):
            logger.info(f"  {name}: {importance:.4f}")
    
    def save_model(self):
        """Save trained model to disk"""
        if self.model is None:
            logger.error("No model to save. Train a model first.")
            return False
        
        try:
            with open(self.model_save_path, 'wb') as f:
                pickle.dump(self.model, f)
            logger.info(f"Model saved to {self.model_save_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            return False


def main():
    """
    Main training pipeline
    """
    logger.info("=" * 60)
    logger.info("STRESS DETECTION MODEL TRAINING")
    logger.info("=" * 60)
    
    # Load and preprocess data
    logger.info("\nLoading data...")
    try:
        X, y = load_data()
        logger.info("Data loaded successfully")
    except FileNotFoundError:
        logger.warning("Training data not found. Creating synthetic data for demonstration.")
        X = np.random.rand(200, 5) * 100
        y = np.random.choice([0, 1, 2], 200)  # 0=low, 1=medium, 2=high
    
    logger.info("\nPreprocessing data...")
    X = preprocess_data(X)
    
    # Train model
    logger.info("\nTraining model...")
    trainer = ModelTrainer()
    result = trainer.train(X, y)
    
    if result['status'] == 'success':
        # Save model
        logger.info("\nSaving model...")
        trainer.save_model()
        
        logger.info("\n" + "=" * 60)
        logger.info("TRAINING COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)
        logger.info(f"Test Accuracy: {trainer.metrics['test']['accuracy']:.4f}")
        logger.info(f"Test F1 Score: {trainer.metrics['test']['f1']:.4f}")
    else:
        logger.error("Training failed")


if __name__ == '__main__':
    main()
