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

def simulate_performance_degradation():
    logger.info("Starting performance degradation simulation...")
    
    # Simulate high load and noisy data
    logger.info("Sending 200 requests with high noise...")
    for i in range(200):
        # Features with high noise/randomness
        features = [random.uniform(-5, 5) for _ in range(10)]
        
        try:
            # Simulate some network latency in the caller
            if i % 10 == 0:
                time.sleep(0.5)
            
            requests.post(API_URL, json={"features": features}, timeout=5)
        except Exception as e:
            logger.error(f"Error at request {i}: {e}")
            
    logger.info("Performance simulation requests completed.")
    
    # Trigger monitoring
    logger.info("Triggering monitoring report generation...")
    try:
        response = requests.post(MONITOR_URL, timeout=30)
        logger.info(f"Monitoring result: {response.json()}")
    except Exception as e:
        logger.error(f"Error triggering monitoring: {e}")

if __name__ == "__main__":
    simulate_performance_degradation()
