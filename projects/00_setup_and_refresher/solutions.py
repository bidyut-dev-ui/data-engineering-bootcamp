"""
Solutions for Setup & Refresher Practice Exercises

This file contains example implementations for the practice exercises.
These are reference solutions - there are often multiple correct approaches.
"""

import sys
import platform
import shutil
import subprocess
import os
import psutil

def exercise_1_check_python_version():
    """
    Exercise 1: Check Python Version and Environment
    """
    print("Checking Python version...")
    
    # Get version info
    version_info = sys.version_info
    version_str = sys.version.split()[0]  # Just the version number
    
    # Check if Python 3.10+
    is_sufficient = version_info >= (3, 10)
    
    if is_sufficient:
        print(f"✅ Python {version_str} is sufficient (3.10+ required)")
    else:
        print(f"❌ Python {version_str} is insufficient (3.10+ required)")
    
    # Additional details
    print(f"  Platform: {platform.platform()}")
    print(f"  Implementation: {platform.python_implementation()}")
    print(f"  Executable: {sys.executable}")
    
    return is_sufficient

def exercise_2_verify_tools_installed():
    """
    Exercise 2: Verify Required Tools
    """
    print("Verifying required tools...")
    
    # Essential tools for data engineering
    essential_tools = ["git", "docker", "python3", "pip3"]
    optional_tools = ["docker-compose", "code", "curl", "wget"]
    
    results = {}
    
    # Check essential tools
    print("\nEssential Tools:")
    for tool in essential_tools:
        path = shutil.which(tool)
        is_available = path is not None
        results[tool] = is_available
        
        status = "✅" if is_available else "❌"
        print(f"  {status} {tool}: {path or 'Not found'}")
    
    # Check optional tools
    print("\nOptional Tools:")
    for tool in optional_tools:
        path = shutil.which(tool)
        is_available = path is not None
        results[tool] = is_available
        
        status = "✓" if is_available else "○"
        print(f"  {status} {tool}: {path or 'Not found'}")
    
    # Check if all essential tools are available
    all_essential = all(results[tool] for tool in essential_tools)
    
    if all_essential:
        print("\n✅ All essential tools are available!")
    else:
        missing = [tool for tool in essential_tools if not results[tool]]
        print(f"\n❌ Missing essential tools: {', '.join(missing)}")
    
    return results

