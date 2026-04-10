#!/bin/bash
# Setup script for Advanced PySpark Module
# Optimized for 8GB RAM, Windows 11 + WSL2 Ubuntu 22
# Intel i5 CPU, 477 GB SSD

set -e  # Exit on error

echo "========================================="
echo "Advanced PySpark Module Setup"
echo "Optimized for 8GB RAM Laptop"
echo "========================================="

# Check if running in WSL
if grep -q Microsoft /proc/version; then
    echo "✓ Running in WSL2"
else
    echo "⚠ Not running in WSL2 - some optimizations may not apply"
fi

# Check system resources
echo -e "\n📊 System Resources Check:"
TOTAL_RAM=$(free -g | awk '/^Mem:/{print $2}')
echo "  Total RAM: ${TOTAL_RAM}GB"
if [ "$TOTAL_RAM" -lt 8 ]; then
    echo "  ⚠ Warning: Less than 8GB RAM detected. Adjust Spark memory settings."
fi

# Update package list
echo -e "\n🔄 Updating package list..."
sudo apt-get update -qq

# Install Python and pip if not present
echo -e "\n🐍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "  Installing Python 3.10+..."
    sudo apt-get install -y python3 python3-pip python3-venv
fi

# Create virtual environment
echo -e "\n🏗️ Creating Python virtual environment..."
python3 -m venv venv_advanced_pyspark
source venv_advanced_pyspark/bin/activate

echo -e "\n📦 Installing PySpark and dependencies..."
echo "  This may take 5-10 minutes on 8GB RAM system..."

# Install PySpark first (largest package)
pip install --no-cache-dir pyspark==3.5.0

# Install other dependencies from requirements.txt
if [ -f "requirements.txt" ]; then
    pip install --no-cache-dir -r requirements.txt
else
    echo "  requirements.txt not found, installing core dependencies..."
    pip install --no-cache-dir \
        pyarrow>=14.0.0 \
        findspark>=2.0.0 \
        pandas>=2.0.0 \
        numpy>=1.24.0 \
        scikit-learn>=1.3.0 \
        fastapi>=0.104.0 \
        uvicorn[standard]>=0.24.0 \
        pydantic>=2.5.0 \
        kafka-python>=2.0.0 \
        python-dotenv>=1.0.0 \
        tqdm>=4.66.0 \
        pytest>=7.4.0
fi

# Create optimized Spark configuration for 8GB RAM
echo -e "\n⚙️ Creating optimized Spark configuration for 8GB RAM..."
cat > spark_8gb_config.conf << 'EOF'
# Spark Configuration for 8GB RAM Laptop
# Optimized for Intel i5, WSL2 Ubuntu 22

# Memory Settings (2GB for driver, 1GB per executor)
spark.driver.memory=2g
spark.executor.memory=1g
spark.memory.fraction=0.6
spark.memory.storageFraction=0.5

# Parallelism and Cores
spark.default.parallelism=4
spark.sql.shuffle.partitions=4
spark.cores.max=2

# Serialization and Compression
spark.serializer=org.apache.spark.serializer.KryoSerializer
spark.kryoserializer.buffer.max=256m
spark.sql.parquet.compression.codec=snappy
spark.rdd.compress=true

# Adaptive Query Execution
spark.sql.adaptive.enabled=true
spark.sql.adaptive.coalescePartitions.enabled=true
spark.sql.adaptive.skewJoin.enabled=true
spark.sql.adaptive.localShuffleReader.enabled=true

# Dynamic Allocation (disabled for local)
spark.dynamicAllocation.enabled=false

# Logging
spark.eventLog.enabled=true
spark.eventLog.dir=/tmp/spark-events
spark.history.fs.logDirectory=/tmp/spark-events

# WSL2 Specific Optimizations
spark.local.dir=/tmp/spark-local
spark.sql.warehouse.dir=/tmp/spark-warehouse

# Garbage Collection (G1GC for better memory management)
spark.executor.extraJavaOptions=-XX:+UseG1GC -XX:InitiatingHeapOccupancyPercent=35 -XX:ConcGCThreads=4
spark.driver.extraJavaOptions=-XX:+UseG1GC -XX:InitiatingHeapOccupancyPercent=35
EOF

echo "  Created spark_8gb_config.conf"

