import math
import random

class SpringLayout:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.iterations = 50
        self.k = 0 # Optimal distance
        self.temperature = 0 # Initial temperature

    def calculate_layout(self, node_items, edge_items):
        """
        Fruchterman-Reingold Force-Directed Layout Algorithm.
        Nodes: List of NodeItem objects
        Edges: List of EdgeItem objects
        Returns: Dict {node_id: (x, y)}
        """
        if not node_items:
            return {}

        nodes = [item for item in node_items]
        
        # Area and optimal distance
        area = self.width * self.height
        self.k = math.sqrt(area / len(nodes)) * 0.75
        self.temperature = self.width / 10

        # Initial positions (keep visible)
        positions = {node.node_id: (node.x(), node.y()) for node in nodes}
        displacements = {node.node_id: [0.0, 0.0] for node in nodes}

        for i in range(self.iterations):
            # 1. Calculate Repulsive Forces (Nodes repel each other)
            for v in nodes:
                displacements[v.node_id] = [0.0, 0.0] # Reset
                for u in nodes:
                    if u.node_id != v.node_id:
                        delta_x = positions[v.node_id][0] - positions[u.node_id][0]
                        delta_y = positions[v.node_id][1] - positions[u.node_id][1]
                        dist = math.sqrt(delta_x**2 + delta_y**2)
                        
                        if dist < 0.1: dist = 0.1 # Avoid division by zero
                        
                        repulsive = (self.k * self.k) / dist
                        
                        displacements[v.node_id][0] += (delta_x / dist) * repulsive
                        displacements[v.node_id][1] += (delta_y / dist) * repulsive

            # 2. Calculate Attractive Forces (Edges pull nodes together)
            for edge in edge_items:
                u = edge.source
                v = edge.target
                if not u or not v: continue

                delta_x = positions[v.node_id][0] - positions[u.node_id][0]
                delta_y = positions[v.node_id][1] - positions[u.node_id][1]
                dist = math.sqrt(delta_x**2 + delta_y**2)
                
                if dist < 0.1: dist = 0.1

                attractive = (dist * dist) / self.k

                dx = (delta_x / dist) * attractive
                dy = (delta_y / dist) * attractive

                displacements[u.node_id][0] += dx
                displacements[u.node_id][1] += dy
                
                displacements[v.node_id][0] -= dx
                displacements[v.node_id][1] -= dy

            # 3. Apply Forces (Limit movement by temperature)
            for node in nodes:
                disp = displacements[node.node_id]
                dist = math.sqrt(disp[0]**2 + disp[1]**2)
                
                if dist < 0.1: dist = 0.1
                
                # Limit by temperature
                limited_dist = min(dist, self.temperature)
                
                new_x = positions[node.node_id][0] + (disp[0] / dist) * limited_dist
                new_y = positions[node.node_id][1] + (disp[1] / dist) * limited_dist
                
                # Boundary constraints (Keep inside canvas)
                border = 50
                new_x = min(self.width - border, max(border, new_x))
                new_y = min(self.height - border, max(border, new_y))
                
                positions[node.node_id] = (new_x, new_y)

            # Cool down
            self.temperature *= 0.95

        return positions
