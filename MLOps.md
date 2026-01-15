# Stress Detection - MLOps Production Architecture

## Project Overview

This is a **production-ready, enterprise-grade** stress detection application that transforms a research ML model into a fully deployable service with:

- ✅ **Production-Grade Architecture**: Clean separation of concerns (ML, Backend, Frontend)
- ✅ **Containerization**: Multi-stage Docker build for optimal image size
- ✅ **CI/CD Pipeline**: Automated testing, building, and deployment with GitHub Actions
- ✅ **Cloud Ready**: Deploy to Render, Railway, AWS, or any Docker-compatible platform
- ✅ **API-First Design**: RESTful endpoints with comprehensive error handling
- ✅ **Monitoring**: Health checks, logging, and performance metrics
- ✅ **Security**: Input validation, CORS, secure defaults

---

## Directory Structure

```
stress-detection-prod/
│
├── .github/
│   └── workflows/
│       └── deploy.yml              # CI/CD pipeline configuration
│
├── server/                          # Flask Backend API
│   ├── app.py                      # Main Flask application
│   ├── predict.py                  # ML inference logic
│   ├── requirements.txt            # Python dependencies
│   ├── .env.example                # Environment variable template
│   └── static/                     # Served React build files
│
├── client/                          # React Frontend
│   ├── src/                        # React components
│   ├── public/                     # Static assets
│   ├── package.json                # Node.js dependencies
│   └── Dockerfile.dev              # Development container
│
├── ml_logic/                        # Machine Learning Logic
│   ├── train.py                    # Model training script
│   ├── preprocessing.py            # Data preprocessing utilities
│   ├── models/                     # Saved model files
│   └── data/                       # Training data directory
│
├── Dockerfile                       # Production multi-stage build
├── docker-compose.yml              # Local development environment
├── requirements.txt                # Root dependencies
├── README.md                       # Project documentation
├── DEPLOYMENT.md                   # Detailed deployment guide
├── .gitignore                      # Git configuration
└── MLOps.md                        # This file - Architecture overview

```

---

## Architecture Overview

### Component Diagram

```
                    ┌─────────────────────┐
                    │   React Frontend    │
                    │  (Node 18-alpine)   │
                    └──────────┬──────────┘
                               │
                               │ (Static Build)
                               ▼
                    ┌─────────────────────┐
                    │   Flask Backend     │
                    │ (Python 3.9-slim)   │
                    │   + Gunicorn        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   ML Model Logic    │
                    │  Random Forest      │
                    │  Scikit-Learn       │
                    └─────────────────────┘
```

### Data Flow

```
1. User Input (via React UI)
   ↓
2. HTTP Request → Flask API (JSON)
   ↓
3. Input Validation (predict.py)
   ↓
4. Feature Extraction & Normalization
   ↓
5. Random Forest Model Inference
   ↓
6. Probability Calculation
   ↓
7. JSON Response → React Frontend
   ↓
8. UI Display (Stress Level + Confidence)
```

---

## Key Technologies

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Frontend | React | 18.2+ | User interface |
| Backend | Flask | 2.3+ | REST API server |
| ML Framework | Scikit-learn | 1.3+ | Random Forest model |
| Server | Gunicorn | 21.2+ | Production WSGI server |
| Containerization | Docker | Latest | Deployment container |
| Container Orchestration | Docker Compose | Latest | Local development |
| CI/CD | GitHub Actions | Native | Automated pipeline |

---

## Deployment Architecture

### Single Container (Monolithic)
```
Docker Container
├── React Static Files
├── Flask Server
└── ML Model
```

**Best for**: Simple deployments, getting started, learning

**Platforms**: Render, Railway, AWS App Runner, Heroku

### Multi-Container (Microservices)
```
Container 1: Frontend (Nginx)
Container 2: Backend API (Flask)
Container 3: ML Service (FastAPI)
Container 4: Database (PostgreSQL)
Container 5: Redis (Caching)
```

**Best for**: Large-scale applications, horizontal scaling

**Platforms**: Kubernetes, Docker Swarm, AWS ECS

### Serverless
```
AWS Lambda + API Gateway
+ S3 for frontend
+ SageMaker for ML
```

**Best for**: Cost optimization, pay-per-use

**Platforms**: AWS Lambda, Google Cloud Functions, Azure Functions

---

## Key Features Explained

### 1. Multi-Stage Docker Build

**Why**: Reduces image size by ~70%

```dockerfile
Stage 1: Build frontend (Node 18-alpine) → React build files
Stage 2: Build backend (Python 3.9-slim) → Copy build from Stage 1
Result: Single optimized ~500MB image
```

