import re
import os
from src.parsers.base import BaseParser

class JSParser(BaseParser):
    def parse(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"{self.file_path} does not exist.")
            
        with open(self.file_path, "r", encoding="utf-8", errors="ignore") as f:
            self.lines = f.readlines()
            
        self.source = "".join(self.lines)

    def get_functions(self):
        """
        Regex based extraction for:
        - function name()
        - const name = () =>
        - const name = function()
        """
        funcs = []
        
        # Pattern 1: function myFunc()
        p1 = r"function\s+([a-zA-Z0-9_$]+)\s*\("
        
        # Pattern 2: const/let/var myFunc = ...
        # Catches arrow functions and function expressions
        p2 = r"(?:const|let|var)\s+([a-zA-Z0-9_$]+)\s*=\s*(?:\([^)]*\)|[a-zA-Z0-9_$]+)\s*=>"
        p3 = r"(?:const|let|var)\s+([a-zA-Z0-9_$]+)\s*=\s*function"

        # Scan line by line for line numbers (Regex on full text loses line info easily)
        for i, line in enumerate(self.lines, 1):
            # Check P1
            for match in re.finditer(p1, line):
                funcs.append({"name": match.group(1), "lineno": i, "type": "function_declaration"})
            
            # Check P2 (Arrows)
            for match in re.finditer(p2, line):
                funcs.append({"name": match.group(1), "lineno": i, "type": "arrow_function"})

            # Check P3 (Expressions)
            for match in re.finditer(p3, line):
                funcs.append({"name": match.group(1), "lineno": i, "type": "function_expression"})
                
        return funcs

    def get_classes(self):
        """
        Regex for: class MyClass extends Parent
        """
        classes = []
        # Pattern: class Name [extends Parent]
        pattern = r"class\s+([a-zA-Z0-9_$]+)(?:\s+extends\s+([a-zA-Z0-9_$]+))?"
        
        for i, line in enumerate(self.lines, 1):
            for match in re.finditer(pattern, line):
                cls_data = {
                    "name": match.group(1),
                    "lineno": i,
                    "extends": match.group(2) if match.group(2) else None
                }
                classes.append(cls_data)
        return classes

    def get_imports(self):
        """
        Regex for ES6 and CommonJS imports
        """
        imports = []
        
        # ES6: import ... from 'path'
        # Group 1: imports content, Group 2: quote, Group 3: path
        p_es6 = r"import\s+(?:(.+?)\s+from\s+)?(['\"])(.+?)\2"
        
        # CommonJS: const x = require('path')
        # Group 1: quote, Group 2: path
        p_cjs = r"require\s*\(\s*(['\"])(.+?)\1\s*\)"

        for i, line in enumerate(self.lines, 1):
            # ES6
            for match in re.finditer(p_es6, line):
                raw_imports = match.group(1)
                module_path = match.group(3)
                names = []
                if raw_imports:
                    # simplistic cleaning of { X, Y as Z } or * as X or Default
                    cleaned = raw_imports.replace("{", "").replace("}", "").strip()
                    names = [n.strip() for n in cleaned.split(",")]
                
                imports.append({
                    "module": module_path,
                    "type": "es6",
                    "names": names,
                    "lineno": i
                })
            
            # CommonJS
            for match in re.finditer(p_cjs, line):
                imports.append({
                    "module": match.group(2),
                    "type": "commonjs",
                    "names": ["*"], # Usually assigns to a variable, but for deps graph module is key
                    "lineno": i
                })
                
        return imports
