import argparse
import pandas as pd
import glob
import os
import sys

def process_file(file_path):
    """Reads a JSONL file, cleans it, and returns a DataFrame."""
    print(f"Processing {file_path}...")
    
    try:
        # Read JSONL
        df = pd.read_json(file_path, lines=True)
    except ValueError as e:
        print(f"Error reading {file_path}: {e}")
        return None

    # 1. Drop rows with missing timestamp
    initial_rows = len(df)
    df = df.dropna(subset=['timestamp'])
    
    # 2. Normalize 'action' to lowercase
    df['action'] = df['action'].str.lower()
    
    # 3. Flatten 'metadata' column (extract ip and user_agent)
    # This is a common DE task: flattening nested JSON
    if 'metadata' in df.columns:
        metadata_df = pd.json_normalize(df['metadata'])
        df = pd.concat([df.drop('metadata', axis=1), metadata_df], axis=1)
    
    # 4. Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    print(f"  - Cleaned {initial_rows} -> {len(df)} rows.")
    return df

def main():
    parser = argparse.ArgumentParser(description="The Data Janitor: Log Cleaner")
    parser.add_argument('--input', type=str, default='data/raw/*.jsonl', help='Input file pattern')
    parser.add_argument('--output', type=str, default='data/processed/cleaned_logs.parquet', help='Output file path')
    
    args = parser.parse_args()
    
    # Find all files matching the pattern
    files = glob.glob(args.input)
    if not files:
        print(f"No files found matching: {args.input}")
        sys.exit(1)
        
    print(f"Found {len(files)} files to process.")
    
    all_dfs = []
    
    for f in files:
        df = process_file(f)
        if df is not None:
            all_dfs.append(df)
            
    if not all_dfs:
        print("No data processed.")
        sys.exit(1)
        
    # Combine all chunks
    final_df = pd.concat(all_dfs, ignore_index=True)
    
    # Save to Parquet (efficient storage)
    print(f"Saving {len(final_df)} rows to {args.output}...")
    final_df.to_parquet(args.output)
    print("Done!")

if __name__ == "__main__":
    main()
