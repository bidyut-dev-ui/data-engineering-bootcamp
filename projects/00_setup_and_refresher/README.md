# Week 1: Setup & Refresher

**Goal**: Verify your development environment is ready for Data Engineering tasks.

## Checklist
1. **WSL2 & Ubuntu**: Ensure you are running inside Ubuntu.
2. **Python 3.10+**: `python3 --version`
3. **Docker**: `docker --version` (Ensure Docker Desktop is running in Windows and exposed to WSL2).
4. **VS Code**: You are likely using this already.

## Task: Run the Environment Check

1. Open a terminal in this directory.
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install basic dependencies:
   ```bash
   pip install pandas
   ```
4. Run the check script:
   ```bash
   python check_env.py
   ```

## Expected Output
You should see `[OK]` for git, docker, and pandas.
