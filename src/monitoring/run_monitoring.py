import pandas as pd
import joblib
import os
from .monitor import ModelMonitor
from evidently.pipeline.column_mapping import ColumnMapping

def run_monitoring():
    # Load the model
    model_path = 'models/model.joblib'
    if not os.path.exists(model_path):
        print(f"Model not found at {model_path}. Please run src/train_model.py first.")
        return
    
    model = joblib.load(model_path)
    
    # Load data
    reference_data = pd.read_csv('data/reference.csv')
    current_data = pd.read_csv('data/current.csv')
    
    # Generate predictions
    X_ref = reference_data.drop('target', axis=1)
    X_curr = current_data.drop('target', axis=1)
    
    reference_data['prediction'] = model.predict(X_ref)
    current_data['prediction'] = model.predict(X_curr)
    
    # Define column mapping
    column_mapping = ColumnMapping()
    column_mapping.target = 'target'
    column_mapping.prediction = 'prediction'
    column_mapping.numerical_features = [f"feature_{i+1}" for i in range(10)]
    
    # Initialize monitor
    monitor = ModelMonitor()
    
    # Run full monitoring suite
    print("Running full monitoring suite...")
    monitor.run_full_suite(reference_data, current_data, column_mapping=column_mapping)
    
    # Save the report
    report_dir = 'reports'
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
        
    report_path = os.path.join(report_dir, 'monitoring_report.html')
    monitor.save_report(report_path)
    print(f"Report generated and saved to {report_path}")
    
    # Extract metrics for the API
    results = monitor.report.as_dict()
    
    # Try to extract data drift score
    drift_score = 0
    try:
        # Evidently 0.4.x+ structure
        for metric in results['metrics']:
            if metric['metric'] == 'DatasetDriftMetric':
                drift_score = metric['result']['drift_share']
                break
    except:
        pass

    # Try to extract accuracy
    accuracy_score = 0
    try:
        for metric in results['metrics']:
            if metric['metric'] == 'ClassificationQualityMetric':
                accuracy_score = metric['result']['current']['accuracy']
                break
    except:
        pass
        
    return {
        "drift": drift_score,
        "accuracy": accuracy_score
    }

if __name__ == "__main__":
    run_monitoring()
