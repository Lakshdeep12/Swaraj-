# Example API requests for testing

## Health Check
```bash
curl http://localhost:5000/health
```

## Get API Features
```bash
curl http://localhost:5000/api/features
```

## Single Prediction (Low Stress)
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "heart_rate": 70,
    "ecg": 0.3,
    "emg": 0.2,
    "gsr": 0.1,
    "resp": 0.3
  }'
```

## Single Prediction (Medium Stress)
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "heart_rate": 85,
    "ecg": 0.6,
    "emg": 0.5,
    "gsr": 0.4,
    "resp": 0.5
  }'
```

## Single Prediction (High Stress)
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "heart_rate": 110,
    "ecg": 0.8,
    "emg": 0.7,
    "gsr": 0.6,
    "resp": 0.7
  }'
```

## Batch Predictions
```bash
curl -X POST http://localhost:5000/api/batch-predict \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {"heart_rate": 70, "ecg": 0.3, "emg": 0.2, "gsr": 0.1, "resp": 0.3},
      {"heart_rate": 85, "ecg": 0.6, "emg": 0.5, "gsr": 0.4, "resp": 0.5},
      {"heart_rate": 110, "ecg": 0.8, "emg": 0.7, "gsr": 0.6, "resp": 0.7}
    ]
  }'
```

## Python Requests

```python
import requests
import json

BASE_URL = "http://localhost:5000"

# Single prediction
data = {
    "heart_rate": 75,
    "ecg": 0.5,
    "emg": 0.3,
    "gsr": 0.2,
    "resp": 0.4
}

response = requests.post(
    f"{BASE_URL}/api/predict",
    json=data
)

print(json.dumps(response.json(), indent=2))

# Batch prediction
batch_data = {
    "data": [
        {"heart_rate": 70, "ecg": 0.3, "emg": 0.2, "gsr": 0.1, "resp": 0.3},
        {"heart_rate": 85, "ecg": 0.6, "emg": 0.5, "gsr": 0.4, "resp": 0.5}
    ]
}

response = requests.post(
    f"{BASE_URL}/api/batch-predict",
    json=batch_data
)

print(json.dumps(response.json(), indent=2))
```

## JavaScript/Fetch

```javascript
const BASE_URL = "http://localhost:5000";

// Single prediction
const data = {
  heart_rate: 75,
  ecg: 0.5,
  emg: 0.3,
  gsr: 0.2,
  resp: 0.4
};

fetch(`${BASE_URL}/api/predict`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(data)
})
.then(response => response.json())
.then(result => console.log(JSON.stringify(result, null, 2)));

// Batch prediction
const batchData = {
  data: [
    {heart_rate: 70, ecg: 0.3, emg: 0.2, gsr: 0.1, resp: 0.3},
    {heart_rate: 85, ecg: 0.6, emg: 0.5, gsr: 0.4, resp: 0.5}
  ]
};

fetch(`${BASE_URL}/api/batch-predict`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(batchData)
})
.then(response => response.json())
.then(result => console.log(JSON.stringify(result, null, 2)));
```

## Expected Response (Low Stress)

```json
{
  "stress_level": "low",
  "confidence": 0.95,
  "probabilities": {
    "low": 0.95,
    "medium": 0.04,
    "high": 0.01
  },
  "features_used": ["heart_rate", "ecg", "emg", "gsr", "resp"]
}
```

## Expected Response (Medium Stress)

```json
{
  "stress_level": "medium",
  "confidence": 0.72,
  "probabilities": {
    "low": 0.15,
    "medium": 0.72,
    "high": 0.13
  },
  "features_used": ["heart_rate", "ecg", "emg", "gsr", "resp"]
}
```

## Expected Response (High Stress)

```json
{
  "stress_level": "high",
  "confidence": 0.88,
  "probabilities": {
    "low": 0.03,
    "medium": 0.09,
    "high": 0.88
  },
  "features_used": ["heart_rate", "ecg", "emg", "gsr", "resp"]
}
```

## Error Response (Missing Fields)

```json
{
  "error": "Missing features: ['gsr', 'resp']",
  "stress_level": null,
  "confidence": 0.0
}
```

## Error Response (Invalid Content Type)

```json
{
  "error": "Content-Type must be application/json",
  "received": "text/plain"
}
```

## Error Response (Batch Size Exceeded)

```json
{
  "error": "Batch size limited to 100 predictions"
}
```

## Load Testing (Apache Bench)

```bash
# Test single endpoint (100 requests, 10 concurrent)
ab -n 100 -c 10 -T application/json \
   -p data.json \
   http://localhost:5000/api/predict

# Where data.json contains:
# {"heart_rate": 75, "ecg": 0.5, "emg": 0.3, "gsr": 0.2, "resp": 0.4}
```

## Load Testing (Apache JMeter)

1. Create Thread Group with 50 threads
2. Add HTTP Sampler:
   - Method: POST
   - URL: http://localhost:5000/api/predict
   - Body: JSON data
3. Add View Results Tree listener
4. Run test

## Performance Benchmarks

Expected results on modern hardware:

```
Single Request Latency:        5-50ms
Throughput (1 worker):         20-100 requests/sec
Throughput (4 workers):        80-400 requests/sec
Model Inference Time:          5-10ms
Batch Prediction (10 items):   15-80ms
Memory Usage:                  ~200MB
CPU Usage (idle):              <1%
CPU Usage (100 req/s):         10-20%
```

---

For more information, see [README.md](README.md) and [DEPLOYMENT.md](DEPLOYMENT.md)
