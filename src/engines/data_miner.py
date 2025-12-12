import re
import os
from src.core.logger import setup_logger

class DataMiner:
    """
    Excavates data artifacts from source code.
    Identifies:
    - Raw SQL queries
    - ORM Definitions (Django, SQLAlchemy, Mongoose)
    """

    def __init__(self):
        self.logger = setup_logger(name="DataMiner")
        
        # Compiled Regex Patterns
        self.patterns = {
            "SQL_RAW": [
                r"SELECT\s+.*?\s+FROM\s+[\w_]+",
                r"INSERT\s+INTO\s+[\w_]+",
                r"UPDATE\s+[\w_]+\s+SET",
                r"DELETE\s+FROM\s+[\w_]+"
            ],
            "ORM_DJANGO": [
                r"class\s+(\w+)\s*\(.*models\.Model.*\):"
            ],
            "ORM_MONGOOSE": [
                r"mongoose\.model\s*\(['\"](\w+)['\"]",
                r"new\s+Schema\s*\("
            ],
            "ORM_SQLALCHEMY": [
                r"Column\(",
                r"declarative_base"
            ]
        }

    def mine(self, file_path):
        """
        Scans a file for data artifacts.
        """
        if not os.path.exists(file_path):
            return []

        artifacts = []
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                lines = content.splitlines()
        except Exception as e:
            self.logger.error(f"Failed to read {file_path}: {e}")
            return []

        # Scan for Regex patterns (Global content scan for some, line scan for others if needed)
        # We'll scan content for multi-line robustness or line-by-line for location
        
        # Let's do line-by-line to get line numbers, but some regexes might span lines.
        # For this prototype, line-by-line is safer for simple patterns.
        
        for i, line in enumerate(lines, 1):
            # Check Raw SQL
            for pattern in self.patterns["SQL_RAW"]:
                if re.search(pattern, line, re.IGNORECASE):
                    artifacts.append({
                        "type": "SQL_RAW",
                        "content": line.strip()[:100], # Truncate for sanity
                        "lineno": i,
                        "file_path": file_path
                    })
                    break # detected one sql pattern in this line

            # Check Django
            for pattern in self.patterns["ORM_DJANGO"]:
                match = re.search(pattern, line)
                if match:
                    artifacts.append({
                        "type": "ORM_DJANGO_MODEL",
                        "name": match.group(1),
                        "lineno": i,
                        "file_path": file_path
                    })

            # Check Mongoose
            for pattern in self.patterns["ORM_MONGOOSE"]:
                match = re.search(pattern, line)
                if match:
                    name = match.group(1) if match.lastindex else "Unknown" # new Schema might not have capture group
                    artifacts.append({
                        "type": "ORM_MONGOOSE",
                        "name": name,
                        "subtype": "Schema/Model",
                        "lineno": i,
                        "file_path": file_path
                    })

            # Check SQLAlchemy
            for pattern in self.patterns["ORM_SQLALCHEMY"]:
                if re.search(pattern, line):
                    artifacts.append({
                        "type": "ORM_SQLALCHEMY",
                        "content": line.strip(),
                        "lineno": i,
                        "file_path": file_path
                    })

        return artifacts
