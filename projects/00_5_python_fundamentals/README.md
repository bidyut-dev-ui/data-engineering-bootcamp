# Week 0.5: Python Fundamentals for Complete Beginners

**Goal**: Learn Python from scratch - no prior programming experience required. This project teaches the absolute basics needed before diving into data engineering.

## 🎯 Learning Objectives

By the end of this week, you will be able to:
- Write and run basic Python scripts
- Understand Python data types and variables
- Use control flow (if/else, loops)
- Work with lists, dictionaries, and other data structures
- Define and call functions
- Handle basic file I/O operations
- Debug simple Python programs

## 🖥️ Hardware Constraints & Configuration

This project is designed for **8GB RAM laptops with zero GPU**:
- All code runs locally without external dependencies
- Minimal memory usage (basic Python operations)
- No Docker required for this project
- Uses standard Python 3.10+ libraries only

## 📁 Project Structure

```
00_5_python_fundamentals/
├── README.md                          # This file
├── requirements.txt                   # Dependencies (minimal)
├── 01_variables_and_types.py         # Variables, data types, operators
├── 02_control_flow.py                # if/elif/else, loops
├── 03_data_structures.py             # Lists, dictionaries, tuples, sets
├── 04_functions.py                   # Function definition, parameters, return
├── 05_file_io.py                     # Reading/writing files, with statement
├── 06_error_handling.py              # try/except/finally, exceptions
├── 07_modules_and_imports.py         # Importing modules, creating packages
├── 08_practice_exercises.py          # Hands-on exercises
├── GOTCHAS_BEST_PRACTICES.md         # Common mistakes and solutions
├── INTERVIEW_QUESTIONS.md            # Basic Python interview questions
└── solutions/                        # Solution files for exercises
    ├── 01_solution.py
    ├── 02_solution.py
    └── ...
```

## 🚀 Getting Started

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Tutorials in Order
```bash
# Start with the basics
python 01_variables_and_types.py

# Then move to control flow
python 02_control_flow.py

# Continue through all tutorials
```

## 📚 Tutorial Overview

### Tutorial 1: Variables and Data Types
- Variables and assignment
- Basic data types: int, float, str, bool
- Type conversion (int(), str(), float())
- Arithmetic and comparison operators
- String operations and formatting

### Tutorial 2: Control Flow
- Conditional statements (if, elif, else)
- Logical operators (and, or, not)
- For loops with range()
- While loops and break/continue
- Nested control structures

### Tutorial 3: Data Structures
- Lists: creation, indexing, slicing, methods
- Dictionaries: key-value pairs, methods
- Tuples: immutable sequences
- Sets: unique elements, set operations
- Choosing the right data structure

### Tutorial 4: Functions
- Defining functions with def
- Parameters and arguments
- Return values
- Default parameters
- Variable scope (local vs global)

### Tutorial 5: File I/O
- Reading files with open()
- Writing files
- The with statement (context managers)
- Working with CSV and JSON files
- File paths and directory operations

### Tutorial 6: Error Handling
- try/except blocks
- Handling specific exceptions
- finally clause for cleanup
- Raising exceptions with raise
- Creating custom exceptions

### Tutorial 7: Modules and Imports
- Importing standard library modules
- Creating your own modules
- Package structure
- Import aliases (import as)
- Relative vs absolute imports

### Tutorial 8: Practice Exercises
- 10 hands-on exercises covering all topics
- Real-world scenarios
- Gradual difficulty progression
- Solutions provided in solutions/ directory

## 🎯 Real-World Application

These fundamentals are essential for:
- **Data Engineering**: Understanding data types helps with schema design
- **Pandas**: Lists and dictionaries are the foundation of DataFrames
- **API Development**: Functions and error handling are critical for robust APIs
- **ETL Pipelines**: File I/O and control flow are used in every pipeline

## 📈 Expected Outcomes

After completing this project, you should be able to:
1. Write Python scripts to solve basic problems
2. Read and understand Python code written by others
3. Debug common Python errors
4. Prepare for the more advanced "Python Deep Dive for Pandas" (Week 1.5)
5. Feel confident tackling data engineering projects

## 🚨 Important Notes for Beginners

1. **Don't Skip Exercises**: Practice is essential for muscle memory
2. **Type Everything**: Don't copy-paste - typing helps learning
3. **Embrace Errors**: Errors are learning opportunities, not failures
4. **Ask Questions**: Use the GOTCHAS_BEST_PRACTICES.md when stuck
5. **Review Regularly**: Python basics need repetition to stick

## 🔗 Integration with Other Projects

This project prepares you for:
- **Week 1.5**: Python Deep Dive for Pandas (builds on these basics)
- **Week 2**: Pandas Basics (uses lists/dicts for DataFrames)
- **Week 3**: Advanced Pandas (requires solid Python foundation)

## 📚 Further Learning

- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Real Python](https://realpython.com/) - Excellent tutorials
- [Python for Everybody](https://www.py4e.com/) - Free course
- [Learn Python the Hard Way](https://learnpythonthehardway.org/) - Hands-on approach