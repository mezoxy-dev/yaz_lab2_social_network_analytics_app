# GÖREV: Üye B - Veri Yapıları

class Edge:
    def __init__(self, source_id, target_id, weight=1.0):
        self.source_id = source_id
        self.target_id = target_id
        self.weight = weight

    def __repr__(self):
        return f"Edge({self.source_id} -> {self.target_id}, w={self.weight})"
