from src.parsers.base import BaseParser
import sys

def test_architecture():
    print("TEST 1: Enforcing Abstract Contract...")
    try:
        # Should fail
        parser = BaseParser("dummy.txt")
        print("FAIL: BaseParser was instantiated directly (Impossible!)")
        sys.exit(1)
    except TypeError as e:
        print(f"PASS: Correctly rejected instantiation ({e})")

    print("\nTEST 2: Testing Concrete Implementation...")
    
    class DummyParser(BaseParser):
        def parse(self):
            self.raw_ast = "DUMMY_AST"
            
        def get_functions(self):
            return [{"name": "test_func", "lineno": 1}]
            
        def get_classes(self):
            return []
            
        def get_imports(self):
            return ["os", "sys"]

    try:
        dummy = DummyParser("test.py")
        dummy.parse()
        data = dummy.to_json()
        
        print(f"PASS: Concrete Parser Instantiated.")
        print(f"DATA OUTPUT: {data}")
        
        if data['imports'] == ['os', 'sys']:
            print("PASS: Data structure verified.")
        else:
            print("FAIL: Data mismatch.")
            sys.exit(1)
            
    except Exception as e:
        print(f"FAIL: Implementation error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_architecture()
