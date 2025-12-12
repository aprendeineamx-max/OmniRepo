import os

class DependencyResolver:
    """
    Resolves import strings to absolute file paths on the local filesystem.
    Handles language-specific nuances (implicit extensions, relative paths, etc).
    """
    
    def __init__(self, root_path):
        """
        root_path: The root directory of the analyzed repository (e.g. /vault/repo_target)
        """
        self.root_path = os.path.abspath(root_path)

    def resolve(self, source_file_path, import_string, language):
        """
        Returns:
            - Absolute path to the file if found.
            - "EXTERNAL_LIB" if it's a library/built-in.
            - None if resolution fails but looks like a local path.
        """
        source_dir = os.path.dirname(os.path.abspath(source_file_path))
        
        if language.lower() in ["python", "py"]:
            return self._resolve_python(source_dir, import_string)
        elif language.lower() in ["javascript", "typescript", "js", "ts", "jsx", "tsx"]:
            return self._resolve_js(source_dir, import_string)
        
        return None

    def _resolve_python(self, source_dir, import_string):
        # 1. Handle Relative Imports (from . import x, from ..sub import y)
        if import_string.startswith('.'):
            # Calculate base level based on dots
            level = 0
            temp_import = import_string
            while temp_import.startswith('.'):
                level += 1
                temp_import = temp_import[1:]
            
            # Navigate up directories
            base_dir = source_dir
            for _ in range(level - 1):
                base_dir = os.path.dirname(base_dir)
            
            # Construct candidate path
            # import_string ".utils" -> level 1, temp "utils"
            parts = temp_import.split('.')
            candidate_base = os.path.join(base_dir, *parts)
            
            return self._finalize_py_path(candidate_base)

        # 2. Handle Absolute/Library Imports
        # In a real project, we might check sys.path or local root.
        # For now, simplistic check if it exists relative to root
        # e.g. import src.core.config
        parts = import_string.split('.')
        candidate_from_root = os.path.join(self.root_path, *parts)
        local_path = self._finalize_py_path(candidate_from_root)
        
        if local_path:
            return local_path
        
        # If not local, assume external
        return "EXTERNAL_LIB"

    def _finalize_py_path(self, base_path):
        # Try .py
        if os.path.exists(base_path + ".py"):
            return base_path + ".py"
        
        # Try package (__init__.py)
        init_path = os.path.join(base_path, "__init__.py")
        if os.path.exists(init_path):
            return init_path
            
        return None

    def _resolve_js(self, source_dir, import_string):
        # 1. Handle Relative Imports (./, ../)
        if import_string.startswith('./') or import_string.startswith('../'):
            candidate_base = os.path.normpath(os.path.join(source_dir, import_string))
            return self._finalize_js_path(candidate_base)
            
        # 2. Handle Absolute/Module Imports
        # If it doesn't start with ./ or /, it's usually a node_module or alias
        # For this prototype, we treat non-relative as EXTERNAL unless configured with aliases
        # (Aliases logic requires reading tsconfig/webpack, deferred)
        return "EXTERNAL_LIB"

    def _finalize_js_path(self, base_path):
        # List of extensions to try
        extensions = ['.js', '.jsx', '.ts', '.tsx', '.json']
        
        # 1. Exact match (rare for imports but possible)
        if os.path.exists(base_path) and os.path.isfile(base_path):
            return base_path
            
        # 2. Try extensions
        for ext in extensions:
            if os.path.exists(base_path + ext):
                return base_path + ext
                
        # 3. Try directory index
        if os.path.isdir(base_path):
            for ext in extensions:
                index_path = os.path.join(base_path, f"index{ext}")
                if os.path.exists(index_path):
                    return index_path
                    
        return None
