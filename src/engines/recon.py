import os
import json
import sys
from collections import defaultdict

# Add root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from src.core.logger import setup_logger

class ReconEngine:
    def __init__(self, target_path="vault/repo_target"):
        self.target_path = os.path.join(root_dir, target_path)
        self.manifest_path = os.path.join(root_dir, "vault", "manifest.json")
        self.logger = setup_logger(name="ReconEngine")

    def scan(self):
        """
        Performs a surface scan of the target repository.
        """
        self.logger.info(f"Initiating Recon Scan on sector: {self.target_path}")
        
        if not os.path.exists(self.target_path):
            self.logger.error("Target not found. Is the vault empty?")
            return False

        stats = {
            "total_files": 0,
            "total_size_mb": 0.0,
            "max_depth": 0,
            "extensions": defaultdict(int),
            "topography": [] # Folder structure summary could go here, keeping it simple for now
        }

        start_depth = self.target_path.rstrip(os.sep).count(os.sep)

        for root, dirs, files in os.walk(self.target_path):
            # Calculate Depth
            current_depth = root.count(os.sep) - start_depth
            if current_depth > stats["max_depth"]:
                stats["max_depth"] = current_depth

            for file in files:
                file_path = os.path.join(root, file)
                
                # File Size
                try:
                    size = os.path.getsize(file_path)
                    stats["total_size_mb"] += size
                except OSError:
                    pass

                # Extension Count
                _, ext = os.path.splitext(file)
                ext = ext.lower() if ext else "(no_ext)"
                stats["extensions"][ext] += 1
                stats["total_files"] += 1

        # Convert size to MB
        stats["total_size_mb"] = round(stats["total_size_mb"] / (1024 * 1024), 4)
        
        # Convert defaultdict to dict for JSON serialization
        stats["extensions"] = dict(stats["extensions"])

        self._generate_manifest(stats)
        return True

    def _generate_manifest(self, stats):
        try:
            with open(self.manifest_path, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=4)
            self.logger.info(f"Manifest generated: {self.manifest_path}")
            self.logger.info(f"Scan Result: {stats['total_files']} files, {stats['total_size_mb']} MB")
        except Exception as e:
            self.logger.error(f"Failed to write manifest: {e}")

if __name__ == "__main__":
    recon = ReconEngine()
    
    # Ensure there is something to scan (if vault is empty, create dummy)
    if not os.path.exists(recon.target_path):
        os.makedirs(recon.target_path, exist_ok=True)
        with open(os.path.join(recon.target_path, "dummy.py"), "w") as f:
            f.write("print('Hello World')")
        print("Created dummy content for validation.")

    recon.scan()
