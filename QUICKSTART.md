# 🎯 GETTING STARTED GUIDE - 30 Minute Quick Start

Welcome! This guide will get you from zero to a working stress detection system in 30 minutes.

---

## Step 1: Choose Your Path (2 minutes)

### 🚀 Fastest Path: Docker (Recommended)
**Time:** 5 minutes setup + 2-3 minutes build = ~10 minutes total
**Pros:** No dependencies to install, works everywhere
**Cons:** Requires Docker installation
→ **Jump to:** [Path A: Docker](#path-a-docker)

### 💻 Developer Path: Local Development
**Time:** 10 minutes setup
**Pros:** Full control, hot reload, easiest for modifications
**Cons:** Requires Python + Node.js
→ **Jump to:** [Path B: Local](#path-b-local-development)

### ☁️ Cloud Path: Deploy Now
**Time:** 15-20 minutes
**Pros:** Live on the internet immediately
**Cons:** Requires GitHub + cloud account
→ **Jump to:** [Path C: Cloud](#path-c-cloud-deployment)

---

## Path A: Docker

### Prerequisites Check
```bash
# Check if Docker is installed
docker --version
# Should show: Docker version 20.10+

# If not installed:
# Windows/Mac: Download Docker Desktop
# Linux: sudo apt-get install docker.io
```

### Build & Run (5 minutes)
```bash
# Navigate to project
cd stress-detection-prod

# Build Docker image
docker build -t stress-detection:latest .
# Wait 2-3 minutes for build...

# Run container
docker run -p 5000:5000 stress-detection:latest

# In browser, visit:
http://localhost:5000
```

### Test the API
```bash
# In a new terminal:
curl http://localhost:5000/health
# Should return: {"status": "healthy", ...}

# Try a prediction
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"heart_rate": 75, "ecg": 0.5, "emg": 0.3, "gsr": 0.2, "resp": 0.4}'
# Should return: {"stress_level": "low", "confidence": 0.95, ...}
```

### Next Steps
✅ API is running at http://localhost:5000
✅ Frontend UI is available
✅ Ready to deploy or customize

→ [Customization](#customization) or [Deployment](#deployment)

---

## Path B: Local Development

### Prerequisites Check
```bash
# Check Python
python --version
# Should be 3.8 or higher

# Check Node.js
node --version
# Should be 14 or higher

# If missing, install from:
# Python: https://python.org
# Node.js: https://nodejs.org
```

### Automated Setup (Windows)
```bash
# In PowerShell:
cd stress-detection-prod
.\setup.bat
# Follows prompts automatically
```

### Automated Setup (Linux/macOS)
```bash
# In terminal:
cd stress-detection-prod
bash setup.sh
# Follows prompts automatically
```

### Manual Setup (All Platforms)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd client
npm install
cd ..

# Create environment file
cp server/.env.example server/.env
```

### Start Development Server (3 terminals needed)

**Terminal 1: Backend**
```bash
cd server
python app.py
# You should see: Running on http://0.0.0.0:5000
```

**Terminal 2: Frontend**
```bash
cd client
npm start
# You should see: webpack compiled successfully
# Browser opens to http://localhost:3000
```

**Terminal 3: Testing**
```bash
# Test API
curl http://localhost:5000/health

# Test prediction
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"heart_rate": 75, "ecg": 0.5, "emg": 0.3, "gsr": 0.2, "resp": 0.4}'
```

### Next Steps
✅ Backend API running at http://localhost:5000
✅ Frontend UI at http://localhost:3000
✅ Files auto-reload on save (hot reload enabled)

→ [Customization](#customization) or [Deployment](#deployment)

---

## Path C: Cloud Deployment

### Prerequisites
- GitHub account
- GitHub repository with this code
- Cloud platform account (Render recommended)

### Step 1: Push to GitHub
```bash
cd stress-detection-prod

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial production-ready stress detection app"

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Render (10 minutes)

**Go to:** https://render.com

**Click:** "New +" → "Web Service"

**Select:** Your GitHub repository

**Configure:**
| Setting | Value |
|---------|-------|
| Name | stress-detection-api |
| Environment | Docker |
| Build Command | (leave empty) |
| Start Command | (leave empty) |

**Environment Variables:**
```
FLASK_ENV=production
PORT=10000
```

**Click:** "Create Web Service"

**Wait:** 3-5 minutes for deployment

**Done!** Your app is live at: `https://stress-detection-api.onrender.com`

### Step 3: Test Cloud Deployment
```bash
# Replace with your actual URL
curl https://stress-detection-api.onrender.com/health

curl -X POST https://stress-detection-api.onrender.com/api/predict \
  -H "Content-Type: application/json" \
  -d '{"heart_rate": 75, "ecg": 0.5, "emg": 0.3, "gsr": 0.2, "resp": 0.4}'

# Visit in browser:
https://stress-detection-api.onrender.com
```

### Alternative Platforms

**Railway (5 minutes):**
```bash
npm install -g @railway/cli
railway login
railway init
railway up
railway open
```

**AWS App Runner (15 minutes):**
Follow detailed guide in [DEPLOYMENT.md](DEPLOYMENT.md)

### Next Steps
✅ Application is live on the internet
✅ URL is shareable with others
✅ Auto-updates with each GitHub push (after CI/CD setup)

→ [CI/CD Setup](#ci-cd-setup) or [Customization](#customization)

---

## Customization

### Change the Model Prediction Behavior

**Edit:** `server/predict.py`

```python
# Around line 45 - Change stress classes:
self.stress_classes = ['relaxed', 'normal', 'stressed']  # Customize labels

# Around line 113 - Add feature validation:
if value < 0 or value > 200:  # Add your own validation
    return False, f"Invalid {feature} value"
```

### Customize the User Interface

**Edit:** `client/src/StressPredictionForm.jsx`

```javascript
// Change form labels (line ~30)
<label>Heart Rate (BPM):</label>  // Customize this

// Change stress colors (line ~83)
case 'low':
  return '#4CAF50';  // Green - customize color

// Add new input fields (line ~120)
<div style={styles.inputGroup}>
  <label>New Sensor Input:</label>
  <input type="number" name="new_sensor" ... />
</div>
```

### Use Real Training Data

**Place CSV file:** `ml_logic/data/stress_data.csv`

**Format:**
```
heart_rate,ecg,emg,gsr,resp,stress_level
75,0.5,0.3,0.2,0.4,0
85,0.6,0.4,0.3,0.5,1
110,0.8,0.7,0.6,0.7,2
```

**Train model:**
```bash
python ml_logic/train.py
# Model saved to: ml_logic/models/stress_model.pkl
```

**Include in deployment:**
```bash
git add ml_logic/models/stress_model.pkl
git commit -m "Add trained model"
git push
```

### Add New API Endpoints

**Edit:** `server/app.py`

```python
@app.route('/api/my-feature', methods=['POST'])
def my_feature():
    """My new endpoint"""
    data = request.get_json()
    
    # Your logic here
    result = {"your": "result"}
    
    return jsonify(result), 200
```

**Then test:**
```bash
curl -X POST http://localhost:5000/api/my-feature \
  -H "Content-Type: application/json" \
  -d '{"param": "value"}'
```

---

## CI/CD Setup (Auto-Deploy on Push)

### Step 1: Create GitHub Secrets

Go to: GitHub repo → Settings → Secrets and variables → Actions

**For Render:**
```
Name: RENDER_DEPLOY_HOOK
Value: https://api.render.com/deploy/...
# Get this URL from Render dashboard → Settings → Deploy hook
```

**For Slack notifications (optional):**
```
Name: SLACK_WEBHOOK_URL
Value: https://hooks.slack.com/...
# Get from Slack App
```

### Step 2: Configure Variables

Go to: Settings → Variables → Repository variables

```
DEPLOY_TO_RENDER=true
```

### Step 3: Test CI/CD Pipeline

```bash
# Make a change
echo "# Updated" >> README.md

# Commit and push
git add .
git commit -m "Test CI/CD"
git push

# Watch: GitHub → Actions tab
# You should see workflow running
# Check logs for any errors
# After ~2 minutes, your cloud deployment updates automatically
```

### Pipeline Features
✅ Automatically builds Docker image on every push
✅ Runs tests (Python + JavaScript)
✅ Scans for security vulnerabilities
✅ Deploys to your cloud platform
✅ Sends Slack notification

---

## Troubleshooting Quick Fixes

### Docker Build Fails
```bash
# Solution 1: Check disk space
docker system prune -a

# Solution 2: Rebuild with fresh layers
docker build --no-cache -t stress-detection:latest .

# Solution 3: Check Docker logs
docker build -t stress-detection . --progress=plain
```

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :5000
kill -9 <PID>
```

### Module Not Found (Python)
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# For venv issues
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate  # or activate.bat
pip install -r requirements.txt
```

### npm Dependencies Issues
```bash
# Clear npm cache
npm cache clean --force

# Reinstall
rm -rf node_modules
npm install --legacy-peer-deps
```

### Frontend not connecting to backend
```bash
# Check backend is running
curl http://localhost:5000/health

# Check CORS is enabled
# In server/app.py, CORS should be configured
```

---

## Testing Endpoints

### Using cURL (Command line)

```bash
# Health check
curl http://localhost:5000/health

# Get features info
curl http://localhost:5000/api/features

# Single prediction - LOW stress
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "heart_rate": 70,
    "ecg": 0.3,
    "emg": 0.2,
    "gsr": 0.1,
    "resp": 0.3
  }'

# Single prediction - MEDIUM stress
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "heart_rate": 85,
    "ecg": 0.6,
    "emg": 0.5,
    "gsr": 0.4,
    "resp": 0.5
  }'

# Single prediction - HIGH stress
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "heart_rate": 110,
    "ecg": 0.8,
    "emg": 0.7,
    "gsr": 0.6,
    "resp": 0.7
  }'

# Batch predictions
curl -X POST http://localhost:5000/api/batch-predict \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {"heart_rate": 70, "ecg": 0.3, "emg": 0.2, "gsr": 0.1, "resp": 0.3},
      {"heart_rate": 85, "ecg": 0.6, "emg": 0.5, "gsr": 0.4, "resp": 0.5}
    ]
  }'
```

### Using Python

```python
import requests
import json

BASE_URL = "http://localhost:5000"

# Single prediction
response = requests.post(
    f"{BASE_URL}/api/predict",
    json={
        "heart_rate": 75,
        "ecg": 0.5,
        "emg": 0.3,
        "gsr": 0.2,
        "resp": 0.4
    }
)

print(json.dumps(response.json(), indent=2))
```

### Using Browser
```
http://localhost:5000/health
http://localhost:5000/api/features
http://localhost:5000/docs
```

---

## Key Files to Understand

### Understanding the Backend

**server/app.py** - Main API
- Lines 1-50: Imports & setup
- Lines 60-90: Health check endpoints
- Lines 100-150: Single prediction endpoint
- Lines 160-200: Batch prediction endpoint
- Lines 210-250: Feature information

**server/predict.py** - ML Logic
- Lines 1-50: Class initialization
- Lines 100-150: Input validation
- Lines 160-200: Making predictions
- Lines 210-250: Probability calculations

### Understanding the Frontend

**client/src/App.jsx** - Main app structure
**client/src/StressPredictionForm.jsx** - The form and API calls
**client/src/App.css** - Styling

### Understanding ML

**ml_logic/train.py** - How to train the model
**ml_logic/preprocessing.py** - Data preparation

---

## Next Steps After Basic Setup

### Day 1-2: Understanding
- [ ] Read README.md (5 min)
- [ ] Test all API endpoints (10 min)
- [ ] Explore code structure (20 min)
- [ ] Review DEPLOYMENT.md (10 min)

### Day 3-5: Customization
- [ ] Change model labels/colors
- [ ] Add custom input fields
- [ ] Adjust prediction thresholds
- [ ] Test changes locally

### Week 2: Deployment
- [ ] Set up GitHub repository
- [ ] Configure cloud platform
- [ ] Deploy to production
- [ ] Monitor in real-time

### Week 3+: Production
- [ ] Gather user feedback
- [ ] Collect real sensor data
- [ ] Retrain model with real data
- [ ] Monitor performance metrics
- [ ] Plan improvements

---

## Important Reminders

✅ **Always test locally first**
```bash
docker run -p 5000:5000 stress-detection:latest
# Test before pushing to cloud
```

✅ **Keep secrets in environment variables**
```bash
# DON'T do this:
api_key = "abc123"

# DO this:
api_key = os.getenv('API_KEY')
```

✅ **Use .env.example as template**
```bash
cp server/.env.example server/.env
# Edit server/.env with your settings
# .gitignore prevents committing secrets
```

✅ **Read error messages carefully**
```bash
# Example error message points you to:
ImportError: No module named 'flask'
# → Need to: pip install flask
```

---

## Support Resources

### Documentation
- **Getting Started:** This file
- **Detailed Setup:** [DEPLOYMENT.md](DEPLOYMENT.md)
- **API Usage:** [API-EXAMPLES.md](API-EXAMPLES.md)
- **Architecture:** [MLOps.md](MLOps.md)
- **Full Summary:** [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
- **File Structure:** [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md)

### External Resources
- [Flask Docs](https://flask.palletsprojects.com/)
- [React Docs](https://react.dev/)
- [Docker Docs](https://docs.docker.com/)
- [Render Docs](https://render.com/docs)
- [Railway Docs](https://railway.app/docs)

### Common Issues
- Check [IMPLEMENTATION_SUMMARY.md - Troubleshooting](IMPLEMENTATION_SUMMARY.md#troubleshooting)
- Search error messages in documentation
- Check Docker/npm logs

---

## You're Ready! 🎉

You now have:

✅ **Working application** - Fully functional stress detection system
✅ **Clean architecture** - Separated backend, frontend, ML logic  
✅ **Docker containerized** - Runs anywhere
✅ **CI/CD ready** - Auto-deploy on GitHub push
✅ **Cloud deployable** - Render, Railway, AWS support
✅ **Fully documented** - Complete guides for every step
✅ **Production hardened** - Input validation, error handling, security

### Your 30-Minute Timeline

| Time | Action |
|------|--------|
| 0-2 min | Choose your path (Docker/Local/Cloud) |
| 2-5 min | Setup prerequisites |
| 5-10 min | Build/run application |
| 10-15 min | Test endpoints |
| 15-20 min | Try customization |
| 20-25 min | Configure deployment |
| 25-30 min | Deploy to cloud (optional) |

---

## What to Do Next

**Just want to run it?**
→ See [Path A: Docker](#path-a-docker)

**Want to develop locally?**
→ See [Path B: Local Development](#path-b-local-development)

**Want to deploy immediately?**
→ See [Path C: Cloud Deployment](#path-c-cloud-deployment)

**Want detailed steps?**
→ Read [DEPLOYMENT.md](DEPLOYMENT.md)

**Want to understand architecture?**
→ Read [MLOps.md](MLOps.md)

---

**Happy coding! 🚀**

*Last Updated: January 2026*
*Status: Production Ready*
*Support: See documentation links above*
