"""
Data Preprocessing Module for Stress Detection
Handles data loading and preprocessing
"""

import numpy as np
import pandas as pd
import logging
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


def load_data(data_path=None):
    """
    Load stress detection data from CSV
    
    Args:
        data_path: Path to the data CSV file
    
    Returns:
        Tuple of (X, y) - features and labels
    """
    if data_path is None:
        # Create path relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(current_dir, 'data', 'stress_data.csv')
    
    try:
        df = pd.read_csv(data_path)
        logger.info(f"Data loaded from {data_path}")
        
        # Assuming last column is the target
        X = df.iloc[:, :-1].values
        y = df.iloc[:, -1].values
        
        logger.info(f"Data shape: {X.shape}")
        logger.info(f"Labels shape: {y.shape}")
        
        return X, y
    except FileNotFoundError:
        raise FileNotFoundError(f"Data file not found at {data_path}")
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise


def preprocess_data(X, scaler=None, fit=True):
    """
    Preprocess features using StandardScaler
    
    Args:
        X: Feature array
        scaler: Optional pre-fitted scaler
        fit: Whether to fit the scaler on the data
    
    Returns:
        Scaled feature array and scaler object
    """
    if scaler is None:
        scaler = StandardScaler()
    
    if fit:
        X_scaled = scaler.fit_transform(X)
    else:
        X_scaled = scaler.transform(X)
    
    logger.info(f"Data preprocessing completed. Shape: {X_scaled.shape}")
    logger.info(f"Feature means: {X_scaled.mean(axis=0)}")
    logger.info(f"Feature stds: {X_scaled.std(axis=0)}")
    
    return X_scaled


def handle_missing_values(X, strategy='mean'):
    """
    Handle missing values in data
    
    Args:
        X: Feature array
        strategy: Strategy for handling missing values ('mean', 'median', 'drop')
    
    Returns:
        Array with missing values handled
    """
    df = pd.DataFrame(X)
    
    if strategy == 'mean':
        df = df.fillna(df.mean())
    elif strategy == 'median':
        df = df.fillna(df.median())
    elif strategy == 'drop':
        df = df.dropna()
    
    return df.values


def remove_outliers(X, threshold=3):
    """
    Remove outliers using z-score method
    
    Args:
        X: Feature array
        threshold: Z-score threshold
    
    Returns:
        Array with outliers removed
    """
    z_scores = np.abs((X - X.mean()) / X.std())
    mask = (z_scores < threshold).all(axis=1)
    return X[mask]


def augment_features(X):
    """
    Create additional features from existing ones
    
    Args:
        X: Feature array
    
    Returns:
        Array with augmented features
    """
    # Calculate ratios and interactions
    hr = X[:, 0]
    ecg = X[:, 1]
    emg = X[:, 2]
    gsr = X[:, 3]
    resp = X[:, 4]
    
    # Additional features
    hr_ecg_ratio = hr / (ecg + 1e-6)
    emg_gsr_product = emg * gsr
    resp_hr_ratio = resp / (hr + 1e-6)
    
    # Combine with original features
    augmented = np.column_stack([
        X,
        hr_ecg_ratio,
        emg_gsr_product,
        resp_hr_ratio
    ])
    
    logger.info(f"Features augmented. New shape: {augmented.shape}")
    return augmented
