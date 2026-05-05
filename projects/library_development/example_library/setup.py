#!/usr/bin/env python3
"""
Legacy setup.py configuration for example-lib.

This file is provided for compatibility with older build systems
and tools that don't support pyproject.toml yet.

Note: Modern Python packaging should use pyproject.toml instead.
This file is kept for educational purposes and backward compatibility.
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read version from pyproject.toml or version file
def get_version():
    """Extract version from pyproject.toml or version file."""
    try:
        # Try to read from pyproject.toml
        import tomli
        with open("pyproject.toml", "rb") as f:
            pyproject = tomli.load(f)
        return pyproject["project"]["version"]
    except (ImportError, KeyError, FileNotFoundError):
        # Fallback to version file
        version_file = os.path.join("src", "example_lib", "_version.py")
        if os.path.exists(version_file):
            with open(version_file, "r") as f:
                for line in f:
                    if line.startswith("__version__"):
                        return line.split("=")[1].strip().strip('"\'')
        return "0.1.0"

setup(
    name="example-lib",
    version=get_version(),
    author="Data Engineering Bootcamp",
    author_email="example@example.com",
    maintainer="Library Development Team",
    maintainer_email="maintainers@example.com",
    description="An example Python library demonstrating packaging best practices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/example/example-lib",
    project_urls={
        "Homepage": "https://github.com/example/example-lib",
        "Documentation": "https://example-lib.readthedocs.io/",
        "Repository": "https://github.com/example/example-lib",
        "Changelog": "https://github.com/example/example-lib/releases",
        "Issues": "https://github.com/example/example-lib/issues",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Education :: Testing",
    ],
    python_requires=">=3.8",
    install_requires=[
        "typing-extensions>=4.0.0; python_version<'3.11'",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "isort>=5.12.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.3.0",
            "myst-parser>=2.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "hypothesis>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "example-cli=example_lib.cli:main",
        ],
        "example_lib.plugins": [
            "calculator=example_lib.plugins:CalculatorPlugin",
            "validator=example_lib.plugins:ValidatorPlugin",
        ],
        "pytest11": [
            "example_lib=example_lib.pytest_plugin",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=["example", "library", "tutorial", "packaging"],
)


if __name__ == "__main__":
    # This allows running: python setup.py --version
    import sys
    if "--version" in sys.argv:
        print(get_version())
        sys.exit(0)