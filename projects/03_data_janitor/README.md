# Week 4: Mini-Project 1 - The Data Janitor

**Goal**: Build a CLI tool that ingests raw, messy server logs (JSONL), cleans them, flattens nested structures, and saves them as an optimized Parquet file.

## Scenario
You are a Data Engineer at a startup. The backend team dumps raw logs into a folder every hour. Your job is to write a script that can process these logs so the Data Analysts can query them.

## Structure
- `data/raw/`: Where the messy logs live.
- `data/processed/`: Where your clean Parquet files go.
- `generate_logs.py`: Simulates the backend dumping logs.
- `janitor.py`: **Your CLI tool**.

## Instructions

### 1. Setup
Activate your environment:
```bash
cd ../03_data_janitor
source ../00_setup_and_refresher/venv/bin/activate
```

### 2. Generate Data
Simulate the log dump:
```bash
python generate_logs.py
```
Check `data/raw/` to see the files.

### 3. Run the Janitor
Run your tool to clean the data:
```bash
python janitor.py
```
This will:
1. Read all `*.jsonl` files in `data/raw/`.
2. Drop rows with missing timestamps.
3. Lowercase the actions.
4. **Flatten** the nested `metadata` JSON object into separate columns (`ip`, `user_agent`).
5. Save the result to `data/processed/cleaned_logs.parquet`.

### 4. Verify
You can verify the output by quickly inspecting it with python:
```bash
python -c "import pandas as pd; print(pd.read_parquet('data/processed/cleaned_logs.parquet').head())"
```

## Homework / Extensions
1. Modify `janitor.py` to accept a command line argument `--filter-bot` that removes rows where `user_agent` contains "Bot".
2. Add a check to ensure `janitor.py` doesn't crash if `data/processed` doesn't exist (create it automatically).
