from src.core.graph_builder import GraphCore
import os
import json
import shutil

TEST_OUTPUT = "test_graph_output"

def test_graph_builder():
    if os.path.exists(TEST_OUTPUT):
        shutil.rmtree(TEST_OUTPUT)
        
    print("Initializing GraphCore...")
    brain = GraphCore()
    
    # Create Nodes
    brain.add_node("main.py", type="file", language="Python", loc=100)
    brain.add_node("utils.py", type="file", language="Python", loc=50)
    brain.add_node("requests", type="library", external=True)
    
    # Create Edges
    brain.add_edge("main.py", "utils.py", "IMPORTS")
    brain.add_edge("utils.py", "requests", "DEPENDS_ON")
    
    print("Exporting Graph...")
    json_path, gexf_path = brain.export(TEST_OUTPUT)
    
    # Verify JSON
    if os.path.exists(json_path):
        print(f"✅ JSON Created: {json_path}")
        with open(json_path, 'r') as f:
            data = json.load(f)
            nodes = len(data['nodes'])
            # Check for keys (NetworkX might return 'links' or 'edges')
            links_key = 'links' if 'links' in data else 'edges'
            nodes = len(data['nodes'])
            links = len(data[links_key])
            print(f"   Nodes: {nodes} (Expected 3)")
            print(f"   Links: {links} (Expected 2)")
            
            if nodes == 3 and links == 2:
                print("   Structure VALID.")
            else:
                print("   ❌ Structure INVALID.")
    else:
        print("❌ JSON Export FAILED")
        
    # Verify GEXF
    if os.path.exists(gexf_path):
        print(f"✅ GEXF Created: {gexf_path}")
    else:
        print("❌ GEXF Export FAILED")

    # Cleanup
    shutil.rmtree(TEST_OUTPUT)
    print("Cleanup complete.")

if __name__ == "__main__":
    test_graph_builder()
