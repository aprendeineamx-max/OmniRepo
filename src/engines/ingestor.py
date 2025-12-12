import os
import shutil
import subprocess
import sys
import re

# Add root to path to find src.core
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from src.core.logger import setup_logger

class Ingestor:
    def __init__(self, vault_path="vault"):
        self.vault_path = os.path.join(root_dir, vault_path)
        self.target_path = os.path.join(self.vault_path, "repo_target")
        self.logger = setup_logger(name="IngestorEngine")
        self.max_size_mb = 500

    def cleanup_vault(self):
        """
        Nukes the quarantine zone (vault) to ensure sterility.
        Safety: Only deletes files INSIDE self.vault_path.
        """
        self.logger.info(f"Initiating cleanup of quarantine zone: {self.vault_path}")
        
        if not os.path.exists(self.vault_path):
            os.makedirs(self.vault_path, exist_ok=True)
            return

        for item in os.listdir(self.vault_path):
            item_path = os.path.join(self.vault_path, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            except Exception as e:
                self.logger.error(f"Failed to delete {item_path}: {e}")
        
        self.logger.info("Vault contents incinerated. Area sterile.")

    def validate_url(self, url):
        """
        Checks if the URL matches standard GitHub format.
        """
        pattern = r"https://github\.com/[\w-]+/[\w.-]+"
        if re.match(pattern, url):
            return True
        return False

    def check_size(self):
        """
        Calculates size of the cloned repo.
        Returns size in MB.
        """
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(self.target_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)

        size_mb = total_size / (1024 * 1024)
        return size_mb

    def clone_repo(self, url):
        """
        Clones the repo into the vault.
        """
        if not self.validate_url(url):
            self.logger.error(f"Invalid URL rejected: {url}")
            return False

        self.cleanup_vault()
        
        self.logger.info(f"Engaging Git Cloner for target: {url}")
        try:
            # Using subprocess to call git directly
            result = subprocess.run(
                ["git", "clone", "--depth", "1", url, self.target_path],
                check=True,
                capture_output=True,
                text=True
            )
            self.logger.info("Clone operation complete.")
            
            # Verify Size
            size_mb = self.check_size()
            self.logger.info(f"Biomass assessment: {size_mb:.2f} MB")
            
            if size_mb > self.max_size_mb:
                self.logger.hazmat(f"BIOHAZARD ALERT: Repo exceeds safety limit ({size_mb:.2f}MB > {self.max_size_mb}MB)")
                self.logger.warning("Suggesting immediate purge.")
                # Optional: self.cleanup_vault() # Disabled for now to allow inspection if needed
                return False
                
            return True

        except subprocess.CalledProcessError as e:
            self.logger.error(f"Git Clone Failed: {e.stderr}")
            return False
        except Exception as e:
            self.logger.error(f"Critical Ingestion Error: {e}")
            return False

if __name__ == "__main__":
    engine = Ingestor()
    test_url = "https://github.com/octocat/Spoon-Knife"
    print(f"Testing ingestion of {test_url}...")
    success = engine.clone_repo(test_url)
    if success:
        print("TEST SUCCESS: Organism captured in vault.")
    else:
        print("TEST FAILED: Ingestion failed.")
