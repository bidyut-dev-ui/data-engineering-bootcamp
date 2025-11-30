import pandas as pd

def main():
    print("=== Chunking Tutorial ===")
    print("Simulating processing a file larger than RAM...\n")
    
    file_path = 'large_sales.csv'
    chunk_size = 100_000 # Process 100k rows at a time
    
    total_sales = 0
    total_rows = 0
    
    # Create an iterator
    chunk_iterator = pd.read_csv(file_path, chunksize=chunk_size)
    
    print(f"Processing '{file_path}' in chunks of {chunk_size}...")
    
    for i, chunk in enumerate(chunk_iterator):
        # In each loop, 'chunk' is a DataFrame of size 100k
        
        # Perform aggregation on the chunk
        chunk_sales = (chunk['price'] * chunk['quantity']).sum()
        
        total_sales += chunk_sales
        total_rows += len(chunk)
        
        print(f"  Batch {i+1}: Processed {len(chunk)} rows. Partial Sales: ${chunk_sales:,.2f}")
        
    print("\n=== Final Results ===")
    print(f"Total Rows Processed: {total_rows}")
    print(f"Total Sales: ${total_sales:,.2f}")
    print("Success! We processed the file without loading it all at once.")

if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError:
        print("Error: 'large_sales.csv' not found. Run generate_large_data.py first!")
