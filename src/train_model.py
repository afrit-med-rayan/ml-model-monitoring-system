import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

def train_model():
    # Load reference data
    df = pd.read_csv('data/reference.csv')
    
    X = df.drop('target', axis=1)
    y = df['target']
    
    # Train a simple model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Evaluate on the training set (just for sanity check)
    preds = model.predict(X)
    acc = accuracy_score(y, preds)
    f1 = f1_score(y, preds)
    
    print(f"Model training completed. Accuracy: {acc:.4f}, F1 Score: {f1:.4f}")
    
    # Save the model
    joblib.dump(model, 'models/model.joblib')
    print("Model saved to models/model.joblib")

if __name__ == "__main__":
    train_model()
