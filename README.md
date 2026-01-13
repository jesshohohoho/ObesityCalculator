# Obesity Classification Web App

A simple web application for obesity classification using machine learning.

## 🏗️ Project Structure

```
ObesityApp/
├── backend/               # FastAPI backend
│   ├── main.py           # API endpoints
│   ├── requirements.txt  # Python dependencies
│   ├── obesity_model.pkl      # YOUR MODEL FILES (add these)
│   ├── feature_names.pkl      # YOUR MODEL FILES (add these)
│   └── label_mapping.pkl      # YOUR MODEL FILES (add these)
│
├── frontend/             # Web interface
│   ├── index.html       # Main HTML page
│   ├── styles.css       # Styling
│   └── script.js        # Frontend logic
│
└── vercel.json          # Vercel deployment config
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js (for Vercel CLI, optional)

### 1️⃣ Setup Backend

1. **Copy your model files** to the `backend/` folder:
   - `obesity_model.pkl`
   - `feature_names.pkl`
   - `label_mapping.pkl`

2. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Run the backend:**
   ```bash
   python main.py
   ```
   
   Backend will run at http://localhost:8000

### 2️⃣ Setup Frontend

1. **Open the frontend:**
   - Simply open `frontend/index.html` in your browser
   - Or use a local server:
     ```bash
     cd frontend
     python -m http.server 3000
     ```

2. **Test the app:**
   - Fill in the form with your data
   - Click "Get Classification"
   - View the results!

## 📦 Deployment

### Deploy Backend on Render

1. **Push code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Create Web Service on Render:**
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name:** obesity-classification-api
     - **Root Directory:** `backend`
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Click "Create Web Service"

3. **Note your backend URL:**
   - Example: `https://obesity-classification-api.onrender.com`

### Deploy Frontend on Vercel

1. **Install Vercel CLI (optional):**
   ```bash
   npm install -g vercel
   ```

2. **Deploy:**
   - **Option A: Using Vercel CLI**
     ```bash
     cd frontend
     vercel
     ```
   
   - **Option B: Using Vercel Dashboard**
     - Go to https://vercel.com
     - Click "Add New" → "Project"
     - Import your GitHub repository
     - Set Root Directory to `frontend`
     - Click "Deploy"

3. **Update API URL:**
   - Open `frontend/script.js`
   - Change line 2:
     ```javascript
     const API_URL = 'https://your-render-backend-url.onrender.com';
     ```
   - Redeploy

### Update CORS Settings

After deploying frontend, update `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-vercel-app.vercel.app"],
    # ... rest of settings
)
```

Then redeploy the backend.

## 🧪 Testing the API

### Using curl:
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "weight": 75,
    "height": 170,
    "gender": "Male",
    "age": 25,
    "high_caloric_food": "No",
    "alcohol_intake": "No",
    "vegetable_intake": "Yes",
    "main_meals": 3
  }'
```

### Using browser:
- Visit http://localhost:8000/docs for interactive API documentation

## 📝 Notes

- Make sure your model files are in the correct format (pickle files)
- The backend expects specific feature names - adjust the code if your model uses different features
- Free tier on Render may have cold starts (first request might be slow)

## 🐛 Troubleshooting

**Backend won't start:**
- Check if all .pkl files are present
- Verify Python version compatibility
- Check requirements.txt dependencies

**Frontend can't connect:**
- Verify backend is running
- Check API_URL in script.js
- Check browser console for CORS errors

**Model prediction fails:**
- Verify feature names match your model
- Check data types and encoding match training data

## 📄 License

MIT License - Feel free to use this for your projects!
