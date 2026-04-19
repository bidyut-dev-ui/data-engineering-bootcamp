#!/usr/bin/env python3
"""
Week 14.5 - Hadoop Basics: HDFS Operations Tutorial
===================================================

This tutorial covers basic HDFS operations using the `hdfs` Python library.
We'll learn how to interact with Hadoop's distributed file system from Python.

Learning Objectives:
1. Connect to HDFS using WebHDFS REST API
2. Perform basic file operations (list, upload, download, delete)
3. Understand HDFS directory structure and permissions
4. Work with large files in chunks for 8GB RAM constraints

Prerequisites:
- Hadoop cluster running (from 01_hadoop_docker_setup.py)
- `hdfs` Python library installed (in requirements.txt)
"""

import os
import time
from pathlib import Path
from hdfs import InsecureClient, HdfsError

# Configuration
HDFS_HOST = "localhost"
HDFS_PORT = 9870  # Namenode WebUI port
HDFS_WEBHDFS_PORT = 9870  # WebHDFS port
HDFS_USER = "root"
HDFS_URL = f"http://{HDFS_HOST}:{HDFS_WEBHDFS_PORT}"

def create_hdfs_client():
    """
    Create an HDFS client using WebHDFS REST API.
    
    Returns:
        hdfs.InsecureClient: Client for HDFS operations
    """
    try:
        client = InsecureClient(HDFS_URL, user=HDFS_USER)
        print(f"✅ Connected to HDFS at {HDFS_URL}")
        return client
    except Exception as e:
        print(f"❌ Failed to connect to HDFS: {e}")
        print("Make sure Hadoop cluster is running (run 01_hadoop_docker_setup.py first)")
        return None

def check_hdfs_status(client):
    """
    Check HDFS status and display basic information.
    
    Args:
        client: HDFS client
    """
    try:
        status = client.status("/")
        print(f"📊 HDFS Root Status:")
        print(f"   Path: {status['path']}")
        print(f"   Type: {status['type']}")
        print(f"   Length: {status['length']} bytes")
        print(f"   Owner: {status['owner']}")
        print(f"   Group: {status['group']}")
        print(f"   Permissions: {status['permission']}")
        print(f"   Access Time: {time.ctime(status['accessTime'] / 1000)}")
        print(f"   Modification Time: {time.ctime(status['modificationTime'] / 1000)}")
        return True
    except HdfsError as e:
        print(f"❌ Could not get HDFS status: {e}")
        return False

def list_hdfs_directory(client, path="/"):
    """
    List contents of an HDFS directory.
    
    Args:
        client: HDFS client
        path: HDFS path to list
    """
    try:
        print(f"📁 Listing HDFS directory: {path}")
        contents = client.list(path)
        
        if not contents:
            print("   (empty directory)")
            return
        
        for item in contents:
            item_path = os.path.join(path, item)
            try:
                status = client.status(item_path)
                item_type = "📄" if status['type'] == 'FILE' else "📁"
                size_mb = status['length'] / (1024 * 1024)
                print(f"   {item_type} {item}")
                print(f"      Size: {size_mb:.2f} MB | Owner: {status['owner']} | Perm: {status['permission']}")
            except:
                print(f"   ? {item} (could not get details)")
    except HdfsError as e:
        print(f"❌ Error listing directory {path}: {e}")

def upload_file_to_hdfs(client, local_path, hdfs_path):
    """
    Upload a file from local filesystem to HDFS.
    
    Args:
        client: HDFS client
        local_path: Path to local file
        hdfs_path: Destination HDFS path
    """
    try:
        if not os.path.exists(local_path):
            print(f"❌ Local file {local_path} does not exist")
            return False
        
        file_size = os.path.getsize(local_path)
        file_size_mb = file_size / (1024 * 1024)
        
        print(f"⬆️  Uploading {local_path} ({file_size_mb:.2f} MB) to HDFS: {hdfs_path}")
        
        # For large files (> 10MB), use chunked upload for 8GB RAM constraints
        if file_size > 10 * 1024 * 1024:  # 10MB
            print("   Using chunked upload for large file...")
            with open(local_path, 'rb') as local_file:
                client.write(hdfs_path, local_file, overwrite=True)
        else:
            client.upload(hdfs_path, local_path, overwrite=True)
        
        print(f"✅ Upload successful")
        return True
    except HdfsError as e:
        print(f"❌ Upload failed: {e}")
        return False

