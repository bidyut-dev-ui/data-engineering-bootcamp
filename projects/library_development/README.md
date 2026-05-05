# Library Development & Packaging

## Learning Objectives
- Create Python packages with setuptools and poetry
- Publish packages to PyPI
- Design clean, maintainable APIs
- Generate comprehensive documentation
- Implement testing strategies for libraries
- Manage versioning and backward compatibility

## Project Structure
```
projects/library_development/
├── README.md (this file)
├── requirements.txt
├── example_library/ - Complete example library
│   ├── pyproject.toml - Modern package configuration
│   ├── setup.py - Legacy setup configuration
│   ├── README.md - Library documentation
│   ├── LICENSE - License file
│   ├── src/
│   │   └── example_lib/
│   │       ├── __init__.py - Package initialization
│   │       ├── core.py - Core library functionality
│   │       ├── utils.py - Utility functions
│   │       └── exceptions.py - Custom exceptions
│   ├── tests/
│   │   ├── test_core.py - Unit tests for core functionality
│   │   └── test_utils.py - Unit tests for utilities
│   └── docs/
│       ├── index.md - Documentation homepage
│       ├── api.md - API reference
│       └── examples.md - Usage examples
├── 01_packaging_basics.py - Packaging fundamentals tutorial
├── 02_api_design.py - API design principles tutorial
├── 03_documentation.py - Documentation generation tutorial
├── 04_testing_strategies.py - Testing strategies tutorial
├── 05_versioning.py - Versioning and compatibility tutorial
├── 06_ci_cd.py - CI/CD pipeline tutorial
├── practice_exercises.py - Hands-on exercises
├── GOTCHAS_BEST_PRACTICES.md - Common pitfalls and best practices
└── INTERVIEW_QUESTIONS.md - Interview questions for library development
```

## Key Topics Covered

### 1. Packaging Fundamentals
- setuptools vs poetry vs flit
- pyproject.toml configuration
- Wheel and source distribution building
- Dependency management
- Entry points and console scripts

### 2. API Design Principles
- Public vs private API boundaries
- Function and class design patterns
- Error handling and exception design
- Configuration and customization
- Backward compatibility strategies

### 3. Documentation Generation
- Sphinx and MkDocs setup
- Docstring conventions (Google, NumPy, reStructuredText)
- API reference generation
- Tutorial and example creation
- ReadTheDocs deployment

### 4. Testing Strategies
- Unit testing with pytest
- Mocking and patching
- Integration testing
- Test coverage analysis
- Property-based testing

### 5. Versioning & Compatibility
- Semantic versioning (SemVer)
- Backward compatibility testing
- Deprecation strategies
- Migration guides
- Version pinning

### 6. CI/CD Pipelines
- GitHub Actions for Python packages
- Automated testing and linting
- Documentation deployment
- PyPI publishing automation
- Release management

## Prerequisites
- Intermediate Python programming skills
- Basic understanding of virtual environments
- Familiarity with Git and GitHub
- Experience with command-line tools
- Completion of Python fundamentals (00_5_python_fundamentals)

## Getting Started

### 1. Setup Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt

# Install example library in development mode
cd example_library
pip install -e .
```

### 2. Run Tutorials
Start with the tutorials in numerical order:
```bash
# Packaging basics
python 01_packaging_basics.py

# API design
python 02_api_design.py

# Documentation
python 03_documentation.py

# Testing strategies
python 04_testing_strategies.py

# Versioning
python 05_versioning.py

# CI/CD
python 06_ci_cd.py
```

### 3. Explore Example Library
```bash
cd example_library

# Build the package
python -m build

# Run tests
pytest tests/

