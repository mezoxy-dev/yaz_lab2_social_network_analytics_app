# GÖREV: Üye B - Veri Yapıları
from collections import defaultdict
from .node import Node
from .edge import Edge

class Graph:
    def __init__(self):
        self.nodes = {}  # id -> Node
        self.edges = []  # List[Edge]
        self.adjacency = defaultdict(list) # id -> List[Edge]

    def add_node(self, node_id, data=None):
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(node_id, data)

    def add_edge(self, source_id, target_id, weight=1.0):
        self.add_node(source_id)
        self.add_node(target_id)
        edge = Edge(source_id, target_id, weight)
        self.edges.append(edge)
        self.adjacency[source_id].append(edge)
