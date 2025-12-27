import math

class Edge:
    def __init__(self, source_node, target_node):
        """
        source_node: Başlangıç Düğümü (Node Nesnesi)
        target_node: Bitiş Düğümü (Node Nesnesi)
        """
        self.source = source_node
        self.target = target_node
        
        # Nesne oluşturulurken ağırlığı otomatik hesapla
        self.weight = self.calculate_weight()

    def calculate_weight(self):
        """
        Proje Dökümanı Madde 4.3'teki formülü uygular[cite: 59].
        Formül: 1 + sqrt((AktiflikFarki)^2 + (EtkilesimFarki)^2 + (BaglantiFarki)^2)
        """
        # 1. Node nesnelerinin içindeki özellikleri kullanarak farkları bul
        # Senin Node sınıfındaki isimlerle birebir aynı olmalı:
        delta_aktiflik = self.source.aktiflik - self.target.aktiflik
        delta_etkilesim = self.source.etkilesim - self.target.etkilesim
        delta_baglanti = self.source.baglanti_sayisi - self.target.baglanti_sayisi

        # 2. Kareler Toplamını Hesapla
        kareler_toplami = (delta_aktiflik ** 2) + \
                          (delta_etkilesim ** 2) + \
                          (delta_baglanti ** 2)

        # 3. Karekök al ve 1 ekle [cite: 59]
        weight = 1 + math.sqrt(kareler_toplami)
        
        # Sonucu 2 ondalık basamağa yuvarla (Okunabilirlik için)
        return round(weight, 2)

    def __repr__(self):
        """Debug çıktısı: Hangi düğümler bağlı ve ağırlık ne?"""
        return f"Edge({self.source.id} <-> {self.target.id}, W={self.weight})"

    def to_dict(self):
        """Dosyaya kaydederken kullanılır."""
        return {
            "source": self.source.id,
            "target": self.target.id,
            "weight": self.weight
        }