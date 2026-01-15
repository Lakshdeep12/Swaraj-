# Deployment Guide for Stress Detection Application

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development](#local-development)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements
- Git
- Docker & Docker Compose (for containerized deployment)
- Cloud CLI tools (for cloud deployment)
- Python 3.8+ (for local development)
- Node.js 14+ (for frontend development)

### Required Credentials
- GitHub account and repository access
- Cloud provider account (Render, Railway, or AWS)
- Optionally: Docker Hub account for image registry

---

## Local Development

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/stress-detection-prod.git
cd stress-detection-prod
```

### 2. Setup Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup Node Environment
```bash
cd client
npm install
cd ..
```

### 4. Train the Model (Optional)
```bash
python ml_logic/train.py
# Model will be saved to ml_logic/models/stress_model.pkl
```

### 5. Run Locally
```bash
# Terminal 1: Start Flask backend
cd server
python app.py
# Server will be available at http://localhost:5000

# Terminal 2: Start React frontend (optional)
cd client
npm start
# Frontend will be available at http://localhost:3000
```

### 6. Test the API
```bash
# Health check
curl http://localhost:5000/health

# Make a prediction
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "heart_rate": 75,
    "ecg": 0.5,
    "emg": 0.3,
    "gsr": 0.2,
    "resp": 0.4
  }'
```

---

## Docker Deployment

### 1. Build Docker Image
```bash
# Build the image (includes frontend and backend)
docker build -t stress-detection:latest .

# Or with a custom tag
docker build -t stress-detection:v1.0 .
```

### 2. Run Container Locally
```bash
# Run with default settings
docker run -p 5000:5000 stress-detection:latest

# Run with environment variables
docker run -p 5000:5000 \
  -e FLASK_ENV=production \
  -e MODEL_PATH=/app/ml_logic/models/stress_model.pkl \
  stress-detection:latest

# Run in background
docker run -d -p 5000:5000 \
  --name stress-detection-app \
  stress-detection:latest

# Check logs
docker logs stress-detection-app

# Stop container
docker stop stress-detection-app
```

### 3. Using Docker Compose (Development)
```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop all services
docker-compose down
```

### 4. Push to Docker Registry
```bash
# Login to Docker Hub
docker login

# Tag image
docker tag stress-detection:latest yourusername/stress-detection:latest

# Push image
docker push yourusername/stress-detection:latest

# Or use GitHub Container Registry
docker tag stress-detection:latest ghcr.io/yourusername/stress-detection:latest
docker push ghcr.io/yourusername/stress-detection:latest
```

---

## Cloud Deployment

### Option 1: Deploy to Render

#### Step 1: Prepare Repository
```bash
# Ensure Dockerfile is in root directory
# Ensure requirements.txt contains all dependencies
# Push changes to GitHub
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

#### Step 2: Create Render Service
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure service:
   - **Name**: stress-detection-api
   - **Environment**: Docker
   - **Branch**: main
   - **Build Command**: (leave empty - auto-detects Dockerfile)
   - **Start Command**: (leave empty - auto-detects)

#### Step 3: Set Environment Variables
1. In Render dashboard, go to Environment
2. Add variables:
   ```
   FLASK_ENV=production
   MODEL_PATH=/app/ml_logic/models/stress_model.pkl
   PORT=10000
   ```

#### Step 4: Deploy
1. Click "Create Web Service"
2. Render automatically builds and deploys
3. Service URL will be provided: `https://stress-detection-api.onrender.com`

#### Step 5: Test Deployment
```bash
curl https://stress-detection-api.onrender.com/health

curl -X POST https://stress-detection-api.onrender.com/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "heart_rate": 75,
    "ecg": 0.5,
    "emg": 0.3,
    "gsr": 0.2,
    "resp": 0.4
  }'
```

---

### Option 2: Deploy to Railway

#### Step 1: Install Railway CLI
```bash
npm install -g @railway/cli

# Or on macOS
brew install railway
```

#### Step 2: Login to Railway
```bash
railway login
```

#### Step 3: Initialize Railway Project
```bash
railway init
# Follow prompts to create new project
```

#### Step 4: Deploy
```bash
# Deploy from local environment
railway up

# Or link existing GitHub repo
railway link
```

#### Step 5: Set Environment Variables
```bash
railway variables set FLASK_ENV=production
railway variables set MODEL_PATH=/app/ml_logic/models/stress_model.pkl
```

#### Step 6: Check Status
```bash
# View deployed service
railway status

# View logs
railway logs
```

#### Step 7: Get Public URL
```bash
railway open
# Opens your deployed application in browser
```

---

### Option 3: Deploy to AWS App Runner

#### Prerequisites
- AWS Account
- AWS CLI installed and configured
- Docker image pushed to Amazon ECR

#### Step 1: Push Image to ECR
```bash
# Create ECR repository
aws ecr create-repository --repository-name stress-detection

# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <YOUR-ACCOUNT-ID>.dkr.ecr.us-east-1.amazonaws.com

# Tag and push image
docker tag stress-detection:latest <YOUR-ACCOUNT-ID>.dkr.ecr.us-east-1.amazonaws.com/stress-detection:latest
docker push <YOUR-ACCOUNT-ID>.dkr.ecr.us-east-1.amazonaws.com/stress-detection:latest
```

