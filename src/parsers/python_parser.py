import ast
import os
from src.parsers.base import BaseParser

class PythonParser(BaseParser):
    def parse(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"{self.file_path} does not exist.")
            
        with open(self.file_path, "r", encoding="utf-8") as f:
            source = f.read()
        self.raw_ast = ast.parse(source)

    def get_functions(self):
        funcs = []
        for node in ast.walk(self.raw_ast):
            if isinstance(node, ast.FunctionDef):
                # Extract args
                args = [arg.arg for arg in node.args.args]
                # Extract decorators
                decorators = []
                for dec in node.decorator_list:
                    if isinstance(dec, ast.Name):
                        decorators.append(dec.id)
                    elif isinstance(dec, ast.Call):
                        # Handle @decorator(args) - simple case
                        if isinstance(dec.func, ast.Name):
                            decorators.append(dec.func.id)
                        elif isinstance(dec.func, ast.Attribute):
                             decorators.append(dec.func.attr)

                funcs.append({
                    "name": node.name,
                    "lineno": node.lineno,
                    "args": args,
                    "decorators": decorators,
                    "docstring": ast.get_docstring(node)
                })
        return funcs

    def get_classes(self):
        classes = []
        for node in ast.walk(self.raw_ast):
            if isinstance(node, ast.ClassDef):
                bases = []
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        bases.append(base.id)
                    elif isinstance(base, ast.Attribute):
                        bases.append(base.attr)
                        
                methods = []
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        methods.append(item.name)
                
                classes.append({
                    "name": node.name,
                    "lineno": node.lineno,
                    "bases": bases,
                    "methods": methods,
                    "docstring": ast.get_docstring(node)
                })
        return classes

    def get_imports(self):
        imports = []
        for node in ast.walk(self.raw_ast):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        "module": alias.name,
                        "alias": alias.asname
                    })
            elif isinstance(node, ast.ImportFrom):
                module = node.module
                for alias in node.names:
                    imports.append({
                        "module": module,
                        "name": alias.name,
                        "alias": alias.asname
                    })
        return imports
