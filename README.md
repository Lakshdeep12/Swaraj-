# Stress Detection System - Production Ready

A machine learning-based stress detection system that combines a React frontend with a Flask/FastAPI backend to predict user stress levels from physiological data.

## Features

- 🎯 Random Forest ML model for stress prediction
- 🚀 Production-ready Docker deployment
- 📱 React-based user interface
- 🔄 CI/CD pipeline with GitHub Actions
- 📊 RESTful API for predictions
- 🐳 Multi-stage Docker build for optimal image size
- ☁️ Cloud-ready for Render, Railway, or AWS

## Tech Stack

- **Frontend**: React.js, Axios
- **Backend**: Flask, FastAPI
- **ML Model**: Scikit-learn Random Forest Classifier
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Deployment**: Render, Railway, or AWS App Runner

## Project Structure

```
stress-detection-prod/
├── server/                 # Flask backend API
│   ├── app.py             # Flask application entry point
│   ├── predict.py         # Inference script with ML logic
│   ├── models/            # Saved ML models
│   └── requirements.txt    # Python dependencies
├── client/                # React frontend
│   ├── src/
│   ├── public/
│   ├── package.json       # Node dependencies
│   └── Dockerfile         # Frontend build stage
├── ml_logic/              # ML training and utilities
│   ├── train.py          # Model training script
│   └── preprocessing.py  # Data preprocessing utilities
├── Dockerfile            # Multi-stage production Dockerfile
├── docker-compose.yml    # Local development environment
├── requirements.txt      # Root Python dependencies
└── .github/workflows/    # CI/CD pipelines
    └── deploy.yml        # GitHub Actions deployment
```

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 14+
- Docker & Docker Compose

### Local Development

```bash
# Clone repository
git clone https://github.com/yourusername/stress-detection-prod.git
cd stress-detection-prod

# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies
cd client && npm install && cd ..

# Train the model
python ml_logic/train.py

# Start the Flask server
cd server && python app.py
```

### Docker Deployment

```bash
# Build the Docker image
docker build -t stress-detection:latest .

# Run the container
docker run -p 5000:5000 stress-detection:latest
```

Visit `http://localhost:5000` to access the application.

## API Documentation

### Stress Prediction Endpoint

**POST** `/api/predict`

Request body:
```json
{
  "heart_rate": 75,
  "ecg": 0.5,
  "emg": 0.3,
  "gsr": 0.2,
  "resp": 0.4
}
```

Response:
```json
{
  "stress_level": "low",
  "confidence": 0.95,
  "probabilities": {
    "low": 0.95,
    "medium": 0.04,
    "high": 0.01
  }
}
```

## Deployment

### Deploy to Render

1. Push code to GitHub
2. Connect repository to Render
3. Set build command: `docker build -t stress-detection .`
4. Set start command: Docker image
5. Deploy

### Deploy to Railway

1. Connect GitHub repository
2. Railway auto-detects Dockerfile
3. Set PORT environment variable to 5000
4. Deploy

### Deploy to AWS App Runner

1. Connect GitHub repository
2. Configure build settings for Dockerfile
3. Set environment variables
4. Deploy

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## Environment Variables

```
FLASK_ENV=production
FLASK_DEBUG=False
MODEL_PATH=./ml_logic/models/stress_model.pkl
PORT=5000
```

## Model Information

- **Algorithm**: Random Forest Classifier
- **Input Features**: Heart Rate, ECG, EMG, GSR, Respiration
- **Output Classes**: Low, Medium, High (stress levels)
- **Dataset**: WESAD (Wearable Stress and Affect Detection)
- **Accuracy**: ~85% (varies by data)

## CI/CD Pipeline

The GitHub Actions workflow automatically:

1. Builds the Docker image on every push to main
2. Runs linting and code quality checks
3. Executes unit tests
4. Pushes image to Docker registry (optional)
5. Deploys to cloud provider (optional)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Support

For issues and feature requests, please use the GitHub issue tracker.

---

**Last Updated**: January 2026
**Maintainer**: Your Name
