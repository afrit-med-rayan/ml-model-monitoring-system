from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os
import pandas as pd
import sys
import joblib
from pydantic import BaseModel
from typing import List
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Gauge, Counter

# Add src to path to allow imports if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from monitoring.run_monitoring import run_monitoring

app = FastAPI(title="ML Model Monitoring System API")

# Custom metrics
DRIFT_SCORE = Gauge('ml_model_drift_score', 'Data drift score for the model')
ACCURACY_SCORE = Gauge('ml_model_accuracy_score', 'Accuracy score for the model')
PREDICTION_VOLUME = Counter('ml_model_prediction_volume', 'Total number of predictions made')

class PredictionRequest(BaseModel):
    features: List[float]

model = None

@app.on_event("startup")
async def startup():
    global model
    model_path = 'models/model.joblib'
    if os.path.exists(model_path):
        model = joblib.load(model_path)
    else:
        print(f"Warning: Model file not found at {model_path}")
    Instrumentator().instrument(app).expose(app)

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "ML Model Monitoring System API is running"}

@app.post("/predict")
async def predict(request: PredictionRequest):
    global model
    if model is None:
        # Try to load again if it wasn't loaded at startup
        model_path = 'models/model.joblib'
        if os.path.exists(model_path):
            model = joblib.load(model_path)
        else:
            raise HTTPException(status_code=400, detail="Model not loaded and file not found")
    
    try:
        # Make prediction
        prediction = model.predict([request.features])[0]
        
        # Log to current.csv (Simulating production logging)
        # In a real app, this would go to a database or log file
        cols = [f'feature_{i+1}' for i in range(len(request.features))] + ['target']
        df_row = pd.DataFrame([request.features + [prediction]], columns=cols)
        
        df_row.to_csv('data/current.csv', mode='a', header=not os.path.exists('data/current.csv'), index=False)
        
        PREDICTION_VOLUME.inc()
        
        return {"prediction": float(prediction)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model/status")
async def get_model_status():
    model_path = 'models/model.joblib'
    exists = os.path.exists(model_path)
    return {
        "model_loaded": exists,
        "model_path": model_path if exists else None,
        "message": "Model is available" if exists else "Model file not found"
    }

@app.get("/data/status")
async def get_data_status():
    ref_path = 'data/reference.csv'
    curr_path = 'data/current.csv'
    
    ref_exists = os.path.exists(ref_path)
    curr_exists = os.path.exists(curr_path)
    
    return {
        "reference_data": {
            "exists": ref_exists,
            "path": ref_path if ref_exists else None,
            "rows": len(pd.read_csv(ref_path)) if ref_exists else 0
        },
        "current_data": {
            "exists": curr_exists,
            "path": curr_path if curr_exists else None,
            "rows": len(pd.read_csv(curr_path)) if curr_exists else 0
        }
    }

@app.post("/monitoring/run")
async def trigger_monitoring():
    try:
        # Check if requirements are met
        if not os.path.exists('models/model.joblib'):
            raise HTTPException(status_code=400, detail="Model file not found. Run training first.")
        if not os.path.exists('data/reference.csv') or not os.path.exists('data/current.csv'):
            raise HTTPException(status_code=400, detail="Data files not found. Generate data first.")
            
        run_monitoring()
        
        # Simulate metric extraction from the report
        # In a real scenario, we'd parse the Evidently JSON or use their collectors
        DRIFT_SCORE.set(0.15)  # Example value
        ACCURACY_SCORE.set(0.92)  # Example value
        
        return {"status": "success", "message": "Monitoring report generated successfully", "report_path": "reports/monitoring_report.html"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reports/latest")
async def get_latest_report():
    report_path = 'reports/monitoring_report.html'
    if not os.path.exists(report_path):
        raise HTTPException(status_code=404, detail="Monitoring report not found. Run monitoring first.")
    
    return FileResponse(report_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