# Create test script to verify installation
echo -e "\n🧪 Creating verification script..."
cat > test_installation.py << 'EOF'
#!/usr/bin/env python3
"""
Test script to verify PySpark advanced module installation.
Runs basic operations to ensure everything works on 8GB RAM.
"""

import sys
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import pandas as pd
import numpy as np

def test_spark_session():
    """Test creating a SparkSession with 8GB RAM optimization."""
    print("Testing SparkSession creation with 8GB RAM optimization...")
    
    try:
        spark = SparkSession.builder \
            .appName("AdvancedPySparkTest") \
            .master("local[2]") \
            .config("spark.driver.memory", "2g") \
            .config("spark.executor.memory", "1g") \
            .config("spark.sql.shuffle.partitions", "4") \
            .getOrCreate()
        
        print(f"✓ SparkSession created successfully")
        print(f"  Spark version: {spark.version}")
        print(f"  Master URL: {spark.sparkContext.master}")
        
        # Test basic DataFrame operations
        print("\nTesting DataFrame operations...")
        data = [("Alice", 34), ("Bob", 45), ("Catherine", 29)]
        df = spark.createDataFrame(data, ["Name", "Age"])
        
        print(f"✓ DataFrame created with {df.count()} rows")
        
        # Test aggregation
        avg_age = df.agg({"Age": "avg"}).collect()[0][0]
        print(f"✓ Average age calculated: {avg_age:.1f}")
        
        # Test SQL
        df.createOrReplaceTempView("people")
        sql_result = spark.sql("SELECT COUNT(*) as count FROM people").collect()[0][0]
        print(f"✓ SQL query executed: {sql_result} rows")
        
        spark.stop()
        print("\n✅ All Spark tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Spark test failed: {e}")
        return False

def test_dependencies():
    """Test that all required dependencies are installed."""
    print("\nTesting Python dependencies...")
    
    dependencies = {
        'pyspark': '3.5.0',
        'pandas': '2.0.0',
        'numpy': '1.24.0',
        'scikit-learn': '1.3.0',
        'pyarrow': '14.0.0'
    }
    
    all_passed = True
    for package, min_version in dependencies.items():
        try:
            module = __import__(package)
            version = getattr(module, '__version__', 'unknown')
            print(f"  ✓ {package}: {version}")
        except ImportError:
            print(f"  ❌ {package}: NOT INSTALLED")
            all_passed = False
    
    return all_passed

def test_memory_optimization():
    """Test memory-efficient operations."""
    print("\nTesting memory optimization techniques...")
    
    try:
        # Create a larger dataset to test memory management
        spark = SparkSession.builder \
            .appName("MemoryTest") \
            .master("local[2]") \
            .config("spark.driver.memory", "2g") \
            .config("spark.executor.memory", "1g") \
            .getOrCreate()
        
        # Generate sample data
        pandas_df = pd.DataFrame({
            'id': range(10000),
            'value': np.random.randn(10000)
        })
        
        # Convert to Spark DataFrame (tests memory)
        spark_df = spark.createDataFrame(pandas_df)
        
        # Test memory-efficient operations
        result = spark_df.selectExpr(
            "COUNT(*) as count",
            "AVG(value) as avg_value",
            "STDDEV(value) as std_value"
        ).collect()[0]
        
        print(f"✓ Processed {result['count']:,} rows")
        print(f"✓ Memory-efficient operations completed")
        
        spark.stop()
        return True
        
    except Exception as e:
        print(f"❌ Memory optimization test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Advanced PySpark Installation Test")
    print("Optimized for 8GB RAM Laptop")
    print("=" * 60)
    
    tests = [
        ("Spark Session", test_spark_session),
        ("Dependencies", test_dependencies),
        ("Memory Optimization", test_memory_optimization)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} test...")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! Advanced PySpark is ready for use.")
        print("\nNext steps:")
        print("1. Generate sample data: python generate_advanced_data.py")
        print("2. Run tutorial 1: python 01_catalyst_optimizer.py")
        print("3. Check memory usage with: python 02_memory_management.py")
    else:
        print("⚠ Some tests failed. Check the errors above.")
        sys.exit(1)
    
    print("=" * 60)

if __name__ == "__main__":
    main()
EOF

chmod +x test_installation.py

# Create a quick start guide
echo -e "\n📝 Creating quick start guide..."
cat > QUICK_START.md << 'EOF'
# Quick Start: Advanced PySpark on 8GB RAM Laptop

