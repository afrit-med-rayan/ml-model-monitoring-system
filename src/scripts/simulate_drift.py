import requests
import time
import random
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configurable API URL
API_BASE_URL = os.getenv("API_URL", "http://localhost:8000")
API_URL = f"{API_BASE_URL}/predict"
MONITOR_URL = f"{API_BASE_URL}/monitoring/run"

def simulate_drift():
    logger.info("Starting data drift simulation...")
    
    # Normal data (similar to reference)
    logger.info("Sending normal data...")
    for i in range(50):
        features = [random.uniform(-1, 1) for _ in range(10)]
        try:
            requests.post(API_URL, json={"features": features}, timeout=5)
        except Exception as e:
            logger.error(f"Error at request {i}: {e}")
        time.sleep(0.1)
    
    # Drifted data (shifted distributions)
    logger.info("Sending drifted data (feature_1 and feature_2 shifted)...")
    for i in range(50):
        # Shift feature_1 by +2 and feature_2 by -2
        features = [random.uniform(-1, 1) for _ in range(10)]
        features[0] += 2.0
        features[1] -= 2.0
        
        try:
            requests.post(API_URL, json={"features": features}, timeout=5)
        except Exception as e:
            logger.error(f"Error at request {i}: {e}")
        time.sleep(0.1)
    
    logger.info("Drift simulation requests completed.")
    
    # Trigger monitoring
    logger.info("Triggering monitoring report generation...")
    try:
        response = requests.post(MONITOR_URL, timeout=30)
        logger.info(f"Monitoring result: {response.json()}")
    except Exception as e:
        logger.error(f"Error triggering monitoring: {e}")

if __name__ == "__main__":
    simulate_drift()
