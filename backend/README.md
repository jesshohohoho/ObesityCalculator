# Backend - Obesity Classification API

## Setup Instructions

1. **Place your model files** in this backend folder:
   - `obesity_model.pkl`
   - `feature_names.pkl`
   - `label_mapping.pkl`

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run locally:**
   ```bash
   python main.py
   ```
   
   Or using uvicorn:
   ```bash
   uvicorn main:app --reload
   ```

4. **Test the API:**
   - Open http://localhost:8000 in your browser
   - API docs available at http://localhost:8000/docs

## Deployment on Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set the following:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory:** `backend`
4. Upload your .pkl files or commit them to your repository
5. Deploy!
