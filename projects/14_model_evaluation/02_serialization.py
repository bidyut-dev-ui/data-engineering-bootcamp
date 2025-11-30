import joblib
import pandas as pd
import json
from datetime import datetime

def save_model_metadata(model, metrics, filename='model_metadata.json'):
    """Save model metadata for tracking"""
    metadata = {
        'model_type': type(model.named_steps['regressor']).__name__,
        'trained_at': datetime.now().isoformat(),
        'metrics': metrics,
        'features': list(model.feature_names_in_),
        'parameters': model.named_steps['regressor'].get_params()
    }
    
    with open(filename, 'w') as f:
        json.dump(metadata, f, indent=2, default=str)
    
    print(f"Metadata saved to {filename}")

def load_and_predict(model_path, input_data):
    """Load model and make prediction"""
    model = joblib.load(model_path)
    prediction = model.predict(input_data)
    return prediction

def main():
    print("=== Model Serialization Tutorial ===\n")
    
    # 1. Load the trained model
    print("1. Loading model...")
    model = joblib.load('housing_model.joblib')
    print(f"Model type: {type(model.named_steps['regressor']).__name__}")
    
    # 2. Save metadata
    print("\n2. Saving model metadata...")
    metrics = {
        'rmse': 45000.0,  # Example values
        'r2': 0.85,
        'mae': 32000.0
    }
    save_model_metadata(model, metrics)
    
    # 3. Make predictions on new data
    print("\n3. Making predictions on new data...")
    new_data = pd.DataFrame({
        'square_feet': [2000, 1500, 2500],
        'bedrooms': [3, 2, 4],
        'bathrooms': [2, 1, 3],
        'age_years': [10, 25, 5],
        'distance_to_city': [5, 15, 8]
    })
    
    print("Input data:")
    print(new_data)
    
    predictions = model.predict(new_data)
    print("\nPredictions:")
    for i, pred in enumerate(predictions):
        print(f"  House {i+1}: ${pred:,.2f}")
    
    # 4. Model versioning example
    print("\n4. Model versioning...")
    version = "v1.0.0"
    versioned_filename = f'housing_model_{version}.joblib'
    joblib.dump(model, versioned_filename)
    print(f"Saved versioned model: {versioned_filename}")
    
    print("\n✓ Model serialization complete!")

if __name__ == "__main__":
    main()
