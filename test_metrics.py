from src.engines.metrics import MetricsEngine
import os

DUMMY_PY = "dummy_complexity.py"

CODE = """
def good_function(a, b):
    # Complexity: 1
    return a + b

def bad_function(x):
    # Complexity: 1 + 5 ifs + 1 while = 7? Let's check logic.
    # Actually logic captures recursive/nested structure?
    # Let's make a MONSTER. 
    # Threshold is 10. We need > 10.
    
    if x > 0:           # +1
        print("pos")
    
    if x % 2 == 0:      # +1
        print("even")
    elif x % 3 == 0:    # +1 (if part of elif chain in AST is basically If)
        print("div3")
        
    for i in range(10): # +1
        if i == 5:      # +1
            break
            
    while True:         # +1
        try:            # +0 (Try doesn't count in some definitions, but Handler does)
            x += 1
        except Exception: # +1
            break
            
    if x > 100 and x < 1000: # +1 for If, +1 for And = +2
        pass
        
    if x == 1 or x == 2 or x == 3: # +1 for If, +2 for Ors = +3
        pass

    return x
"""

def test_metrics():
    print(f"Creating {DUMMY_PY}...")
    with open(DUMMY_PY, "w") as f:
        f.write(CODE)
        
    print("Running MetricsEngine...")
    engine = MetricsEngine(high_risk_threshold=5, critical_threshold=10) # Lowered for test
    
    metrics = engine.analyze(DUMMY_PY)
    
    if not metrics:
        print("FAIL: No metrics returned")
        return

    print("METRICS REPORT:")
    for func in metrics['functions']:
        print(f" - Function: {func['name']:<15} Complexity: {func['complexity']:<3} Status: {func['status']}")

    # Validation
    func_map = {f['name']: f for f in metrics['functions']}
    
    good = func_map.get('good_function')
    bad = func_map.get('bad_function')
    
    if good['complexity'] == 1:
        print("✅ GOOD CODE: Correctly scored (1)")
    else:
        print(f"❌ GOOD CODE: Unexpected score {good['complexity']}")

    # Let's count 'bad_function' expected:
    # Base: 1
    # If x>0: +1
    # If x%2: +1
    # If x%3 (elif): +1
    # For: +1
    # If i==5: +1
    # While: +1
    # Except: +1
    # If x>100: +1
    # And: +1
    # If x==1: +1
    # Or: +2
    # Total: 1 + 1+1+1+1+1+1+1+1+1+1+2 = 13
    
    if bad['complexity'] >= 10:
        print(f"✅ BAD CODE: Correctly scored ({bad['complexity']}) and flagged as {bad['status']}")
    else:
        print(f"❌ BAD CODE: Too low ({bad['complexity']})")

    # Cleanup
    os.remove(DUMMY_PY)
    print("Cleanup complete.")

if __name__ == "__main__":
    test_metrics()
