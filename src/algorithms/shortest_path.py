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
            
            # OPTIMIZE EDILDI: Graph.get_neighbors ve get_edge kullaniliyor
            neighbors = graph.get_neighbors(current_id)
            if not neighbors:
                continue
                
            for neighbor_id in neighbors:
                edge = graph.get_edge(current_id, neighbor_id)
                if not edge: continue
                
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
        """
        Sezgisel (Heuristic) Fonksiyon:
        Kullanıcının isteği üzerine 'Piksel Mesafesi' KESİNLİKLE kullanılmamaktadır.
        Bunun yerine 'Sosyal Özellik Uzayı' (Feature Space) üzerindeki Öklid mesafesi kullanılır.
        
        h(n) = sqrt((Aktiflik_fark)^2 + (Etkilesim_fark)^2 + ...)
        
        Bu değer, gerçek maliyet (Cost = 1 + h(n)) değerinden her zaman küçüktür (Admissible).
        Bu sayede A* hem doğru sonucu bulur hem de sosyal özellik olarak hedefe benzeyen
        düğümleri önceleyerek aramayı hızlandırır.
        """
        d_aktiflik = node_a.aktiflik - node_b.aktiflik
        d_etkilesim = node_a.etkilesim - node_b.etkilesim
        d_baglanti = node_a.baglanti_sayisi - node_b.baglanti_sayisi
        
        # Özellik uzayındaki direkt kuş uçuşu mesafe
        return math.sqrt(d_aktiflik**2 + d_etkilesim**2 + d_baglanti**2)

    def execute(self, graph, start_node_id=None, end_node_id=None):
        if start_node_id not in graph.nodes or end_node_id not in graph.nodes:
            return []

        # G Score: Başlangıçtan buraya kadarki gerçek maliyet
        g_score = {node_id: float('inf') for node_id in graph.nodes}
        g_score[start_node_id] = 0
        
        # F Score: G Score + Heuristic
        f_score = {node_id: float('inf') for node_id in graph.nodes}
        f_score[start_node_id] = self.heuristic(graph.nodes[start_node_id], graph.nodes[end_node_id])
        
        predecessors = {node_id: None for node_id in graph.nodes}
        
        # Kuyruk F Score'a göre sıralı
        pq = [(f_score[start_node_id], start_node_id)]
        
        visited = set() # Optimize: Aynı düğümü tekrar tekrar işlememek için

        while pq:
            _, current_id = heapq.heappop(pq)
            
            if current_id == end_node_id:
                break
            
            # Daha kötü bir yoldan tekrar geldiysek atla
            # (Set kullanarak visited kontrolü veya g_score kontrolü yapılabilir)
            
            neighbors = graph.get_neighbors(current_id)
            if not neighbors: continue
                
            for neighbor_id in neighbors:
                edge = graph.get_edge(current_id, neighbor_id)
                if not edge: continue

                # DİKKAT: edge.weight artık 'Cost' (Maliyet) veriyor.
                # PRD'deki 'Similarity' (1/1+diff) değil.
                tentative_g_score = g_score[current_id] + edge.weight
                
                if tentative_g_score < g_score[neighbor_id]:
                    predecessors[neighbor_id] = current_id
                    g_score[neighbor_id] = tentative_g_score
                    
                    h = self.heuristic(graph.nodes[neighbor_id], graph.nodes[end_node_id])
                    f_score[neighbor_id] = g_score[neighbor_id] + h
                    
                    heapq.heappush(pq, (f_score[neighbor_id], neighbor_id))
                        
        # Yolu Geriye İzle
        path = []
        step = end_node_id
        while step is not None:
            path.insert(0, step)
            step = predecessors[step]
            
        if path[0] != start_node_id: return []
        return path