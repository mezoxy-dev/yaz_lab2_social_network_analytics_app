import math

class Edge:
    def __init__(self, source_node, target_node):
        """
        source_node: baslangic dugumu (Node Nesnesi)
        target_node: bitis dugumu (Node Nesnesi)
        """
        self.source = source_node
        self.target = target_node
        
        # Maliyet ve Benzerlik hesaplamalari dinamik property olarak alinir
        # Ancak performans icin bir kez hesaplayip saklayabiliriz.
        self._calculate_metrics()

    @staticmethod
    def calculate_weight(props_source, props_target):
        """
        Verilen iki özellik setine göre ağırlığı hesaplar.
        Statik metod: UI tarafında anlık hesaplama için kullanılabilir.
        """
        try:
            p_s = props_source if props_source else {}
            p_t = props_target if props_target else {}
            
            val_s_akt = float(p_s.get('aktiflik', 0.0))
            val_s_etk = float(p_s.get('etkilesim', 0.0))
            val_s_bag = float(p_s.get('baglanti_sayisi', 0.0))
            
            val_t_akt = float(p_t.get('aktiflik', 0.0))
            val_t_etk = float(p_t.get('etkilesim', 0.0))
            val_t_bag = float(p_t.get('baglanti_sayisi', 0.0))
            
            d_aktiflik = val_s_akt - val_t_akt
            d_etkilesim = val_s_etk - val_t_etk
            d_baglanti = val_s_bag - val_t_bag
            
            feature_distance = math.sqrt(d_aktiflik**2 + d_etkilesim**2 + d_baglanti**2)
            
            weight = round(1 + feature_distance, 2)
            similarity = round(1 / (1 + feature_distance), 4)
            
            return weight, similarity
        except:
            return 1.0, 1.0

    def _calculate_metrics(self):
        """
        PRD 4.3 Maddesi:
        Ağırlık(i,j) = 1 / (1 + √[(Farklar)^2])
        """
        # Node özelliklerini sözlük olarak alip statik metoda verelim
        props_source = {
            'aktiflik': self.source.aktiflik,
            'etkilesim': self.source.etkilesim,
            'baglanti_sayisi': self.source.baglanti_sayisi
        }
        props_target = {
            'aktiflik': self.target.aktiflik,
            'etkilesim': self.target.etkilesim,
            'baglanti_sayisi': self.target.baglanti_sayisi
        }
        
        self._weight_cost, self._similarity_score = Edge.calculate_weight(props_source, props_target)

    @property
    def weight(self):
        """En Kısa Yol algoritmaları için 'Maliyet' (Cost) değeri."""
        return round(self._weight_cost, 2)

    @property
    def similarity(self):
        """PRD'de istenen 'Ağırlık' formülü sonucu (Benzerlik Skoru)."""
        return round(self._similarity_score, 4)

    def __repr__(self):
        return f"Edge({self.source.id}-{self.target.id}, Cost={self.weight}, Sim={self.similarity})"

    def to_dict(self):
        """Dosyaya kaydetmek icin kullanilir."""
        return {
            "source": self.source.id,
            "target": self.target.id,
            "weight": self.similarity # PRD formatına sadık kalmak için CSV'ye 'benzerlik' yazılır
        }