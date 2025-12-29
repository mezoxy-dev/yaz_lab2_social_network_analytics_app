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

class WelshPowellAlgorithm(Algorithm):
    def get_name(self):
        return "Welsh-Powell Renklendirme"

    def execute(self, graph, start_node_id=None, end_node_id=None):
        """
        Komşu düğümleri farklı renklere boyar.
        Döküman Madde 3.2: Ayrık topluluktaki komşu düğümler farklı renklerde boyanmalı. 
        """
        # 1. Düğümleri derecelerine göre azalan sırada sırala
        sorted_nodes = sorted(
            graph.nodes.values(), 
            key=lambda node: len(graph.get_neighbors(node.id)), 
            reverse=True
        )
        
        # Renk Paleti (Yeterince renk tanımlayalım)
        colors = [
            "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF", 
            "#FFA500", "#800080", "#008080", "#FFC0CB", "#800000", "#008000"
        ]
        
        # Herkesin rengini sıfırla (None yap veya geçici bir sözlükte tut)
        node_colors = {} # {node_id: renk_kodu}
        
        color_index = 0
        
        # 2. Algoritma Döngüsü
        # Renk atanmamış düğüm kaldığı sürece dön
        while len(node_colors) < len(sorted_nodes):
            current_color = colors[color_index % len(colors)] # Renk seç (yetersiz kalırsa başa dön)
            
            # Bu turda boyananlar (Komşuluk kontrolü için)
            colored_in_this_round = []
            
            for node in sorted_nodes:
                # Zaten boyandıysa geç
                if node.id in node_colors:
                    continue
                
                # Şu anki rengi alan komşusu var mı?
                has_neighbor_same_color = False
                neighbors = graph.get_neighbors(node.id)
                
                for neighbor_id in neighbors:
                    if neighbor_id in colored_in_this_round:
                        has_neighbor_same_color = True
                        break
                
                # Eğer komşularda bu renk yoksa, boya!
                if not has_neighbor_same_color:
                    node_colors[node.id] = current_color
                    colored_in_this_round.append(node.id)
            
            # Bir sonraki renge geç
            color_index += 1
            
        # Sonuç: Node ID ve Renk eşleşmesi
        return node_colors

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