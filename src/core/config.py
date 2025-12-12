import os
import yaml
import sys
from dotenv import load_dotenv

# Add root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))
if root_dir not in sys.path:
    sys.path.append(root_dir)

class Config:
    def __init__(self):
        self.config_path = os.path.join(root_dir, "config.yaml")
        self.env_path = os.path.join(root_dir, ".env")
        self.settings = self._load_config()
        self._load_env()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            # Fallback defaults if config.yaml is missing
            return {
                "project_name": "Quirófano Digital (Default)",
                "limits": {"max_repo_size_mb": 500}
            }
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"[CRITICAL] Error loading config.yaml: {e}")
            return {}

    def _load_env(self):
        load_dotenv(self.env_path)

    def get(self, key, default=None):
        """Metadata retrieval (keys can be nested: 'limits.max_repo_size_mb')"""
        keys = key.split('.')
        value = self.settings
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

# Global instance
settings = Config()
