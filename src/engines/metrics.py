import ast
import os
from src.core.logger import setup_logger

class MetricsEngine:
    """
    Analyzes code complexity.
    - Python: Uses AST for precise Cyclomatic Complexity (McCabe).
    - Others: Uses heuristics (Indentation, LOC).
    """
    
    def __init__(self, high_risk_threshold=10, critical_threshold=20):
        self.logger = setup_logger(name="MetricsEngine")
        self.high_risk_threshold = high_risk_threshold
        self.critical_threshold = critical_threshold

    def analyze(self, file_path):
        """
        Calculates metrics for a file.
        Returns a dict with file-level and function-level metrics.
        """
        if not os.path.exists(file_path):
            self.logger.error(f"File not found: {file_path}")
            return None
            
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ['.py']:
            return self._analyze_python(file_path)
        else:
            return self._analyze_generic(file_path)

    def _analyze_python(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()
            tree = ast.parse(source)
        except Exception as e:
            self.logger.error(f"Failed to parse python file {file_path}: {e}")
            return None

        metrics = {
            "file_path": file_path,
            "language": "Python",
            "loc": len(source.splitlines()),
            "functions": []
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self._calculate_mccabe(node)
                status = "OK"
                if complexity > self.critical_threshold:
                    status = "CRITICAL (MONSTER)"
                elif complexity > self.high_risk_threshold:
                    status = "WARNING"

                metrics["functions"].append({
                    "name": node.name,
                    "lineno": node.lineno,
                    "complexity": complexity,
                    "status": status
                })
        
        return metrics

    def _calculate_mccabe(self, node):
        """
        Calculates Cyclomatic Complexity.
        Start = 1
        +1 for each control flow branch.
        """
        complexity = 1
        for child in ast.walk(node):
            # Control flow structures
            if isinstance(child, (ast.If, ast.For, ast.AsyncFor, ast.While, 
                                  ast.With, ast.AsyncWith, ast.Assert, 
                                  ast.ExceptHandler)):
                complexity += 1
            # Boolean operators
            elif isinstance(child, ast.BoolOp):
                # +1 for each operator (And, Or). 
                # (a and b and c) is 2 operators, so complexity += 2
                complexity += len(child.values) - 1
                
        return complexity

    def _analyze_generic(self, file_path):
        """
        Heuristic analysis for non-Python files.
        """
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except Exception:
            return None

        loc = len([l for l in lines if l.strip()])
        
        # Max indentation depth (assuming 4 spaces per level)
        max_indent = 0
        for line in lines:
            stripped = line.lstrip()
            if not stripped: continue
            indent = len(line) - len(stripped)
            max_indent = max(max_indent, indent)
            
        approx_depth = max_indent // 4 

        return {
            "file_path": file_path,
            "language": "Generic",
            "loc": loc,
            "heuristic_depth": approx_depth,
            "note": "Metrics approximated via heuristics"
        }
