import requests
import time
import random

API_URL = "http://localhost:8000/predict"
MONITOR_URL = "http://localhost:8000/monitoring/run"

def simulate_performance_degradation():
    print("Starting performance degradation simulation...")
    
    # Simulate high load and noisy data
    print("Sending 200 requests with high noise...")
    for i in range(200):
        # Features with high noise/randomness
        features = [random.uniform(-5, 5) for _ in range(10)]
        
        try:
            # Simulate some network latency in the caller
            if i % 10 == 0:
                time.sleep(0.5)
            
            requests.post(API_URL, json={"features": features})
        except Exception as e:
            print(f"Error at request {i}: {e}")
            
    print("Performance simulation requests completed.")
    
    # Trigger monitoring
    print("Triggering monitoring report generation...")
    try:
        response = requests.post(MONITOR_URL)
        print(f"Monitoring result: {response.json()}")
    except Exception as e:
        print(f"Error triggering monitoring: {e}")

if __name__ == "__main__":
    simulate_performance_degradation()
