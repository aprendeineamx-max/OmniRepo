import re
import os
from src.core.logger import setup_logger

class EndpointMapper:
    """
    Cartographer of the API Surface.
    Scans code for exposed HTTP endpoints in common frameworks.
    """

    def __init__(self):
        self.logger = setup_logger(name="EndpointMapper")
        
        self.patterns = {
            "FLASK": r"@app\.route\s*\(\s*['\"](.*?)['\"]",
            "DJANGO": r"path\s*\(\s*['\"](.*?)['\"]",
            "EXPRESS": r"\.?(get|post|put|delete|patch)\s*\(\s*['\"](.*?)['\"]",
            "FASTAPI": r"@app\.(get|post|put|delete|patch)\s*\(\s*['\"](.*?)['\"]"
        }

    def scan(self, file_path):
        """
        Scans a file for API endpoints.
        """
        if not os.path.exists(file_path):
            return []

        endpoints = []
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                lines = content.splitlines()
        except Exception as e:
            self.logger.error(f"Failed to read {file_path}: {e}")
            return []

        for i, line in enumerate(lines, 1):
            
            # Check Flask
            # matches @app.route("/login")
            for match in re.finditer(self.patterns["FLASK"], line):
                endpoints.append({
                    "framework": "Flask",
                    "route": match.group(1),
                    "method": "Unknown (Implicit GET)", # Flask defaults to GET usually, parsing 'methods=[]' is harder via simple regex
                    "lineno": i,
                    "file_path": file_path
                })

            # Check Django
            # matches path('admin/', ...)
            for match in re.finditer(self.patterns["DJANGO"], line):
                endpoints.append({
                    "framework": "Django",
                    "route": match.group(1),
                    "method": "Any", # Django separates method logic in views usually
                    "lineno": i,
                    "file_path": file_path
                })

            # Check Express
            # matches app.get('/users', ...) or router.post('/login')
            # Group 1: method, Group 2: route
            for match in re.finditer(self.patterns["EXPRESS"], line):
                endpoints.append({
                    "framework": "Express (Node)",
                    "route": match.group(2),
                    "method": match.group(1).upper(),
                    "lineno": i,
                    "file_path": file_path
                })

            # Check FastAPI
            # matches @app.get("/items/")
            # Group 1: method, Group 2: route
            for match in re.finditer(self.patterns["FASTAPI"], line):
                endpoints.append({
                    "framework": "FastAPI",
                    "route": match.group(2),
                    "method": match.group(1).upper(),
                    "lineno": i,
                    "file_path": file_path
                })

        return endpoints
