from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import os
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Models
try:
    model = joblib.load('model/rf_model.joblib')
    scaler = joblib.load('model/scaler.joblib')
    label_encoders = joblib.load('model/label_encoders.joblib')
    expected_columns = joblib.load('model/expected_columns.joblib')
except Exception as e:
    print(f"Error loading model: {e}")
    model, scaler, label_encoders, expected_columns = None, None, None, None

class LeadData(BaseModel):
    Name: str = "Unknown"
    Phone: str = "Unknown"
    Email: str = "Unknown"
    InterestLevel: str = "Auto Predict"
    Age: float
    Gender: str
    Location: str
    LeadSource: str
    TimeSpent: float
    PagesViewed: float
    LeadStatus: str
    EmailSent: int
    DeviceType: str
    ReferralSource: str
    FormSubmissions: int
    Downloads: int
    CTR_ProductPage: float
    ResponseTime: float
    FollowUpEmails: int
    SocialMediaEngagement: float
    PaymentHistory: str

@app.post("/api/lead")
def process_lead(lead: LeadData):
    if model is None:
        return {"error": "Model not trained. Train the model first."}
        
    data_dict = lead.model_dump()
    
    col_mapping = {
        "TimeSpent": "TimeSpent (minutes)",
        "ResponseTime": "ResponseTime (hours)"
    }
    
    mapped_dict = {}
    for k, v in data_dict.items():
        if k in col_mapping:
            mapped_dict[col_mapping[k]] = v
        else:
            mapped_dict[k] = v
            
    df = pd.DataFrame([mapped_dict])
    
    # Preprocessing
    for col in expected_columns:
        if col not in df.columns:
            df[col] = 0
            
    df = df[expected_columns]
    
    # Categorical Encoding
    for col in df.columns:
        if col in label_encoders:
            le = label_encoders[col]
            classes = list(le.classes_)
            # Handle unseen labels by mapping to 'Unknown' if it exists, else the first class
            fallback = 'Unknown' if 'Unknown' in classes else classes[0]
            df[col] = df[col].astype(str).apply(lambda x: x if x in classes else fallback)
            df[col] = le.transform(df[col])
            
    # Scaling
    X_scaled = scaler.transform(df)
    
    # Prediction Configuration based on explicit Interest Level or ML model
    interest_level = data_dict.get("InterestLevel", "Auto Predict")
    
    if interest_level == "High":
        prob = 0.85
        prediction = 1
    elif interest_level == "Medium":
        prob = 0.55
        prediction = 1
    elif interest_level == "Low":
        prob = 0.20
        prediction = 0
    else:
        # Auto-predict
        prob = float(model.predict_proba(X_scaled)[0][1])  # Probability of target=1
        prediction = int(prob > 0.5)
    
    # Workflow Orchestration Engine
    from workflow_engine import WorkflowOrchestrator
    orchestrator = WorkflowOrchestrator()
    events = orchestrator.process_lead(data_dict, prob)
        
    return {
        "status": "success",
        "prediction": prediction,
        "probability": prob,
        "workflow_events": events
    }
    
@app.get("/api/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
