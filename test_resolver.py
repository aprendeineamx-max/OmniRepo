import os
import shutil
from src.engines.dependency_resolver import DependencyResolver

TEST_ROOT = "test_fs"

def create_structure():
    if os.path.exists(TEST_ROOT):
        shutil.rmtree(TEST_ROOT)
    os.makedirs(TEST_ROOT)
    
    # Structure:
    # /src
    #   /components
    #     Button.js
    #   /utils
    #     index.js
    #     helper.ts
    #   main.py
    #   /core
    #     config.py
    #     __init__.py
    
    os.makedirs(os.path.join(TEST_ROOT, "src", "components"))
    os.makedirs(os.path.join(TEST_ROOT, "src", "utils"))
    os.makedirs(os.path.join(TEST_ROOT, "src", "core"))
    
    # Create empty files
    with open(os.path.join(TEST_ROOT, "src", "components", "Button.js"), 'w') as f: pass
    with open(os.path.join(TEST_ROOT, "src", "utils", "index.js"), 'w') as f: pass
    with open(os.path.join(TEST_ROOT, "src", "utils", "helper.ts"), 'w') as f: pass
    with open(os.path.join(TEST_ROOT, "src", "main.py"), 'w') as f: pass
    with open(os.path.join(TEST_ROOT, "src", "core", "config.py"), 'w') as f: pass
    with open(os.path.join(TEST_ROOT, "src", "core", "__init__.py"), 'w') as f: pass

def test_resolver():
    create_structure()
    resolver = DependencyResolver(TEST_ROOT)
    
    print(f"Testing Resolver on Root: {os.path.abspath(TEST_ROOT)}\n")
    
    # JS TESTS
    print("--- JS TESTS ---")
    source = os.path.abspath(os.path.join(TEST_ROOT, "src", "components", "Button.js"))
    
    # 1. Resolve ../utils (Implicit index.js)
    res = resolver.resolve(source, "../utils", "js")
    expected = os.path.abspath(os.path.join(TEST_ROOT, "src", "utils", "index.js"))
    print(f"1. '../utils' -> {res}")
    assert res == expected, f"Failed: {res} != {expected}"

    # 2. Resolve ../utils/helper (Implicit .ts extension)
    res = resolver.resolve(source, "../utils/helper", "ts")
    expected = os.path.abspath(os.path.join(TEST_ROOT, "src", "utils", "helper.ts"))
    print(f"2. '../utils/helper' -> {res}")
    assert res == expected, f"Failed: {res} != {expected}"
    
    # 3. Resolve External (react)
    res = resolver.resolve(source, "react", "js")
    print(f"3. 'react' -> {res}")
    assert res == "EXTERNAL_LIB"

    # PYTHON TESTS
    print("\n--- PYTHON TESTS ---")
    source_py = os.path.abspath(os.path.join(TEST_ROOT, "src", "main.py"))
    
    # 4. Resolve .core.config (Module import relative to root simulation)
    # Note: Our simple resolver checks relative to ROOT for non-dots
    # src.core.config
    res = resolver.resolve(source_py, "src.core.config", "python")
    expected = os.path.abspath(os.path.join(TEST_ROOT, "src", "core", "config.py"))
    print(f"4. 'src.core.config' -> {res}")
    assert res == expected, f"Failed: {res} != {expected}"

    # 5. Resolve core (Package init)
    res = resolver.resolve(source_py, "src.core", "python")
    expected = os.path.abspath(os.path.join(TEST_ROOT, "src", "core", "__init__.py"))
    print(f"5. 'src.core' -> {res}")
    assert res == expected, f"Failed: {res} != {expected}"

    # Cleanup
    shutil.rmtree(TEST_ROOT)
    print("\n✅ Verification SUCCESS. All paths resolved correctly.")

if __name__ == "__main__":
    test_resolver()
