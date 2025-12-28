import csv
import os
from src.model.node import Node
from src.model.edge import Edge

class Graph:
    def __init__(self):
        # Düğümleri ID ile hızlı bulmak için sözlük {id: NodeObjesi}
        self.nodes = {} 
        # Tüm kenarların listesi
        self.edges = [] 
        # Algoritmalar için komşuluk listesi {id: [id1, id2]}
        self.adjacency_list = {} 

    def add_node(self, node):
        """Graf yapısına tek bir düğüm ekler."""
        if node.id not in self.nodes:
            self.nodes[node.id] = node
            self.adjacency_list[node.id] = []

    def add_edge(self, source_id, target_id):
        """
        İki ID arasındaki bağlantıyı kurar.
        Edge nesnesi oluşturulurken ağırlık otomatik hesaplanır.
        """
        # 1. Düğümler var mı kontrol et
        if source_id not in self.nodes or target_id not in self.nodes:
            return # Düğüm yoksa işlem yapma
        
        # 2. Daha önce eklenmiş mi? (Tekrarlı kenar kontrolü)
        if target_id in self.adjacency_list[source_id]:
            return

        # 3. Nesneleri al ve Edge oluştur
        source_node = self.nodes[source_id]
        target_node = self.nodes[target_id]
        new_edge = Edge(source_node, target_node)

        # 4. Kayıtları güncelle
        self.edges.append(new_edge)
        
        # Yönsüz graf olduğu için karşılıklı ekliyoruz
        self.adjacency_list[source_id].append(target_id)
        self.adjacency_list[target_id].append(source_id)
        
        # Dugum nesnelerinin kendi icindeki listelerini de guncelle
        source_node.neighbors.append(target_id)
        target_node.neighbors.append(source_id)

    def clear(self):
        """Grafı temizler (Yeni dosya için)."""
        self.nodes.clear()
        self.edges.clear()
        self.adjacency_list.clear()