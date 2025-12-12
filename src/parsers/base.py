from abc import ABC, abstractmethod
import json

class BaseParser(ABC):
    """
    Abstract Base Class for all language-specific parsers.
    Enforces a strict contract to ensure uniform data extraction.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        # Derived classes should populate these during parse()
        self.functions = []
        self.classes = []
        self.imports = []
        self.raw_ast = None

    @abstractmethod
    def parse(self):
        """
        Main logic to read file and build the AST.
        """
        pass

    @abstractmethod
    def get_functions(self):
        """
        Returns a list of function definitions found.
        Format: [{'name': 'foo', 'args': ['a', 'b'], 'lineno': 10, ...}]
        """
        pass

    @abstractmethod
    def get_classes(self):
        """
        Returns a list of class definitions found.
        """
        pass

    @abstractmethod
    def get_imports(self):
        """
        Returns a list of imported modules/files.
        Vital for constructing the dependency graph.
        """
        pass

    def to_json(self):
        """
        Standardizes the parser output into a dictionary.
        This provides the uniform structure for the Anatomy DB.
        """
        return {
            "file_path": self.file_path,
            "functions": self.get_functions(),
            "classes": self.get_classes(),
            "imports": self.get_imports(),
            # "ast": str(self.raw_ast) # Optional debug info
        }
