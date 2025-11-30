import json
import pandas as pd

def process_pipeline():
    print("🚀 Starting Pipeline...")
    
    # 1. Process V1 Data (Expected Schema)
    print("\n--- Processing V1 Data ---")
    try:
        df_v1 = pd.read_json('data_v1.json')
        # Expecting 'name' and 'email'
        if 'name' not in df_v1.columns or 'email' not in df_v1.columns:
            raise ValueError("Schema Mismatch: Missing 'name' or 'email'")
        print("✅ V1 Data Valid:")
        print(df_v1)
    except Exception as e:
        print(f"❌ V1 Failed: {e}")

    # 2. Process V2 Data (Unexpected Schema)
    print("\n--- Processing V2 Data ---")
    try:
        df_v2 = pd.read_json('data_v2.json')
        
        # Check for required columns
        required_cols = ['id', 'name', 'email']
        missing = [col for col in required_cols if col not in df_v2.columns]
        
        if missing:
            print(f"❌ CRITICAL ALERT: Schema changed! Missing columns: {missing}")
            print("   Pipeline stopped to prevent data corruption.")
            
            # 3. Handling Evolution (The Fix)
            print("\n--- Applying Schema Evolution Logic ---")
            # Logic: If 'first_name' exists but 'name' doesn't, combine them
            if 'first_name' in df_v2.columns and 'last_name' in df_v2.columns:
                print("   🔧 Detected new schema (first/last name). Adapting...")
                df_v2['name'] = df_v2['first_name'] + " " + df_v2['last_name']
            
            # Logic: If 'email' is missing, fill with None
            if 'email' not in df_v2.columns:
                print("   🔧 Detected missing 'email'. Filling with None...")
                df_v2['email'] = None
                
            # Now it matches our target schema
            final_df = df_v2[['id', 'name', 'email']]
            print("✅ V2 Data Successfully Adapted:")
            print(final_df)
            
    except Exception as e:
        print(f"❌ V2 Failed: {e}")

if __name__ == "__main__":
    process_pipeline()
