from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import numpy as np
from typing import Optional

app = FastAPI(title="Obesity Classification API")

# Configure CORS to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local testing
        "https://*.vercel.app"     # Your Vercel deployment
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained model and related files
try:
    with open("obesity_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("feature_names.pkl", "rb") as f:
        feature_names = pickle.load(f)
    with open("label_mapping.pkl", "rb") as f:
        label_mapping = pickle.load(f)
except Exception as e:
    print(f"Error loading model files: {e}")
    model = None
    feature_names = None
    label_mapping = None


# Define input data model
class UserInput(BaseModel):
    weight: float
    height: float  # in meters
    gender: str  # "Male" or "Female"
    age: int
    high_caloric_food: str  # "Yes" or "No"
    alcohol_intake: str  # "no", "Sometimes", "Frequently", "Always"
    vegetable_intake: int  # 1, 2, or 3 (FCVC)
    main_meals: int  # NCP


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Obesity Classification API is running",
        "status": "healthy",
        "model_loaded": model is not None
    }


@app.post("/predict")
async def predict(user_input: UserInput):
    """
    Predict obesity classification based on user inputs
    """
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Prepare input features
        # Encode categorical variables to match training data
        # Alcohol intake encoding
        alcohol_map = {'no': 0, 'Sometimes': 1, 'Frequently': 2, 'Always': 3}
        
        # Feature names from pickle are capitalized
        features = {
            'Weight': user_input.weight,
            'Height': user_input.height,
            'Gender': 1 if user_input.gender.lower() == "male" else 0,
            'Age': user_input.age,
            'FAVC': 1 if user_input.high_caloric_food.lower() == "yes" else 0,
            'CALC': alcohol_map.get(user_input.alcohol_intake, 0),
            'FCVC': user_input.vegetable_intake,  # Already 1-3
            'NCP': user_input.main_meals
        }
        
        print(f"Input features: {features}")
        print(f"Feature names from pickle: {feature_names}")
        
        # Convert to numpy array in the correct order
        if feature_names:
            feature_values = [features.get(name, 0) for name in feature_names]
        else:
            feature_values = list(features.values())
        
        print(f"Feature values: {feature_values}")
        print(f"Model type: {type(model)}")
        
        input_array = np.array([feature_values])
        
        # Make prediction
        # Check if model is actually a model object or just an array
        if hasattr(model, 'predict'):
            prediction = model.predict(input_array)[0]
        else:
            # If model is an array, it might be predictions - handle this case
            raise HTTPException(status_code=500, detail="Model file appears to be invalid. Please ensure obesity_model.pkl contains a trained model object, not a numpy array.")
        
        # Get class label if label_mapping exists
        if label_mapping:
            # Reverse the label mapping to get class name
            reverse_mapping = {v: k for k, v in label_mapping.items()}
            prediction_label = reverse_mapping.get(prediction, f"Class {prediction}")
        else:
            prediction_label = f"Class {prediction}"
        
        # Get probability if available
        probability = None
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(input_array)[0]
            probability = float(max(proba))
        
        return {
            "prediction": prediction_label,
            "confidence": probability,
            "input_data": user_input.dict()
        }
    
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"Error occurred: {error_detail}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
