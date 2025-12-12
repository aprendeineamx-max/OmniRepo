import os
import sys

def init_project():
    """
    Initializes the directory structure for Project Prometheus (Quirófano Digital).
    """
    base_dir = os.getcwd()
    
    # Define the structure based on ROADMAP_GENESIS.md
    structure = [
        "vault",          # Quarantine zone
        "src/core",       # Logical brain
        "src/nexus",      # Communication system
        "storage"         # Persistent DBs
    ]

    print(f"[GENESIS] Initializing structure in: {base_dir}")

    for folder in structure:
        path = os.path.join(base_dir, folder)
        try:
            os.makedirs(path, exist_ok=True)
            print(f"[OK] Created/Verified: {folder}")
            
            # Add __init__.py to src subdirectories to make them packages
            if folder.startswith("src/"):
                init_file = os.path.join(path, "__init__.py")
                with open(init_file, 'a') as f:
                    pass
                print(f"    -> Injected __init__.py in {folder}")

        except Exception as e:
            print(f"[ERROR] Failed to create {folder}: {e}")
            sys.exit(1)

    print("\n[SUCCESS] Bunker construction complete. The environment is sterile.")

if __name__ == "__main__":
    init_project()