## System Configuration
- **RAM**: 8GB total (2GB driver, 1GB executor)
- **CPU**: Intel i5 (2 cores for local execution)
- **OS**: Windows 11 + WSL2 Ubuntu 22
- **Storage**: 477 GB SSD
- **Time**: Optimized for 8 hours/day learning

## Setup Complete!

Your environment is now configured with:

### ✅ Installed Packages
- PySpark 3.5.0 with Catalyst Optimizer
- Memory-optimized configurations for 8GB RAM
- ML libraries (scikit-learn, pandas, numpy)
- Streaming support (kafka-python)
- API integration (FastAPI, Pydantic)

### 📁 Project Structure
```
projects/03_pyspark_advanced/
├── 01_catalyst_optimizer.py      # Query optimization
├── 02_memory_management.py       # Memory tuning
├── 03_join_strategies.py         # Join algorithms
├── 04_ml_pipeline.py            # MLlib pipelines
├── 05_streaming_analytics.py    # Structured streaming
├── 06_fastapi_integration.py    # REST API integration
├── generate_advanced_data.py    # Data generation
├── setup_advanced_pyspark.sh    # This setup script
├── test_installation.py         # Verification
└── spark_8gb_config.conf        # Optimized config
```

## 🚀 Getting Started

### 1. Activate Virtual Environment
```bash
source venv_advanced_pyspark/bin/activate
```

### 2. Test Installation
```bash
python test_installation.py
```

### 3. Generate Sample Data
```bash
python generate_advanced_data.py
```
This creates:
- 500K transaction records
- 20K customer records with skew
- 100K ML training samples
- Streaming data files
- API test data

### 4. Run Tutorials in Order
```bash
# Start with Catalyst Optimizer
python 01_catalyst_optimizer.py

# Then memory management
python 02_memory_management.py

# Continue through all 6 tutorials
```

## ⚙️ Memory Optimization Tips for 8GB RAM

### Spark Configuration
- Driver memory: 2GB (spark.driver.memory=2g)
- Executor memory: 1GB (spark.executor.memory=1g)
- Partitions: 4 (spark.sql.shuffle.partitions=4)
- Cores: 2 (spark.cores.max=2)

### WSL2 Specific
- Store data in `/tmp/` for faster I/O
- Monitor memory with `htop` or `free -h`
- Restart WSL if memory gets fragmented

### Performance Monitoring
```bash
# Monitor Spark UI (port 4040)
# Monitor memory usage
watch -n 1 free -h

# Check disk I/O
iostat -x 1
```

## 🐛 Troubleshooting

### Out of Memory Errors
1. Reduce dataset size in tutorials
2. Increase `spark.memory.fraction` to 0.8
3. Use `df.persist(StorageLevel.MEMORY_AND_DISK)` for large DataFrames

### Slow Performance
1. Check CPU usage with `top`
2. Ensure data is partitioned correctly
3. Use `.coalesce()` instead of `.repartition()` for reducing partitions

### WSL2 Issues
1. Restart WSL: `wsl --shutdown`
2. Increase WSL2 memory limit in `.wslconfig`
3. Store project files in WSL filesystem, not Windows mount

## 📈 Learning Path (6 Months, 8 Hours/Day)

### Month 1-2: Core Optimization
- Catalyst optimizer internals
- Memory management techniques
- Join strategy optimization

### Month 3-4: Advanced Features
- ML pipeline development
- Structured streaming
- Performance tuning

### Month 5-6: Integration & Production
- API integration with FastAPI
- Production deployment patterns
- Interview preparation

## 🆘 Need Help?

1. Check Spark UI at http://localhost:4040
2. Review configuration in `spark_8gb_config.conf`
3. Run verification: `python test_installation.py`
4. Consult `scope.md` for detailed roadmap

## 🎯 Success Metrics
- All 6 tutorials run without OOM errors
- Data processing completes within expected time
- Memory usage stays under 7GB peak
- All tests pass in verification script

Happy learning! 🚀
EOF

echo -e "\n✅ Setup complete!"
echo -e "\n📋 Next steps:"
echo "1. Activate virtual environment: source venv_advanced_pyspark/bin/activate"
echo "2. Test installation: python test_installation.py"
echo "3. Generate data: python generate_advanced_data.py"
echo "4. Start with tutorial: python 01_catalyst_optimizer.py"
echo -e "\n📖 See QUICK_START.md for detailed instructions"
echo "========================================="