import networkx as nx
import json
import os
from src.core.logger import setup_logger

class GraphCore:
    """
    The Central Brain.
    Manages the knowledge graph of the repository using NetworkX.
    Nodes = Files/Functions/Classes
    Edges = Dependencies/Calls/Inheritance
    """

    def __init__(self):
        self.logger = setup_logger(name="GraphCore")
        self.graph = nx.DiGraph()

    def add_node(self, node_id, **metadata):
        """
        Adds a node with metadata.
        node_id should ideally be the absolute file path or infinite identifier.
        """
        self.graph.add_node(node_id, **metadata)
        # self.logger.debug(f"Added Node: {node_id}")

    def add_edge(self, source, target, relation_type, **metadata):
        """
        Adds a directed edge.
        relation_type: IMPORTS, DEFINES, CALLS, etc.
        """
        self.graph.add_edge(source, target, relation=relation_type, **metadata)
        # self.logger.debug(f"Added Edge: {source} --[{relation_type}]--> {target}")

    def export(self, output_dir):
        """
        Exports the graph to disk in multiple formats.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 1. JSON-Link (Web Compatible)
        json_data = nx.node_link_data(self.graph)
        json_path = os.path.join(output_dir, "knowledge_graph.json")
        try:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(json_data, f, indent=2)
            self.logger.info(f"Graph exported to JSON: {json_path}")
        except Exception as e:
            self.logger.error(f"Failed to export JSON: {e}")

        # 2. GEXF (Gephi Compatible)
        gexf_path = os.path.join(output_dir, "knowledge_graph.gexf")
        try:
            nx.write_gexf(self.graph, gexf_path)
            self.logger.info(f"Graph exported to GEXF: {gexf_path}")
        except Exception as e:
            self.logger.error(f"Failed to export GEXF: {e}")
            
        return json_path, gexf_path
