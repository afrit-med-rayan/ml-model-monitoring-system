import requests
import time
import random
import numpy as np

API_URL = "http://localhost:8000/predict"
MONITOR_URL = "http://localhost:8000/monitoring/run"

def simulate_drift():
    print("Starting data drift simulation...")
    
    # Normal data (similar to reference)
    print("Sending normal data...")
    for _ in range(50):
        features = [random.uniform(-1, 1) for _ in range(10)]
        try:
            requests.post(API_URL, json={"features": features})
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(0.1)
    
    # Drifted data (shifted distributions)
    print("Sending drifted data (feature_1 and feature_2 shifted)...")
    for _ in range(50):
        # Shift feature_1 by +2 and feature_2 by -2
        features = [random.uniform(-1, 1) for _ in range(10)]
        features[0] += 2.0
        features[1] -= 2.0
        
        try:
            requests.post(API_URL, json={"features": features})
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(0.1)
    
    print("Drift simulation requests completed.")
    
    # Trigger monitoring
    print("Triggering monitoring report generation...")
    try:
        response = requests.post(MONITOR_URL)
        print(f"Monitoring result: {response.json()}")
    except Exception as e:
        print(f"Error sparking monitoring: {e}")

if __name__ == "__main__":
    simulate_drift()
