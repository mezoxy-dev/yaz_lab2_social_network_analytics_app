from src.algorithms.algorithm_base import Algorithm

class BFSAlgorithm(Algorithm):
    def get_name(self):
        return "BFS (Genişlik Öncelikli Arama)"

    def execute(self, graph, start_node_id=None, end_node_id=None):
        """
        Genişlik Öncelikli Arama (Queue Kullanır).
        Breadth First Search (BFS) uses Queue data structure.
        """
        if start_node_id not in graph.nodes:
            print(f"Hata: {start_node_id} ID'li düğüm bulunamadı.")
            return []

        visited = [] # Ziyaret sırası
        queue = [start_node_id] # FIFO (İlk giren ilk çıkar)

        while queue:
            current_id = queue.pop(0) # Kuyruğun BAŞINDAN al
            
            if current_id not in visited:
                visited.append(current_id)
                
                # Komşuları al ve kuyruğa ekle
                neighbors = graph.get_neighbors(current_id)
                for neighbor in neighbors:
                    if neighbor not in visited and neighbor not in queue:
                        queue.append(neighbor)
                        
        return visited

class DFSAlgorithm(Algorithm):
    def get_name(self):
        return "DFS (Derinlik Öncelikli Arama)"

    def execute(self, graph, start_node_id=None, end_node_id=None):
        """
        Derinlik Öncelikli Arama (Stack Kullanır).
        Depth First Search (DFS) uses Stack data structure.
        """
        if start_node_id not in graph.nodes:
            return []

        visited = []
        stack = [start_node_id] # LIFO (Son giren ilk çıkar)

        while stack:
            current_id = stack.pop() # Yığının SONUNDAN al
            
            if current_id not in visited:
                visited.append(current_id)
                
                neighbors = graph.get_neighbors(current_id)
                for neighbor in neighbors:
                    if neighbor not in visited:
                        stack.append(neighbor)
                        
        return visited