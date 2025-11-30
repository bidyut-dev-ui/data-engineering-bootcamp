# Week 3: Advanced Pandas & NumPy

**Goal**: Learn how to handle "Big Data" on a small laptop (8GB RAM).

## Concepts Covered
1. **Memory Management**: Understanding how Pandas uses memory.
2. **Dtypes**: Using `int32`, `float32`, and `category` to reduce footprint by 50-90%.
3. **Chunking**: Processing files larger than your RAM using `chunksize`.

## Instructions

### 1. Setup
Activate your environment:
```bash
cd ../02_advanced_pandas
source ../00_setup_and_refresher/venv/bin/activate
```

### 2. Generate Large Data
We need a bigger file to see the impact. This script generates ~1 Million rows (~200MB CSV).
```bash
python generate_large_data.py
```

### 3. Run Tutorial 1: Memory Optimization
See how changing data types can drastically reduce memory usage.
```bash
python 01_memory_optimization.py
```
*Pay attention to the "Total Savings" percentage!*

### 4. Run Tutorial 2: Chunking
Learn how to compute sums/aggregates on a file without loading the whole thing.
```bash
python 02_chunking.py
```

## Homework / Challenge
Create `03_challenge.py`:
1. Use `read_csv` with `chunksize` to find the **Total Quantity** sold for the category **'Electronics'**.
2. You must NOT load the entire file into memory. Filter inside the loop.
