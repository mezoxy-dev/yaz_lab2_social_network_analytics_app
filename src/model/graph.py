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
        
        # Düğüm nesnelerinin kendi içindeki listelerini de güncelle
        source_node.neighbors.append(target_id)
        target_node.neighbors.append(source_id)

    def load_from_csv(self, file_path):
        """
        Verilen CSV dosyasını okur ve grafı oluşturur.
        Dökümandaki format: DugumId, Aktiflik, Etkilesim, Baglanti, Komsular
        """
        if not os.path.exists(file_path):
            print(f"Hata: Dosya bulunamadı -> {file_path}")
            return False

        print(f"Dosya okunuyor: {file_path}")
        
        # Geçici hafıza: Bağlantıları 2. turda kurmak için veriyi tutalım
        raw_data = []

        try:
            with open(file_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                # --- 1. TUR: Sadece Düğümleri (Node) Yarat ---
                for row in reader:
                    # CSV sütun isimlerini temizle (boşlukları sil)
                    row = {k.strip(): v.strip() for k, v in row.items()}
                    
                    try:
                        node_id = int(row['DugumId'])
                        
                        # Özellikleri hazırla
                        props = {
                            'aktiflik': float(row['Ozellik_I (Aktiflik)']),
                            'etkilesim': float(row['Ozellik_II (Etkileşim)']),
                            'baglanti_sayisi': float(row['Ozellik_III (Bagl. Sayisi)'])
                        }
                        
                        # Düğümü oluştur ve ekle
                        new_node = Node(node_id, properties=props)
                        self.add_node(new_node)
                        
                        # Ham veriyi 2. tur için sakla
                        raw_data.append(row)
                        
                    except ValueError as e:
                        print(f"Satır okuma hatası: {e} - Satır: {row}")
                        continue

            # --- 2. TUR: Bağlantıları (Edge) Kur ---
            for row in raw_data:
                source_id = int(row['DugumId'])
                komsular_str = row['Komsular'] # Örn: "2,4,5"
                
                if komsular_str:
                    # Virgülle ayır ve her biri için kenar oluştur
                    komsu_ids = komsular_str.split(',')
                    for k_id in komsu_ids:
                        try:
                            target_id = int(k_id.strip())
                            # Kendine dönen bağları (Self-loop) engelle (Döküman Madde 4.5)
                            if source_id != target_id:
                                self.add_edge(source_id, target_id)
                        except ValueError:
                            pass

            print(f"✅ Yükleme Başarılı! Toplam Node: {len(self.nodes)}, Toplam Edge: {len(self.edges)}")
            return True

        except Exception as e:
            print(f"Genel Hata: {e}")
            return False

    def clear(self):
        """Grafı temizler (Yeni dosya için)."""
        self.nodes.clear()
        self.edges.clear()
        self.adjacency_list.clear()