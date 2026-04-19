#!/usr/bin/env python3
"""
Tutorial 1: Hadoop Docker Setup for 8GB RAM

This tutorial demonstrates how to set up and run a single-node Hadoop cluster
in Docker with memory constraints suitable for 8GB RAM systems.

Learning Objectives:
1. Start Hadoop services using Docker Compose
2. Verify cluster health
3. Configure memory limits for Hadoop components
4. Access Hadoop web interfaces
"""

import subprocess
import time
import sys
import os
from pathlib import Path

def check_docker():
    """Check if Docker is running."""
    print("🔍 Checking Docker installation...")
    try:
        result = subprocess.run(["docker", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker installed: {result.stdout.strip()}")
            return True
        else:
            print("❌ Docker not found or not running")
            return False
    except FileNotFoundError:
        print("❌ Docker command not found. Please install Docker first.")
        return False

def check_docker_compose():
    """Check if Docker Compose is available."""
    print("🔍 Checking Docker Compose...")
    try:
        result = subprocess.run(["docker-compose", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker Compose installed: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        # Try docker compose (v2)
        try:
            result = subprocess.run(["docker", "compose", "version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Docker Compose (v2) installed")
                return True
        except:
            pass
    
    print("❌ Docker Compose not found")
    return False

def start_hadoop_cluster():
    """Start Hadoop cluster using docker-compose."""
    print("\n🚀 Starting Hadoop cluster...")
    
    # Get the directory containing docker-compose.yml
    script_dir = Path(__file__).parent
    compose_file = script_dir / "docker-compose.yml"
    
    if not compose_file.exists():
        print(f"❌ docker-compose.yml not found at {compose_file}")
        return False
    
    print(f"📁 Using compose file: {compose_file}")
    
    # Start services in detached mode
    print("⏳ Starting services (this may take a few minutes)...")
    try:
        result = subprocess.run(
            ["docker-compose", "-f", str(compose_file), "up", "-d"],
            capture_output=True,
            text=True,
            cwd=script_dir
        )
        
        if result.returncode == 0:
            print("✅ Hadoop cluster started successfully")
            return True
        else:
            print(f"❌ Failed to start cluster: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error starting cluster: {e}")
        return False

def check_cluster_health():
    """Check if Hadoop services are running."""
    print("\n🏥 Checking cluster health...")
    
    # Check running containers
    print("📦 Checking running containers...")
    result = subprocess.run(
        ["docker", "ps", "--format", "table {{.Names}}\t{{.Status}}\t{{.Ports}}"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(result.stdout)
        
        # Count Hadoop-related containers
        hadoop_containers = [
            "namenode", "datanode", "resourcemanager", 
            "nodemanager", "historyserver", "hive-server", "hive-metastore"
        ]
        
        running_containers = []
        for container in hadoop_containers:
            check = subprocess.run(
                ["docker", "ps", "--filter", f"name={container}", "--format", "{{.Names}}"],
                capture_output=True,
                text=True
            )
            if check.stdout.strip():
                running_containers.append(container)
        
        print(f"\n📊 Running: {len(running_containers)}/{len(hadoop_containers)} Hadoop services")
        if running_containers:
            print(f"   ✅ {', '.join(running_containers)}")
        
        missing = set(hadoop_containers) - set(running_containers)
        if missing:
            print(f"   ⚠️  Missing: {', '.join(missing)}")
            print("   Some services may still be starting. Wait 1-2 minutes and check again.")
        
        return len(running_containers) >= 4  # At least core services
    else:
        print("❌ Failed to check containers")
        return False

def show_web_interfaces():
    """Display URLs for Hadoop web interfaces."""
    print("\n🌐 Hadoop Web Interfaces:")
    print("   Note: These may take 1-2 minutes to become accessible after startup")
    print("   ──────────────────────────────────────────")
    print("   📊 HDFS NameNode:    http://localhost:9870")
    print("   ⚙️  YARN ResourceManager: http://localhost:8088")
    print("   📈 Job History:      http://localhost:8188")
    print("   🐝 Hive Server:      http://localhost:10002")
    print("   ──────────────────────────────────────────")
    print("   💡 Tip: Use 'docker-compose logs <service>' to check logs")

def check_hdfs():
    """Check HDFS accessibility."""
    print("\n📁 Checking HDFS...")
    
    # Try to execute a simple HDFS command in the namenode container
    try:
        result = subprocess.run(
            ["docker", "exec", "namenode", "hdfs", "dfs", "-ls", "/"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✅ HDFS is accessible")
            if result.stdout.strip():
                print(f"   Contents of /:\n{result.stdout}")
            else:
                print("   / directory is empty (expected)")
            return True
        else:
            print(f"⚠️  HDFS check returned error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("⚠️  HDFS check timed out (service may still be starting)")
        return False
    except Exception as e:
        print(f"❌ Error checking HDFS: {e}")
        return False

def main():
    """Main tutorial function."""
    print("=" * 60)
    print("Hadoop Docker Setup for 8GB RAM - Tutorial 1")
    print("=" * 60)
    
    # Step 1: Check prerequisites
    if not check_docker():
        print("\n❌ Please install Docker before continuing.")
        print("   Visit: https://docs.docker.com/get-docker/")
        sys.exit(1)
    
    if not check_docker_compose():
        print("\n❌ Please install Docker Compose before continuing.")
        print("   Visit: https://docs.docker.com/compose/install/")
        sys.exit(1)
    
    # Step 2: Start cluster
    if not start_hadoop_cluster():
        print("\n❌ Failed to start Hadoop cluster.")
        print("   Check if ports 9870, 8088, etc. are already in use.")
        sys.exit(1)
    
    # Step 3: Wait for services to start
    print("\n⏳ Waiting 30 seconds for services to initialize...")
    time.sleep(30)
    
    # Step 4: Check health
    if not check_cluster_health():
        print("\n⚠️  Some services may not be running. Checking again in 30 seconds...")
        time.sleep(30)
        check_cluster_health()
    
    # Step 5: Check HDFS
    print("\n⏳ Checking HDFS (additional 15 second wait)...")
    time.sleep(15)
    check_hdfs()
    
    # Step 6: Show web interfaces
    show_web_interfaces()
    
    # Step 7: Provide next steps
    print("\n" + "=" * 60)
    print("✅ Tutorial 1 Complete!")
    print("=" * 60)
    print("\n📚 Next Steps:")
    print("   1. Open http://localhost:9870 in your browser")
    print("   2. Verify HDFS is running (Storage tab should show capacity)")
    print("   3. Run Tutorial 2: HDFS Basics")
    print("\n🛑 To stop the cluster when done:")
    print("   docker-compose -f docker-compose.yml down")
    print("\n📝 Note: Keep cluster running for next tutorials")

if __name__ == "__main__":
    main()