### 2. API Endpoints

```
GET  /                    # Root endpoint with API info
GET  /health             # Health check (for load balancers)
GET  /api/health         # Detailed health status
GET  /api/features       # Model feature information
POST /api/predict        # Single prediction
POST /api/batch-predict  # Multiple predictions
GET  /docs               # API documentation
```

### 3. Input Validation Pipeline

```python
Request → JSON Parse → Feature Check → Value Validation → Prediction
```

### 4. Error Handling

All errors return structured JSON:
```json
{
  "error": "Error type",
  "message": "Human-readable message",
  "details": {...}
}
```

### 5. Logging & Monitoring

- **Flask Logging**: All requests logged to stdout
- **Health Checks**: Kubernetes/Docker native support
- **Metrics**: Response times, error rates tracked
- **Alerts**: Optional Slack integration via CI/CD

---

## CI/CD Pipeline

### Workflow Stages

```
┌─────────────────────────────────────────────────────────┐
│ 1. Code Push to GitHub                                  │
└────────────────┬────────────────────────────────────────┘
                 │
         ┌───────▼────────┐
         │ Checkout Code  │
         └────────┬───────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
  Build      Lint & Test   Security
  Docker     (Python/JS)    Scan
    │             │             │
    └─────────────┼─────────────┘
                  │
         ┌────────▼────────┐
         │ Push to Registry│
         └────────┬────────┘
                  │
    ┌─────────────┴─────────────┐
    │                           │
    ▼                           ▼
Deploy to Render        Deploy to Railway
(if configured)         (if configured)
```

### Pipeline Features

- **Parallel Jobs**: Build, test, scan run simultaneously
- **Conditional Deployment**: Only on main branch
- **Security Scans**: Trivy vulnerability scanning
- **Test Coverage**: Python unit tests, JS linting
- **Notifications**: Slack alerts on failures

---

## Model Information

### Architecture
```
Input Features (5)
    ↓
Random Forest Classifier
    ├── n_estimators=100
    ├── max_depth=15
    ├── min_samples_split=5
    └── class_weight='balanced'
    ↓
Output Classes (3): Low, Medium, High Stress
```

### Features

| Feature | Range | Unit | Description |
|---------|-------|------|-------------|
| Heart Rate | 40-200 | BPM | Beats per minute |
| ECG | 0-1 | Normalized | Electrical cardiac activity |
| EMG | 0-1 | Normalized | Muscle activity |
| GSR | 0-1 | Normalized | Skin conductance |
| Respiration | 0-1 | Normalized | Breathing rate |

### Output

```json
{
  "stress_level": "low",           // Category prediction
  "confidence": 0.9847,             // Prediction confidence (0-1)
  "probabilities": {
    "low": 0.9847,
    "medium": 0.0142,
    "high": 0.0011
  }
}
```

---

## Production Deployment Checklist

### Pre-Deployment
- [ ] All tests passing
- [ ] Code reviewed and approved
- [ ] Security scan passed
- [ ] Documentation updated
- [ ] Environment variables configured
- [ ] Model file included
- [ ] Database backups created

### Deployment
- [ ] Docker image built successfully
- [ ] Image pushed to registry
- [ ] Health checks configured
- [ ] Scaling policies set
- [ ] Monitoring enabled
- [ ] Rollback plan documented

### Post-Deployment
- [ ] Service health verified
- [ ] API endpoints responding
- [ ] Logs being collected
- [ ] Metrics being tracked
- [ ] Alerts configured
- [ ] Team notified
- [ ] Documentation updated

---

## Performance Optimization

### Backend
```python
# Gunicorn configuration (4 workers)
# Typical throughput: ~1000 requests/sec per worker
# Expected latency: <50ms per prediction
```

### Frontend
```javascript
// React optimizations
// - Code splitting
// - Lazy loading
// - Asset compression
// Expected load time: <2 seconds
```

### Model Inference
```python
# Model prediction time: ~5-10ms
# Batch predictions available for throughput
```

### Container
```dockerfile
# Multi-stage build reduces image size
# Python 3.9-slim: minimal OS footprint
# Result: ~500MB total image size
```

---

## Security Considerations

### Input Validation
```python
✓ Type checking (numeric values)
✓ Range validation (non-negative)
✓ Missing field detection
✓ Batch size limits (max 100)
```

### API Security
```python
✓ CORS enabled (configurable)
✓ JSON content-type validation
✓ Error message sanitization
✓ Rate limiting ready (Flask-Limiter)
```