def exercise_3_create_virtual_environment():
    """
    Exercise 3: Virtual Environment Setup
    """
    print("Setting up virtual environment...")
    
    venv_dir = "venv"
    venv_path = os.path.join(os.getcwd(), venv_dir)
    
    # Check if virtual environment already exists
    if os.path.exists(venv_dir):
        print(f"✅ Virtual environment already exists at: {venv_path}")
        
        # Check if it's a valid virtual environment
        if os.path.exists(os.path.join(venv_dir, "pyvenv.cfg")):
            print("  Valid virtual environment detected")
        else:
            print("  Warning: Directory exists but may not be a valid virtual environment")
        
        return venv_path
    
    # Create new virtual environment
    print(f"Creating new virtual environment at: {venv_path}")
    
    try:
        # Use subprocess to create virtual environment
        result = subprocess.run(
            [sys.executable, "-m", "venv", venv_dir],
            capture_output=True,
            text=True,
            check=True
        )
        
        print("✅ Virtual environment created successfully")
        
        # Verify creation
        if os.path.exists(os.path.join(venv_dir, "pyvenv.cfg")):
            print("  Verification: pyvenv.cfg found")
        
        # Show activation instructions
        print("\nTo activate:")
        if platform.system() in ["Linux", "Darwin"]:  # Linux or Mac
            print(f"  source {venv_dir}/bin/activate")
        else:  # Windows
            print(f"  {venv_dir}\\Scripts\\activate")
        
        return venv_path
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        print(f"  Error output: {e.stderr}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def exercise_4_check_disk_space():
    """
    Exercise 4: Disk Space Check for Data Engineering
    """
    print("Checking disk space...")
    
    try:
        # Get disk usage for current directory
        total, used, free = shutil.disk_usage(".")
        
        # Convert to GB
        total_gb = total / (1024**3)
        used_gb = used / (1024**3)
        free_gb = free / (1024**3)
        
        print(f"  Total: {total_gb:.1f} GB")
        print(f"  Used: {used_gb:.1f} GB ({used/total*100:.1f}%)")
        print(f"  Free: {free_gb:.1f} GB ({free/total*100:.1f}%)")
        
        # Check if we have minimum required space
        min_required_gb = 5  # 5GB minimum for data engineering
        has_sufficient_space = free_gb >= min_required_gb
        
        if has_sufficient_space:
            print(f"✅ Sufficient disk space available ({free_gb:.1f} GB free)")
        else:
            print(f"❌ Insufficient disk space ({free_gb:.1f} GB free, {min_required_gb} GB required)")
            print("  Consider:")
            print("  - Cleaning up temporary files")
            print("  - Moving data to external storage")
            print("  - Increasing disk space")
        
        return free_gb
        
    except Exception as e:
        print(f"❌ Error checking disk space: {e}")
        return None

def exercise_5_memory_check():
    """
    Exercise 5: Memory Availability Check
    """
    print("Checking system memory...")
    
    try:
        # Get memory information
        memory = psutil.virtual_memory()
        
        # Convert to GB
        total_gb = memory.total / (1024**3)
        available_gb = memory.available / (1024**3)
        used_gb = memory.used / (1024**3)
        percent_used = memory.percent
        
        print(f"  Total RAM: {total_gb:.1f} GB")
        print(f"  Available: {available_gb:.1f} GB")
        print(f"  Used: {used_gb:.1f} GB ({percent_used:.1f}%)")
        
        # Check if we have minimum required memory
        min_required_gb = 8  # 8GB minimum for data engineering
        has_sufficient_memory = total_gb >= min_required_gb
        
        if has_sufficient_memory:
            print(f"✅ Sufficient RAM available ({total_gb:.1f} GB total)")
        else:
            print(f"⚠️  Limited RAM available ({total_gb:.1f} GB total, {min_required_gb} GB recommended)")
        
        # Recommendations for 8GB RAM systems
        print("\nRecommendations for 8GB RAM systems:")
        print("  1. Use chunking for large datasets")
        print("  2. Set memory limits for Docker containers")
        print("  3. Monitor memory usage during processing")
        print("  4. Consider adding swap space if needed")
        
        # Check swap space
        swap = psutil.swap_memory()
        if swap.total > 0:
            swap_gb = swap.total / (1024**3)
            print(f"\n  Swap space: {swap_gb:.1f} GB available")
        else:
            print("\n  ⚠️  No swap space configured")
            print("    Consider adding swap for memory-intensive tasks")
        
        return {
            'total_gb': total_gb,
            'available_gb': available_gb,
            'percent_used': percent_used,
            'has_sufficient_memory': has_sufficient_memory
        }
        
    except ImportError:
        print("❌ psutil not installed. Install with: pip install psutil")
        return None
    except Exception as e:
        print(f"❌ Error checking memory: {e}")
        return None

def exercise_6_setup_optimization():
    """
    Exercise 6: Environment Optimization for 8GB RAM
    """
    print("Generating optimization recommendations...")
    
    recommendations = []
    
    # 1. Python memory settings
    recommendations.append({
        'category': 'Python Memory',
        'recommendations': [
            "Set PYTHONMALLOC=malloc to use system malloc",
            "Set MALLOC_ARENA_MAX=2 to reduce memory fragmentation",
            "Set OMP_NUM_THREADS=2 to limit parallel threads",
            "Use gc.collect() after large operations",
            "Delete unused variables with del statement"
        ]
    })
    
    # 2. Pandas optimizations
    recommendations.append({
        'category': 'Pandas Optimization',
        'recommendations': [
            "Use dtype parameter to specify column types",
            "Use category dtype for string columns with few unique values",
            "Process large files in chunks with chunksize parameter",
            "Load only needed columns with usecols parameter",
            "Use read_csv(..., low_memory=False) for mixed types"
        ]
    })
    
    # 3. Docker optimizations
    recommendations.append({
        'category': 'Docker Optimization',
        'recommendations': [
            "Set memory limits in docker-compose.yml",
            "Use .dockerignore to exclude unnecessary files",
            "Use multi-stage builds to reduce image size",
            "Set appropriate CPU limits",
            "Use volume mounts for large datasets"
        ]
    })
    
    # 4. System optimizations
    recommendations.append({
        'category': 'System Optimization',
        'recommendations': [
            "Add swap space if not already configured",
            "Close unnecessary applications during data processing",
            "Monitor memory usage with top/htop",
            "Consider using tmpfs for temporary files",
            "Schedule memory-intensive tasks during off-hours"
        ]
    })
    
    # Print recommendations
    for rec in recommendations:
        print(f"\n{rec['category']}:")
        for i, item in enumerate(rec['recommendations'], 1):
            print(f"  {i}. {item}")
    
    # Generate environment variables setup
    print("\nEnvironment variables to set:")
    env_vars = {
        'PYTHONMALLOC': 'malloc',
        'MALLOC_ARENA_MAX': '2',
        'OMP_NUM_THREADS': '2',
        'PYTHONUNBUFFERED': '1',
        'TF_CPP_MIN_LOG_LEVEL': '3'  # Reduce TensorFlow logging
    }
    
    for key, value in env_vars.items():
        print(f"  export {key}={value}")
    
    return recommendations

def exercise_7_troubleshoot_common_issues():
    """
    Exercise 7: Troubleshooting Common Setup Issues
    """
    print("Checking for common setup issues...")
    
    issues_found = []
    solutions_provided = []
    
    # Check 1: Docker running
    try:
        docker_path = shutil.which("docker")
        if docker_path:
            # Try to run a simple docker command
            result = subprocess.run(
                ["docker", "ps"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 0:
                issues_found.append("Docker is installed but not running")
                solutions_provided.append("Start Docker Desktop and ensure it's exposed to WSL2")
            else:
                print("✅ Docker is running correctly")
        else:
            issues_found.append("Docker not installed")
            solutions_provided.append("Install Docker Desktop and enable WSL2 integration")
    except Exception:
        issues_found.append("Docker check failed")
        solutions_provided.append("Check Docker installation and permissions")
    
    # Check 2: Virtual environment activated
    if "VIRTUAL_ENV" not in os.environ:
        issues_found.append("Virtual environment not activated")
        solutions_provided.append("Run: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)")
    else:
        print(f"✅ Virtual environment activated: {os.environ['VIRTUAL_ENV']}")
    
    # Check 3: Python path
    python_path = sys.executable
    if "venv" not in python_path and "VIRTUAL_ENV" in os.environ:
        issues_found.append("Python executable not from virtual environment")
        solutions_provided.append("Ensure virtual environment is properly activated")
    else:
        print(f"✅ Using Python from: {python_path}")
    
    # Check 4: Port conflicts (common ports)
    common_ports = [5432, 8080, 3000, 6379]
    for port in common_ports:
        try:
            # Try to bind to port to check if it's in use
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            
            if result == 0:  # Port is in use
                issues_found.append(f"Port {port} is already in use")
                solutions_provided.append(f"Change service port or stop process using port {port}")
        except Exception:
            pass
    
    # Check 5: Disk space
    try:
        total, used, free = shutil.disk_usage(".")
        free_gb = free / (1024**3)
        if free_gb < 5:
            issues_found.append(f"Low disk space ({free_gb:.1f} GB free)")
            solutions_provided.append("Free up disk space or add more storage")
        else:
            print(f"✅ Sufficient disk space: {free_gb:.1f} GB free")
    except Exception:
        pass
    
    # Report issues and solutions
    if issues_found:
        print("\n❌ Issues found:")
        for i, issue in enumerate(issues_found, 1):
            print(f"  {i}. {issue}")
            print(f"     Solution: {solutions_provided[i-1]}")
    else:
        print("\n✅ No common issues detected!")
    
    return {
        'issues': issues_found,
        'solutions': solutions_provided
    }

def run_all_exercises():
    """Run all exercises and display results"""
    print("=" * 60)
    print("SETUP & REFRESHER PRACTICE EXERCISES - SOLUTIONS")
    print("=" * 60)
    
    exercises = [
        ("1. Python Version Check", exercise_1_check_python_version),
        ("2. Tool Verification", exercise_2_verify_tools_installed),
        ("3. Virtual Environment Setup", exercise_3_create_virtual_environment),
        ("4. Disk Space Check", exercise_4_check_disk_space),
        ("5. Memory Check", exercise_5_memory_check),
        ("6. Environment Optimization", exercise_6_setup_optimization),
        ("7. Troubleshooting", exercise_7_troubleshoot_common_issues),
    ]
    
    all_results = {}
    
    for name, func in exercises:
        print(f"\n{name}:")
        print("-" * 40)
        try:
            result = func()
            all_results[name] = result
        except Exception as e:
            print(f"Error: {e}")
            all_results[name] = None
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    # Provide overall assessment
    print("\nBased on the checks, your environment is:")
    
    # Simple assessment logic
    issues_count = 0
    if all_results.get("1. Python Version Check") is False:
        issues_count += 1
        print("  ❌ Python version insufficient")
    
    tool_results = all_results.get("2. Tool Verification", {})
    if isinstance(tool_results, dict):
        essential_tools = ["git", "docker", "python3"]
        missing_tools = [t for t in essential_tools if not tool_results.get(t, False)]
        if missing_tools:
            issues_count += len(missing_tools)
            print(f"  ❌ Missing tools: {', '.join(missing_tools)}")
    
    if issues_count == 0:
        print("  ✅ Ready for data engineering tasks!")
    else:
        print(f"  ⚠️  {issues_count} issue(s) need attention")
    
    print("\nNext steps:")
    print("  1. Review any issues identified above")
    print("  2. Implement optimization recommendations")
    print("  3. Run the environment check: python check_env.py")
    print("  4. Proceed to Week 2: Pandas Basics")
    
    return all_results

if __name__ == "__main__":
    run_all_exercises()