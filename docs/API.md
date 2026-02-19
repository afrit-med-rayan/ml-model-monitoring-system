# API Documentation

The ML Model Monitoring System API provides endpoints for model inference, health checks, and monitoring triggers.

## Base URL
Default: `http://localhost:8000`

## Endpoints

### 1. Health Check
`GET /health`
- **Description**: Returns the status of the API.
- **Response**:
  ```json
  {
    "status": "ok",
    "message": "ML Model Monitoring System API is running"
  }
  ```

### 2. Model Prediction
`POST /predict`
- **Description**: Makes a prediction using the trained ML model.
- **Request Body**:
  ```json
  {
    "features": [5.1, 3.5, 1.4, 0.2]
  }
  ```
- **Response**:
  ```json
  {
    "prediction": 0.0
  }
  ```

### 3. Run Monitoring
`POST /monitoring/run`
- **Description**: Triggers the Evidently monitoring suite to analyze current data against reference data. Updates Prometheus metrics.
- **Response**:
  ```json
  {
    "status": "success",
    "message": "Monitoring report generated successfully",
    "report_path": "reports/monitoring_report.html",
    "metrics": {
      "drift": 0.1,
      "accuracy": 0.95
    },
    "alerts": []
  }
  ```

### 4. Latest Report
`GET /reports/latest`
- **Description**: Serves the latest generated HTML monitoring report.
- **Response**: HTML File.

### 5. Data Status
`GET /data/status`
- **Description**: Returns information about reference and current data files.
- **Response**:
  ```json
  {
    "reference_data": {
      "exists": true,
      "path": "data/reference.csv",
      "rows": 120
    },
    "current_data": {
      "exists": true,
      "path": "data/current.csv",
      "rows": 50
    }
  }
  ```

### 6. Model Status
`GET /model/status`
- **Description**: Checks if the model file exists and is loaded.
- **Response**:
  ```json
  {
    "model_loaded": true,
    "model_path": "models/model.joblib",
    "message": "Model is available"
  }
  ```

## Prometheus Metrics
The API exposes metrics at `/metrics` (handled by `prometheus-fastapi-instrumentator`). Custom metrics include:
- `ml_model_drift_score`: Latest data drift score.
- `ml_model_accuracy_score`: Latest accuracy score.
- `ml_model_prediction_volume`: Total predictions made.
