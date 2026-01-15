"""
Test suite for Stress Detection API
"""

import unittest
import json
from server.app import app


class APITestCase(unittest.TestCase):
    """Test cases for the Stress Detection API"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_api_health(self):
        """Test API health endpoint"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'ok')
    
    def test_features_endpoint(self):
        """Test features information endpoint"""
        response = self.client.get('/api/features')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('features', data)
        self.assertIn('stress_classes', data)
    
    def test_valid_prediction(self):
        """Test prediction with valid input"""
        payload = {
            'heart_rate': 75,
            'ecg': 0.5,
            'emg': 0.3,
            'gsr': 0.2,
            'resp': 0.4
        }
        response = self.client.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('stress_level', data)
        self.assertIn('confidence', data)
        self.assertIn('probabilities', data)
    
    def test_missing_features(self):
        """Test prediction with missing features"""
        payload = {
            'heart_rate': 75,
            'ecg': 0.5
        }
        response = self.client.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_invalid_content_type(self):
        """Test prediction with wrong content type"""
        response = self.client.post(
            '/api/predict',
            data='not json',
            content_type='text/plain'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_batch_prediction(self):
        """Test batch prediction endpoint"""
        payload = {
            'data': [
                {'heart_rate': 75, 'ecg': 0.5, 'emg': 0.3, 'gsr': 0.2, 'resp': 0.4},
                {'heart_rate': 85, 'ecg': 0.6, 'emg': 0.4, 'gsr': 0.3, 'resp': 0.5}
            ]
        }
        response = self.client.post(
            '/api/batch-predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['count'], 2)
        self.assertIn('predictions', data)
    
    def test_batch_empty_list(self):
        """Test batch prediction with empty list"""
        payload = {'data': []}
        response = self.client.post(
            '/api/batch-predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_batch_size_limit(self):
        """Test batch prediction size limit"""
        payload = {
            'data': [
                {'heart_rate': 75, 'ecg': 0.5, 'emg': 0.3, 'gsr': 0.2, 'resp': 0.4}
            ] * 101  # Exceeds limit of 100
        }
        response = self.client.post(
            '/api/batch-predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_404_not_found(self):
        """Test 404 error for non-existent endpoint"""
        response = self.client.get('/api/nonexistent')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
