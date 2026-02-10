import pandas as pd
import os
import sys

# Add src to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from monitoring.monitor import ModelMonitor

def test_prediction_drift():
    # Load data
    try:
        reference = pd.read_csv('data/reference.csv')
        current = pd.read_csv('data/current.csv')
    except FileNotFoundError:
        print("Data files not found. Generating dummy data...")
        import numpy as np
        reference = pd.DataFrame(np.random.normal(0, 1, size=(100, 5)), columns=[f'col_{i}' for i in range(5)])
        reference['target'] = np.random.randint(0, 2, size=100)
        
        current = pd.DataFrame(np.random.normal(0.5, 1, size=(100, 5)), columns=[f'col_{i}' for i in range(5)])
        current['target'] = np.random.randint(0, 2, size=100)

    # Initialize monitor
    monitor = ModelMonitor()
    
    # Run prediction drift detection
    print("Running Prediction Drift detection...")
    # Expecting 'target' column to be present for TargetDriftPreset
    monitor.detect_prediction_drift(reference_data=reference, current_data=current)
    
    # Save report
    report_path = 'prediction_drift_report.html'
    monitor.save_report(report_path)
    
    if os.path.exists(report_path):
        print(f"Success! Report saved to {report_path}")
    else:
        print("Error: Report was not saved.")

if __name__ == "__main__":
    test_prediction_drift()
