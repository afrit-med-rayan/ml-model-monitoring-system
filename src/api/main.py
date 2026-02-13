from fastapi import FastAPI
import os
import pandas as pd

app = FastAPI(title="ML Model Monitoring System API")

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
