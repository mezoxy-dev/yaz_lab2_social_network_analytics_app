from abc import ABC, abstractmethod
import csv
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
                        props = {
                            'aktiflik': float(row['Ozellik_I (Aktiflik)']),
                            'etkilesim': float(row['Ozellik_II (Etkileşim)']),
                            'baglanti_sayisi': float(row['Ozellik_III (Bagl. Sayisi)'])
                        }
                        
                        # düğümü oluştur ve ekle
                        new_node = Node(node_id, properties=props)
                        self.add_node(new_node)
                        
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
                                self.add_edge(source_id, target_id)
                        except ValueError:
                            pass

            print(f"Yükleme Başarılı! Toplam Node: {len(self.nodes)}, Toplam Edge: {len(self.edges)}")
            return True

        except Exception as e:
            print(f"Genel Hata: {e}")
            return False

    def save(self, file_path, graph):
        # kaydetme mantığı
        pass
#yeni dosya yöneticisi eklenmek istenirse buraya eklenebilir
