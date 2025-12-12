from src.parsers.python_parser import PythonParser
import json
import os

def test_metacognition():
    # The parser analyzes itself
    target_file = os.path.join("src", "parsers", "python_parser.py")
    
    print(f"Initiating Metacognition Test on: {target_file}")
    
    parser = PythonParser(target_file)
    parser.parse()
    
    data = parser.to_json()
    print(json.dumps(data, indent=4))
    
    # Validation
    functions = [f['name'] for f in data['functions']]
    classes = [c['name'] for c in data['classes']]
    
    expected_funcs = ['parse', 'get_functions', 'get_classes', 'get_imports']
    expected_class = 'PythonParser'
    
    if expected_class in classes and all(f in functions for f in expected_funcs):
        print("\n✅ SUCCESS: The parser understands itself.")
    else:
        print("\n❌ FAILURE: Metacognition incomplete.")

if __name__ == "__main__":
    test_metacognition()