# Generate documentation
cd docs
make html  # or mkdocs build
```

### 4. Practice Exercises
After completing each tutorial, work through the corresponding exercises in `practice_exercises.py`.

### 5. Review Best Practices
Read `GOTCHAS_BEST_PRACTICES.md` to understand common pitfalls and how to avoid them.

### 6. Prepare for Interviews
Study `INTERVIEW_QUESTIONS.md` to prepare for technical interviews on library development.

## Real-World Applications

### Reusable Utility Libraries
- Data validation and transformation libraries
- Configuration management utilities
- Logging and monitoring helpers
- API client SDKs

### Framework Extensions
- Django/Flask/FastAPI plugins
- Database adapter libraries
- Authentication and authorization modules
- Template engine extensions

### Open-Source Projects
- Community-maintained packages
- Tooling for specific domains (data science, web dev, etc.)
- Educational and demonstration libraries
- Integration libraries between systems

### Internal Company Libraries
- Shared code across multiple projects
- Standardized configuration and setup
- Common business logic encapsulation
- Development tooling and automation

## Integration with Other Projects

### Advanced Python Projects
- Package advanced patterns as reusable libraries
- Create decorator and descriptor libraries
- Build async utility packages

### API Development Projects
- Create client SDKs for GraphQL/WebSocket APIs
- Build authentication and rate limiting libraries
- Develop API testing utilities

### Data Engineering Projects
- Create data validation and transformation libraries
- Build connector libraries for databases and APIs
- Develop monitoring and logging utilities

## Expected Learning Outcomes

By completing this project, you will be able to:

1. **Design and implement** Python packages with proper structure
2. **Create clean, maintainable APIs** with good documentation
3. **Set up comprehensive testing** for library code
4. **Manage versioning and dependencies** effectively
5. **Automate packaging and deployment** with CI/CD
6. **Publish packages to PyPI** and other repositories
7. **Maintain backward compatibility** across releases

## Assessment

### Self-Assessment Checklist
- [ ] Can create a Python package with proper structure
- [ ] Can write comprehensive documentation with examples
- [ ] Can implement unit tests with good coverage
- [ ] Can manage semantic versioning correctly
- [ ] Can set up CI/CD pipeline for a package
- [ ] Can publish a package to PyPI (test instance)
- [ ] Can design APIs with backward compatibility in mind

### Code Review Points
- Proper package structure and organization
- Clear API design and documentation
- Comprehensive test coverage
- Proper dependency management
- Versioning and changelog maintenance
- CI/CD pipeline configuration

## Next Steps

After completing this project, proceed to:
1. **Contribute to open-source projects** to gain real-world experience
2. **Create your own utility libraries** for common tasks
3. **Explore specialized packaging** (C extensions, binary wheels)
4. **Learn about monorepo tooling** (poetry, pdm, hatch)

## Resources

### Official Documentation
- [Python Packaging User Guide](https://packaging.python.org/)
- [setuptools Documentation](https://setuptools.pypa.io/)
- [poetry Documentation](https://python-poetry.org/docs/)
- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [pytest Documentation](https://docs.pytest.org/)

### Recommended Books
- "Python Packaging" by various authors
- "The Hitchhiker's Guide to Python" by Kenneth Reitz and Tanya Schlusser
- "Python Testing with pytest" by Brian Okken
- "Fluent Python" by Luciano Ramalho

### Online Courses
- "Python Packaging" on Real Python
- "Building Python Packages" on Pluralsight
- "Open Source Software Development" on Coursera

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Check PYTHONPATH and sys.path
   - Verify package structure and __init__.py files
   - Ensure package is installed in development mode

2. **Dependency Conflicts**
   - Use virtual environments
   - Pin dependency versions
   - Use dependency resolution tools (poetry, pip-tools)

3. **Documentation Build Failures**
   - Check Sphinx/MkDocs configuration
   - Verify docstring formatting
   - Check for missing imports in documentation

4. **Test Failures**
   - Check test environment setup
   - Verify mocking and patching
   - Check for side effects between tests

5. **PyPI Upload Issues**
   - Verify package name availability
   - Check authentication tokens
   - Test with TestPyPI first

### Getting Help
- Check the `GOTCHAS_BEST_PRACTICES.md` file
- Review example library implementation
- Search for specific error messages in packaging documentation
- Ask in the course discussion forum
- Consult Python packaging community (Discord, Reddit, Stack Overflow)