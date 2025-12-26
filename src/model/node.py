# GÖREV: Üye B - Veri Yapıları

class Node:
    def __init__(self, node_id, data=None):
        self.node_id = node_id
        self.data = data or {}

    def __repr__(self):
        return f"Node({self.node_id})"
