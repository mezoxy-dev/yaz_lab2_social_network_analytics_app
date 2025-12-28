import math

class Edge:
    def __init__(self, source_node, target_node):
        """
        source_node: baslangic dugumu (Node Nesnesi)
        target_node: bitis dugumu (Node Nesnesi)
        """
        self.source = source_node
        self.target = target_node
        
        # Nesne oluşturulurken ağırlığı otomatik hesapla
        self.weight = self.calculate_weight()

    def calculate_weight(self):
        """
        Formül: 1 + sqrt((AktiflikFarki)^2 + (EtkilesimFarki)^2 + (BaglantiFarki)^2)
        """
        # 1. Node nesnelerinin içindeki özellikleri kullanarak farkları bul
        # Node sınıfındaki isimlerle birebir aynı olmalı:
        delta_aktiflik = self.source.aktiflik - self.target.aktiflik
        delta_etkilesim = self.source.etkilesim - self.target.etkilesim
        delta_baglanti = self.source.baglanti_sayisi - self.target.baglanti_sayisi

        # 2. Kareler Toplamını Hesapla
        kareler_toplami = (delta_aktiflik ** 2) + \
                          (delta_etkilesim ** 2) + \
                          (delta_baglanti ** 2)

        # 3. Karekök al ve 1 ekle
        weight = 1 + math.sqrt(kareler_toplami)
        
        # Sonucu 2 ondalık basamağa yuvarla (Okunabilirlik icin)
        return round(weight, 2)

    def __repr__(self):
        """Debug ciktisi: Hangi dugumler bagli ve agirlik ne?"""
        return f"Edge({self.source.id} <-> {self.target.id}, W={self.weight})"

    def to_dict(self):
        """Dosyaya kaydetmek icin kullanilir."""
        return {
            "source": self.source.id,
            "target": self.target.id,
            "weight": self.weight
        }