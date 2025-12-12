from src.parsers.js_parser import JSParser
import os
import json

DUMMY_FILE = "dummy_react.jsx"

CODE = """
import React, { useState } from 'react';
import { Button } from './components/ui';
const axios = require('axios');

class ErrorBoundary extends React.Component {
    render() {
        return <h1>Error</h1>;
    }
}

function HelperFunc(a, b) {
    return a + b;
}

const MyComponent = (props) => {
    const handleClick = () => {
        console.log("Clicked");
    };
    
    return <Button onClick={handleClick} />;
};

const LegacyFunc = function() {
    return true;
};
"""

def test_js_parser():
    print(f"Creating {DUMMY_FILE}...")
    with open(DUMMY_FILE, "w") as f:
        f.write(CODE)

    print("Running JSParser...")
    parser = JSParser(DUMMY_FILE)
    parser.parse()
    
    data = parser.to_json()
    print(json.dumps(data, indent=4))

    # Assertions
    funcs = [f['name'] for f in data['functions']]
    classes = [c['name'] for c in data['classes']]
    imports = [i['module'] for i in data['imports']]
    
    print("\nVerifying...")
    
    # Check Imports
    if 'react' in imports and './components/ui' in imports and 'axios' in imports:
        print("✅ IMPORTS DETECTED")
    else:
        print("❌ IMPORTS FAILED", imports)

    # Check Classes
    if 'ErrorBoundary' in classes:
        print("✅ CLASSES DETECTED")
    else:
        print("❌ CLASSES FAILED", classes)

    # Check Functions
    expected_funcs = ['HelperFunc', 'MyComponent', 'handleClick', 'LegacyFunc']
    if all(f in funcs for f in expected_funcs):
        print("✅ FUNCTIONS DETECTED (Declarations, Arrows, Expressions)")
    else:
        print("❌ FUNCTIONS FAILED", funcs)

    # Cleanup
    os.remove(DUMMY_FILE)
    print("Cleanup complete.")

if __name__ == "__main__":
    test_js_parser()
