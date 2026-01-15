"""
Production-ready base React component for Stress Detection UI
"""

import React, { useState } from 'react';
import axios from 'axios';

const StressPredictionForm = () => {
  const [formData, setFormData] = useState({
    heart_rate: 75,
    ecg: 0.5,
    emg: 0.3,
    gsr: 0.2,
    resp: 0.4
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: parseFloat(value) || value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(`${API_URL}/api/predict`, formData);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to get prediction');
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const getStressColor = (level) => {
    switch (level) {
      case 'low':
        return '#4CAF50'; // Green
      case 'medium':
        return '#FFC107'; // Yellow
      case 'high':
        return '#F44336'; // Red
      default:
        return '#9E9E9E'; // Gray
    }
  };

  return (
    <div style={styles.container}>
      <h1>Stress Detection System</h1>
      
      <form onSubmit={handleSubmit} style={styles.form}>
        <div style={styles.inputGroup}>
          <label>Heart Rate (BPM):</label>
          <input
            type="number"
            name="heart_rate"
            value={formData.heart_rate}
            onChange={handleInputChange}
            min="0"
            max="200"
            step="1"
          />
        </div>

        <div style={styles.inputGroup}>
          <label>ECG (0-1):</label>
          <input
            type="number"
            name="ecg"
            value={formData.ecg}
            onChange={handleInputChange}
            min="0"
            max="1"
            step="0.01"
          />
        </div>

        <div style={styles.inputGroup}>
          <label>EMG (0-1):</label>
          <input
            type="number"
            name="emg"
            value={formData.emg}
            onChange={handleInputChange}
            min="0"
            max="1"
            step="0.01"
          />
        </div>

        <div style={styles.inputGroup}>
          <label>GSR (0-1):</label>
          <input
            type="number"
            name="gsr"
            value={formData.gsr}
            onChange={handleInputChange}
            min="0"
            max="1"
            step="0.01"
          />
        </div>

        <div style={styles.inputGroup}>
          <label>Respiration (0-1):</label>
          <input
            type="number"
            name="resp"
            value={formData.resp}
            onChange={handleInputChange}
            min="0"
            max="1"
            step="0.01"
          />
        </div>

        <button type="submit" disabled={loading} style={styles.button}>
          {loading ? 'Predicting...' : 'Predict Stress Level'}
        </button>
      </form>

      {error && (
        <div style={styles.error}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div style={styles.result}>
          <h2>Prediction Result</h2>
          
          <div style={{
            ...styles.stressLevel,
            backgroundColor: getStressColor(result.stress_level)
          }}>
            <p>Stress Level: <strong>{result.stress_level.toUpperCase()}</strong></p>
            <p>Confidence: {(result.confidence * 100).toFixed(1)}%</p>
          </div>

          <div style={styles.probabilities}>
            <h3>Probabilities:</h3>
            {Object.entries(result.probabilities).map(([level, prob]) => (
              <div key={level} style={styles.probabilityBar}>
                <span>{level}: {(prob * 100).toFixed(1)}%</span>
                <div style={styles.progressBar}>
                  <div style={{
                    ...styles.progressFill,
                    width: `${prob * 100}%`,
                    backgroundColor: getStressColor(level)
                  }} />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

const styles = {
  container: {
    maxWidth: '600px',
    margin: '0 auto',
    padding: '20px',
    fontFamily: 'Arial, sans-serif'
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '15px',
    marginBottom: '20px'
  },
  inputGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: '5px'
  },
  button: {
    padding: '10px 20px',
    backgroundColor: '#007BFF',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '16px'
  },
  error: {
    padding: '15px',
    backgroundColor: '#ffebee',
    color: '#c62828',
    borderRadius: '4px',
    marginBottom: '20px'
  },
  result: {
    padding: '20px',
    backgroundColor: '#f5f5f5',
    borderRadius: '4px'
  },
  stressLevel: {
    padding: '20px',
    color: 'white',
    borderRadius: '4px',
    marginBottom: '20px',
    textAlign: 'center'
  },
  probabilities: {
    marginTop: '20px'
  },
  probabilityBar: {
    marginBottom: '15px'
  },
  progressBar: {
    width: '100%',
    height: '20px',
    backgroundColor: '#e0e0e0',
    borderRadius: '4px',
    overflow: 'hidden',
    marginTop: '5px'
  },
  progressFill: {
    height: '100%',
    transition: 'width 0.3s ease'
  }
};

export default StressPredictionForm;
