import json
import os
import sys

# Add root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from src.core.logger import setup_logger

class PolyglotEngine:
    def __init__(self):
        self.manifest_path = os.path.join(root_dir, "vault", "manifest.json")
        self.logger = setup_logger(name="PolyglotEngine")
        
        # Rosetta Map
        self.extension_map = {
            ".py": "Python",
            ".js": "JavaScript",
            ".jsx": "JavaScript",
            ".ts": "TypeScript",
            ".tsx": "TypeScript",
            ".html": "HTML",
            ".css": "CSS",
            ".scss": "CSS",
            ".md": "Markdown",
            ".json": "JSON",
            ".java": "Java",
            ".c": "C",
            ".cpp": "C++",
            ".h": "C/C++ Header",
            ".rs": "Rust",
            ".go": "Go",
            ".rb": "Ruby",
            ".php": "PHP",
            ".sh": "Shell",
            ".bat": "Batch",
            ".ps1": "PowerShell",
            ".yaml": "YAML",
            ".yml": "YAML",
            ".xml": "XML",
            ".sql": "SQL",
            ".dockerfile": "Dockerfile",
            "dockerfile": "Dockerfile" # sometimes no extension
        }

    def analyze(self):
        """
        Reads manifest, calculates language distribution, updates manifest.
        """
        self.logger.info("Initiating Linguistic Analysis...")
        
        if not os.path.exists(self.manifest_path):
            self.logger.error("Manifest not found. Run Recon first.")
            return False

        try:
            with open(self.manifest_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            extensions = data.get("extensions", {})
            total_files = data.get("total_files", 0)
            
            if total_files == 0:
                self.logger.warning("No files to analyze.")
                return False

            lang_counts = {}
            unknown_count = 0

            for ext, count in extensions.items():
                # Handle special cases or normalize
                normalized_ext = ext.lower()
                
                lang = self.extension_map.get(normalized_ext)
                if not lang:
                    # Try checking if the extension itself is a known filename (like Dockerfile)
                    # But the manifest usually gives the extension part. 
                    # If ext is empty string (no extension files), check map for ""?
                    # For now map unknowns to "Other"
                    lang = "Other"
                    # Log unknowns if needed?
                
                lang_counts[lang] = lang_counts.get(lang, 0) + count

            # Calculate percentages
            distribution = {}
            for lang, count in lang_counts.items():
                percent = (count / total_files) * 100
                distribution[lang] = round(percent, 2)
            
            # Update data
            data["languages"] = distribution
            
            # Save back
            with open(self.manifest_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
                
            self.logger.info(f"Language Analysis Complete. Distribution: {distribution}")
            return True

        except Exception as e:
            self.logger.error(f"Polyglot failure: {e}")
            return False

if __name__ == "__main__":
    poly = PolyglotEngine()
    poly.analyze()