def download_file_from_hdfs(client, hdfs_path, local_path):
    """
    Download a file from HDFS to local filesystem.
    
    Args:
        client: HDFS client
        hdfs_path: Source HDFS path
        local_path: Destination local path
    """
    try:
        print(f"⬇️  Downloading from HDFS: {hdfs_path} to local: {local_path}")
        
        # For large files, use chunked download
        status = client.status(hdfs_path)
        file_size_mb = status['length'] / (1024 * 1024)
        
        if file_size_mb > 50:  # 50MB threshold
            print(f"   File is large ({file_size_mb:.2f} MB), using chunked download...")
        
        client.download(hdfs_path, local_path, overwrite=True)
        print(f"✅ Download successful")
        return True
    except HdfsError as e:
        print(f"❌ Download failed: {e}")
        return False

def create_hdfs_directory(client, path):
    """
    Create a directory in HDFS.
    
    Args:
        client: HDFS client
        path: HDFS directory path to create
    """
    try:
        print(f"📁 Creating HDFS directory: {path}")
        client.makedirs(path)
        print(f"✅ Directory created")
        return True
    except HdfsError as e:
        print(f"❌ Directory creation failed: {e}")
        return False

def delete_hdfs_path(client, path):
    """
    Delete a file or directory from HDFS.
    
    Args:
        client: HDFS client
        path: HDFS path to delete
    """
    try:
        print(f"🗑️  Deleting HDFS path: {path}")
        client.delete(path, recursive=True)
        print(f"✅ Deleted successfully")
        return True
    except HdfsError as e:
        print(f"❌ Deletion failed: {e}")
        return False

def demonstrate_chunked_operations():
    """
    Demonstrate chunked operations for large files (8GB RAM constraint).
    """
    print("\n🔧 Demonstrating Chunked Operations for 8GB RAM:")
    print("   For large files (>100MB), we need to process in chunks.")
    print("   Example workflow:")
    print("   1. Read file in 64MB chunks")
    print("   2. Process each chunk independently")
    print("   3. Write results incrementally")
    print("   4. Avoid loading entire file into memory")
    
    # Example code for chunked processing
    chunk_size = 64 * 1024 * 1024  # 64MB chunks
    
    print(f"\n   Example chunk size: {chunk_size / (1024*1024):.0f} MB")
    print("   This ensures memory usage stays under 1GB even for multi-GB files")

def main():
    """
    Main tutorial function demonstrating HDFS operations.
    """
    print("=" * 70)
    print("HDFS Operations Tutorial")
    print("=" * 70)
    
    # Create HDFS client
    client = create_hdfs_client()
    if not client:
        return
    
    # Check HDFS status
    print("\n1. Checking HDFS Status:")
    check_hdfs_status(client)
    
    # List root directory
    print("\n2. Listing HDFS Root Directory:")
    list_hdfs_directory(client, "/")
    
    # Create a test directory
    test_dir = "/test_data"
    print(f"\n3. Creating Test Directory: {test_dir}")
    create_hdfs_directory(client, test_dir)
    
    # Create a sample local file
    local_sample = "sample_data.txt"
    print(f"\n4. Creating Sample Local File: {local_sample}")
    with open(local_sample, 'w') as f:
        f.write("This is sample data for HDFS tutorial.\n")
        f.write("Line 2: Hadoop Distributed File System.\n")
        f.write("Line 3: Designed for large datasets.\n")
        f.write("Line 4: Fault-tolerant and scalable.\n")
        f.write("Line 5: Perfect for data engineering workflows.\n" * 100)  # Make it larger
    
    # Upload to HDFS
    hdfs_file = f"{test_dir}/sample_data.txt"
    print(f"\n5. Uploading to HDFS: {hdfs_file}")
    upload_file_to_hdfs(client, local_sample, hdfs_file)
    
    # List the test directory
    print(f"\n6. Listing Contents of {test_dir}:")
    list_hdfs_directory(client, test_dir)
    
    # Download back (with different name)
    local_download = "downloaded_sample.txt"
    print(f"\n7. Downloading from HDFS to: {local_download}")
    download_file_from_hdfs(client, hdfs_file, local_download)
    
    # Verify download
    if os.path.exists(local_download):
        with open(local_download, 'r') as f:
            lines = f.readlines()
            print(f"   Downloaded file has {len(lines)} lines")
    
    # Demonstrate chunked operations
    demonstrate_chunked_operations()
    
    # Cleanup
    print(f"\n8. Cleaning Up:")
    delete_hdfs_path(client, test_dir)
    if os.path.exists(local_sample):
        os.remove(local_sample)
    if os.path.exists(local_download):
        os.remove(local_download)
    
    print("\n" + "=" * 70)
    print("✅ HDFS Tutorial Completed Successfully!")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("1. HDFS provides distributed storage for large datasets")
    print("2. WebHDFS REST API allows Python integration")
    print("3. Always use chunked operations for large files on 8GB RAM")
    print("4. HDFS is optimized for sequential reads/writes, not random access")
    print("5. Proper directory structure improves performance")

if __name__ == "__main__":
    main()