import sys
import platform
import shutil

def check_tool(name):
    path = shutil.which(name)
    print(f"[{'OK' if path else 'MISSING'}] {name}: {path or 'Not found'}")

def main():
    print("=== Environment Check ===")
    print(f"Python Version: {sys.version}")
    print(f"OS: {platform.system()} {platform.release()}")
    
    print("\n--- Tool Availability ---")
    check_tool("git")
    check_tool("docker")
    check_tool("code") # VS Code CLI
    
    print("\n--- Library Check ---")
    try:
        import pandas
        print(f"[OK] pandas: {pandas.__version__}")
    except ImportError:
        print("[MISSING] pandas")

    print("\n=== End Check ===")

if __name__ == "__main__":
    main()