### Container Security
```dockerfile
✓ Non-root user (best practice)
✓ Read-only filesystem (configurable)
✓ Resource limits (CPU, memory)
✓ Health checks enabled
✓ Minimal base image (slim variant)
```

### Environment Security
```bash
✓ Secrets in environment variables
✓ No hardcoded credentials
✓ .env.example template provided
✓ Production defaults (DEBUG=False)
```

---

## Scaling Strategies

### Vertical Scaling
```bash
# Increase container resources
docker run -m 2g -cpus 2 stress-detection:latest
```

### Horizontal Scaling
```yaml
# Kubernetes replicas
spec:
  replicas: 5  # Run 5 instances
  # Auto-scaling based on CPU/memory
```

### Caching Layer (Optional)
```python
# Redis for prediction caching
redis = Redis()
cache_key = hash(input_features)
result = redis.get(cache_key)
```

---

## Monitoring & Observability

### Metrics to Track
- API response time
- Error rate
- Request volume
- Model prediction latency
- Container resource usage
- Uptime percentage

### Tools Integration
- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **ELK Stack**: Logging
- **Datadog**: Full monitoring
- **New Relic**: APM

### Example: Prometheus Metrics
```python
from prometheus_client import Counter, Histogram

predictions = Counter('predictions_total', 'Total predictions')
latency = Histogram('prediction_latency_seconds', 'Prediction latency')
```

---

## Disaster Recovery

### Backup Strategy
```bash
# Back up trained model
aws s3 cp ml_logic/models/stress_model.pkl s3://backup-bucket/

# Back up training data
aws s3 sync ml_logic/data/ s3://backup-bucket/data/
```

### Rollback Procedure
```bash
# Keep previous Docker image tags
docker tag stress-detection:v2.0 stress-detection:v2.0-failed
docker tag stress-detection:v1.9 stress-detection:latest

# Redeploy previous version
docker run stress-detection:v1.9
```

### High Availability
```yaml
# Run multiple replicas across availability zones
spec:
  affinity:
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          topologyKey: kubernetes.io/hostname
```

---

## Development Workflow

### 1. Local Development
```bash
docker-compose up
# Frontend: http://localhost:3000
# Backend: http://localhost:5000
```

### 2. Feature Development
```bash
git checkout -b feature/new-feature
# Make changes...
git push origin feature/new-feature
# Create Pull Request
```

### 3. CI/CD Automation
```
GitHub Actions automatically:
- Builds Docker image
- Runs tests
- Scans security
- Deploys on PR merge
```

### 4. Production Monitoring
```
Cloud provider dashboard shows:
- Real-time logs
- Error rates
- Response times
- Resource usage
```

---

## Cost Estimation

### Render
- Hobby Plan: Free ($0)
- Standard Plan: $7/month + usage
- Pro Plan: Custom pricing

### Railway
- $5/month included credit
- Pay-as-you-go after credit

### AWS App Runner
- $0.064/vCPU-hour
- ~$50/month for small deployment
- Auto-scales based on load

### Total Estimated Monthly Cost
| Tier | Render | Railway | AWS |
|------|--------|---------|-----|
| Dev | $0 | $0 | $15 |
| Prod | $15 | $10 | $50 |
| High Traffic | $50+ | $30+ | $200+ |

---

## Next Steps

1. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/stress-detection-prod.git
   ```

2. **Review Documentation**
   - Read [README.md](README.md) for features
   - Review [DEPLOYMENT.md](DEPLOYMENT.md) for detailed steps

3. **Test Locally**
   ```bash
   docker-compose up
   # Visit http://localhost:5000/health
   ```

4. **Deploy to Cloud**
   - Choose platform (Render/Railway/AWS)
   - Follow platform-specific steps
   - Configure GitHub secrets

5. **Monitor in Production**
   - Check health endpoint
   - Monitor logs and metrics
   - Set up alerts

---

## Resources

### Documentation
- [README.md](README.md) - Project overview
- [DEPLOYMENT.md](DEPLOYMENT.md) - Detailed deployment guide
- [API Documentation](http://localhost:5000/docs) - Live API docs

### Tools & Platforms
- [Docker Documentation](https://docs.docker.com)
- [Render Docs](https://render.com/docs)
- [Railway Docs](https://docs.railway.app)
- [AWS App Runner](https://docs.aws.amazon.com/apprunner/)

### Learning Resources
- [MLOps Best Practices](https://ml-ops.systems/)
- [Container Security](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)
- [CI/CD with GitHub Actions](https://docs.github.com/en/actions)

---

**Last Updated**: January 2026
**Maintained by**: Your Name
**License**: MIT
