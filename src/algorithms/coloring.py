from src.algorithms.algorithm_base import Algorithm

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