#### Step 2: Create App Runner Service via AWS Console
1. Go to [AWS App Runner Console](https://console.aws.amazon.com/apprunner)
2. Click "Create service"
3. Select "Container image URI"
4. Enter ECR image URI
5. Configure service:
   - **Service name**: stress-detection-api
   - **Port**: 5000
   - **CPU**: 1 vCPU
   - **Memory**: 2 GB

#### Step 3: Set Environment Variables
1. In service configuration, add environment variables:
   ```
   FLASK_ENV=production
   MODEL_PATH=/app/ml_logic/models/stress_model.pkl
   ```

#### Step 4: Create and Deploy
1. Click "Create & deploy"
2. Wait for service to be active
3. Copy service URL from dashboard

#### Step 5: Verify Deployment
```bash
curl https://<app-runner-url>/health
```

---

### Option 4: Deploy with Kubernetes (Advanced)

#### Create deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: stress-detection
spec:
  replicas: 2
  selector:
    matchLabels:
      app: stress-detection
  template:
    metadata:
      labels:
        app: stress-detection
    spec:
      containers:
      - name: stress-detection
        image: yourusername/stress-detection:latest
        ports:
        - containerPort: 5000
        env:
        - name: FLASK_ENV
          value: production
        - name: MODEL_PATH
          value: /app/ml_logic/models/stress_model.pkl
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
```

#### Deploy to Kubernetes
```bash
kubectl apply -f deployment.yaml
kubectl expose deployment stress-detection --type=LoadBalancer --port=80 --target-port=5000
kubectl get services
```

---

## CI/CD with GitHub Actions

The repository includes a GitHub Actions workflow (`.github/workflows/deploy.yml`) that automatically:

1. **Builds** Docker image on every push
2. **Runs** linting and tests
3. **Scans** for vulnerabilities
4. **Deploys** to selected cloud providers

### Setup GitHub Secrets

1. Go to GitHub repository → Settings → Secrets
2. Add these secrets:

```
# For Render
RENDER_DEPLOY_HOOK: https://api.render.com/deploy/...

# For Railway
RAILWAY_TOKEN: <your-railway-token>

# For AWS
AWS_ACCESS_KEY_ID: <your-aws-key>
AWS_SECRET_ACCESS_KEY: <your-aws-secret>
AWS_REGION: us-east-1
AWS_APP_RUNNER_SERVICE: stress-detection-api

# For Slack notifications (optional)
SLACK_WEBHOOK_URL: https://hooks.slack.com/...
```

### Enable Deployments in Workflow

Set repository variables in Settings → Variables:

```
DEPLOY_TO_RENDER=true        # or false
DEPLOY_TO_RAILWAY=false      # or true
DEPLOY_TO_AWS=false          # or true
```

---

## Production Checklist

- [ ] Environment variables are set correctly
- [ ] Model file is included in deployment
- [ ] Database/storage is configured (if needed)
- [ ] Logging is enabled and monitored
- [ ] Health checks are passing
- [ ] API endpoints are responding
- [ ] CORS is configured correctly
- [ ] SSL/HTTPS is enabled
- [ ] Rate limiting is enabled
- [ ] Monitoring and alerts are set up
- [ ] Backups are configured
- [ ] Documentation is updated

---

## Troubleshooting

### Docker Build Fails
```bash
# Check Docker logs
docker build -t stress-detection:latest . --progress=plain

# Free up disk space
docker system prune -a

# Use specific Python version
# Edit Dockerfile: FROM python:3.9-slim
```

### Container Won't Start
```bash
# Check container logs
docker logs <container-id>

# Run with interactive shell
docker run -it stress-detection:latest /bin/bash

# Check port availability
netstat -tulpn | grep 5000
```

### API Returns 404
```bash
# Verify container is running
docker ps

# Test endpoint inside container
docker exec <container-id> curl http://localhost:5000/health
```

### Model Not Found
```bash
# Train model locally first
python ml_logic/train.py

# Verify file exists
ls -la ml_logic/models/

# Include in Docker build
# Ensure COPY ml_logic ./ml_logic is in Dockerfile
```

### High Memory Usage
```bash
# Reduce gunicorn workers in Dockerfile
CMD ["gunicorn", "--workers", "2", ...]

# Limit container memory
docker run -m 512m stress-detection:latest
```

---

## Monitoring & Logs

### Render
- Dashboard → Logs tab
- Real-time log streaming
- Error alerts

### Railway
```bash
railway logs --follow
```

### AWS App Runner
- CloudWatch Logs
- Container Insights monitoring

### Local Docker
```bash
docker logs -f stress-detection-app
```

---

## Scaling & Performance

### Horizontal Scaling
- Use Kubernetes for multi-replica deployments
- AWS App Runner auto-scales based on demand
- Railway & Render handle auto-scaling

### Vertical Scaling
```bash
# Increase container resources in cloud provider dashboard
# Or in Dockerfile:
# Adjust gunicorn workers based on CPU cores
# CMD ["gunicorn", "--workers", "4", ...]
```

### Caching
- Implement Redis for model predictions cache
- Use CDN for static frontend files

---

## Security Best Practices

1. **Keep dependencies updated**
   ```bash
   pip list --outdated
   npm outdated
   ```

2. **Use secrets management**
   - AWS Secrets Manager
   - Render Environment Secrets
   - GitHub Secrets

3. **Enable HTTPS**
   - All cloud providers provide free SSL

4. **Rate limiting**
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app)
   @app.route('/api/predict')
   @limiter.limit("100/hour")
   def predict():
       ...
   ```

5. **Input validation**
   - Already implemented in `predict.py`

---

## Support & Resources

- GitHub Issues: [Report bugs](https://github.com/yourusername/stress-detection-prod/issues)
- Documentation: [Full API Docs](README.md)
- Cloud Provider Docs:
  - [Render Docs](https://render.com/docs)
  - [Railway Docs](https://railway.app/docs)
  - [AWS App Runner Docs](https://docs.aws.amazon.com/apprunner/)

---

**Last Updated**: January 2026
