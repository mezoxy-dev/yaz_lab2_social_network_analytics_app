import heapq
import math
from src.algorithms.algorithm_base import Algorithm

class DijkstraAlgorithm(Algorithm):
    def get_name(self):
        return "Dijkstra En Kısa Yol"

    def execute(self, graph, start_node_id=None, end_node_id=None):
        """
        Dijkstra Algoritması: Ağırlıklı graflarda en kısa yolu bulur.
        Priority Queue (Min-Heap) kullanır.
        """
        # Başlangıç ve Bitiş Kontrolü
        if start_node_id not in graph.nodes or end_node_id not in graph.nodes:
            print("Hata: Başlangıç veya Bitiş düğümü geçersiz.")
            return []

        # 1. Hazırlık
        # Herkesin mesafesi sonsuz, başlangıcınki 0
        distances = {node_id: float('inf') for node_id in graph.nodes}
        distances[start_node_id] = 0
        
        # Yolu geriye doğru takip etmek için (Nereden geldim?)
        predecessors = {node_id: None for node_id in graph.nodes}
        
        # Öncelik Kuyruğu: (Maliyet, DüğümID)
        pq = [(0, start_node_id)]

        while pq:
            # En düşük maliyetli düğümü seç
            current_dist, current_id = heapq.heappop(pq)

            # Hedefe vardık mı?
            if current_id == end_node_id:
                break

            # Eğer bulduğumuz yol, bildiğimizden daha kötüyse atla
            if current_dist > distances[current_id]:
                continue

            # Komşuları gez
            # graph.nodes[current_id] diyerek Node nesnesine ulaşıyoruz
            # graph.edges listesini taramak yerine komşuluk listesinden gitmek daha hızlıdır ama
            # Edge ağırlığına ihtiyacımız var.
            
            # Pratik Yöntem: Tüm kenarları gez (Küçük graflar için sorun olmaz)
            # Daha optimize yöntem: Graph sınıfında adjacency_list içinde weight tutmaktır.
            # Şimdilik Edge listesinden bulalım:
            
            for edge in graph.edges:
                neighbor_id = None
                
                # Bu kenar bizim düğümden mi çıkıyor?
                if edge.source.id == current_id:
                    neighbor_id = edge.target.id
                elif edge.target.id == current_id: # Yönsüz olduğu için tersine de bak
                    neighbor_id = edge.source.id
                
                if neighbor_id is not None:
                    # Yeni maliyet = Şu anki maliyet + Kenar Ağırlığı
                    new_dist = current_dist + edge.weight
                    
                    # Eğer daha kısa bir yol bulduysak güncelle
                    if new_dist < distances[neighbor_id]:
                        distances[neighbor_id] = new_dist
                        predecessors[neighbor_id] = current_id
                        heapq.heappush(pq, (new_dist, neighbor_id))

        # Yolu Geriye Doğru Oluştur (Backtrack)
        path = []
        step = end_node_id
        while step is not None:
            path.insert(0, step) # Başa ekle
            step = predecessors[step]
            
        # Eğer başlangıç düğümü yolda yoksa (Yol bulunamadı demektir)
        if path[0] != start_node_id:
            return []
            
        return path

class AStarAlgorithm(Algorithm):
    def get_name(self):
        return "A* (A-Star) Algoritması"

    def heuristic(self, node_a, node_b):
        """Öklid Mesafesi (Kuş uçuşu) hesaplar."""
        return math.sqrt((node_a.x - node_b.x)**2 + (node_a.y - node_b.y)**2)

    def execute(self, graph, start_node_id=None, end_node_id=None):
        if start_node_id not in graph.nodes or end_node_id not in graph.nodes:
            return []

        # G Score: Başlangıçtan buraya kadarki gerçek maliyet
        g_score = {node_id: float('inf') for node_id in graph.nodes}
        g_score[start_node_id] = 0
        
        # F Score: G Score + Heuristic (Tahmini toplam maliyet)
        f_score = {node_id: float('inf') for node_id in graph.nodes}
        f_score[start_node_id] = self.heuristic(graph.nodes[start_node_id], graph.nodes[end_node_id])
        
        predecessors = {node_id: None for node_id in graph.nodes}
        
        # Kuyrukta F Score'a göre sıralanır
        pq = [(f_score[start_node_id], start_node_id)]
        
        while pq:
            _, current_id = heapq.heappop(pq)
            
            if current_id == end_node_id:
                break
                
            for edge in graph.edges:
                neighbor_id = None
                if edge.source.id == current_id: neighbor_id = edge.target.id
                elif edge.target.id == current_id: neighbor_id = edge.source.id
                
                if neighbor_id:
                    tentative_g_score = g_score[current_id] + edge.weight
                    
                    if tentative_g_score < g_score[neighbor_id]:
                        predecessors[neighbor_id] = current_id
                        g_score[neighbor_id] = tentative_g_score
                        
                        # F = G + H
                        h = self.heuristic(graph.nodes[neighbor_id], graph.nodes[end_node_id])
                        f_score[neighbor_id] = g_score[neighbor_id] + h
                        
                        heapq.heappush(pq, (f_score[neighbor_id], neighbor_id))
                        
        # Yolu Oluştur (Dijkstra ile aynı mantık)
        path = []
        step = end_node_id
        while step is not None:
            path.insert(0, step)
            step = predecessors[step]
            
        if path[0] != start_node_id: return []
        return path