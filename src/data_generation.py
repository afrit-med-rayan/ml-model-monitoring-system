import pandas as pd
import numpy as np
from sklearn.datasets import make_classification

def generate_data():
    # Generate a classification dataset
    X, y = make_classification(
        n_samples=2000, 
        n_features=10, 
        n_informative=5, 
        n_redundant=2, 
        random_state=42
    )
    
    columns = [f"feature_{i+1}" for i in range(10)]
    df = pd.DataFrame(X, columns=columns)
    df['target'] = y
    
    # Split into reference (first 1000) and current (next 1000)
    reference = df.iloc[:1000].copy()
    current = df.iloc[1000:].copy()
    
    # Introduce drift in 'feature_1' for the current dataset
    current['feature_1'] = current['feature_1'] + 0.5
    
    # Save datasets
    reference.to_csv('data/reference.csv', index=False)
    current.to_csv('data/current.csv', index=False)
    
    print("Data generated successfully.")
    print("Reference data shape:", reference.shape)
    print("Current data shape:", current.shape)

if __name__ == "__main__":
    generate_data()
