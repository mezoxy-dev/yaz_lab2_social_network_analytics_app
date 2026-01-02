from abc import ABC, abstractmethod
import csv
import os
from src.model.node import Node

#file manager arayüzü
class IFileManager(ABC):
    @abstractmethod
    def load(self, file_path, graph):
        """Dosyayı okur ve graph nesnesini doldurur."""
        pass

    @abstractmethod
    def save(self, file_path, graph):
        """Graph nesnesini dosyaya yazar."""
        pass

#csv file manager
class CSVFileManager(IFileManager):
    def load(self, file_path, graph):
        """
        Verilen CSV dosyasını okur ve grafı oluşturur.
        Dökümandaki format: DugumId, Aktiflik, Etkilesim, Baglanti, Komsular
        """
        if not os.path.exists(file_path):
            print(f"Hata: Dosya bulunamadı -> {file_path}")
            return False

        print(f"Dosya okunuyor: {file_path}")
        
        # geçici hafıza: gelen verileri tutma
        raw_data = []

        try:
            with open(file_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                #1. tur - Node'ları olusturma
                for row in reader:
                    # csv sütun isimlerini temizle ve boşlukları sil
                    row = {k.strip(): v.strip() for k, v in row.items()}
                    
                    try:
                        node_id = int(row['DugumId'])
                        
                        # ozellikleri hazırla
                        # özellikleri hazırla
                        props = {
                            'aktiflik': float(row.get('Ozellik_I (Aktiflik)', 0)),
                            'etkilesim': float(row.get('Ozellik_II (Etkileşim)', 0)),
                            'baglanti_sayisi': float(row.get('Ozellik_III (Bagl. Sayisi)', 0))
                        }
                        
                        # İsmi al (Yoksa opsiyonel)
                        name = row.get('Isim')
                        
                        # düğümü oluştur ve ekle
                        new_node = Node(node_id, properties=props, name=name)
                        graph.add_node(new_node)
                        
                        # ham veriyi 2. tur için sakla
                        raw_data.append(row)
                        
                    except ValueError as e:
                        print(f"Satır okuma hatası: {e} - Satır: {row}")
                        continue

            #2. tur - edge'leri olusturma 
            for row in raw_data:
                source_id = int(row['DugumId'])
                komsular_str = row['Komsular'] # Örn: "2,4,5"
                
                if komsular_str:
                    # virgülle ayır ve her biri için kenar oluştur
                    komsu_ids = komsular_str.split(',')
                    for k_id in komsu_ids:
                        try:
                            target_id = int(k_id.strip())
                            # self-loop engelleme
                            if source_id != target_id:
                                graph.add_edge(source_id, target_id)
                        except ValueError:
                            pass

            print(f"Yükleme Başarılı! Toplam Node: {len(graph.nodes)}, Toplam Edge: {len(graph.edges)}")
            return True

        except Exception as e:
            print(f"Genel Hata: {e}")
            return False

    def save(self, file_path, graph):
        """
        Graph nesnesini CSV formatında kaydeder.
        Format: DugumId, Ozellik_I (Aktiflik), Ozellik_II (Etkileşim), Ozellik_III (Bagl. Sayisi), Komsular
        """
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as f:
                fieldnames = ['DugumId', 'Isim', 'Ozellik_I (Aktiflik)', 'Ozellik_II (Etkileşim)', 'Ozellik_III (Bagl. Sayisi)', 'Komsular']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                writer.writeheader()
                
                for node_id, node in graph.nodes.items():
                    # Komşuları bul (Graph.adjacency_list veya node.neighbors)
                    # Graph.get_neighbors metodu güvenlidir
                    neighbors = graph.get_neighbors(node_id)
                    neighbors_str = ",".join(map(str, neighbors))
                    
                    writer.writerow({
                        'DugumId': node_id,
                        'Isim': node.name,
                        'Ozellik_I (Aktiflik)': node.aktiflik,
                        'Ozellik_II (Etkileşim)': node.etkilesim,
                        'Ozellik_III (Bagl. Sayisi)': node.baglanti_sayisi,
                        'Komsular': neighbors_str
                    })
            
            print(f"Kaydetme başarılı: {file_path}")
            return True
            
        except Exception as e:
            print(f"Kaydetme Hatası: {e}")
            return False
#yeni dosya yöneticisi eklenmek istenirse buraya eklenebilir
