from src.algorithms.algorithm_base import Algorithm
import random

class DegreeCentralityAlgorithm(Algorithm):
    def get_name(self):
        return "Degree Centrality (En Etkili Düğümler)"

    def execute(self, graph, start_node_id=None, end_node_id=None):
        """
        Düğüm derecelerini (komşu sayılarını) hesaplar ve sıralar.
        Döküman Madde 3.2: En yüksek dereceli 5 düğümün gösterilmesi. 
        """
        # Liste: (Node ID, Derece Sayısı)
        centrality_scores = []
        
        for node_id, node in graph.nodes.items():
            degree = len(graph.get_neighbors(node_id))
            centrality_scores.append((node_id, degree))
        
        # Dereceye göre tersten (büyükten küçüğe) sırala
        centrality_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Tüm listeyi döndür (UI tarafında ilk 5'i alacağız)
        return centrality_scores



class ConnectedComponentsAlgorithm(Algorithm):
    def get_name(self):
        return "Bağlı Bileşenler (Topluluk Analizi)"

    def execute(self, graph, start_node_id=None, end_node_id=None):
        """
        Graftaki tüm ayrık toplulukları (Connected Components) bulur.
        Return: [[1, 2, 3], [4, 5]] şeklinde liste içinde liste döndürür.
        """
        visited = set()
        communities = []

        # Grafın tüm düğümlerini tek tek kontrol et
        for node_id in graph.nodes:
            if node_id not in visited:
                # Yeni bir topluluk keşfettik!
                component = []
                
                # Bu düğümden başlayarak ulaşılabilen herkesi bul (Basit BFS)
                queue = [node_id]
                visited.add(node_id)
                
                while queue:
                    current = queue.pop(0)
                    component.append(current)
                    
                    # Komşulara bak
                    neighbors = graph.get_neighbors(current)
                    for neighbor in neighbors:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
                
                # Bulunan grubu listeye ekle
                communities.append(component)
        
        return communities