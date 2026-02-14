from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os
import pandas as pd
import sys

# Add src to path to allow imports if needed, though with __init__.py it should be fine if run from root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from monitoring.run_monitoring import run_monitoring
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="ML Model Monitoring System API")

@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "ML Model Monitoring System API is running"}

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
