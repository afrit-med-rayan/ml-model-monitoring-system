from fastapi import FastAPI

app = FastAPI(title="ML Model Monitoring System API")

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "ML Model Monitoring System API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
