import random

class Node:
    def __init__(self, node_id, properties=None, x=None, y=None):
        """
        node_id: Düğümün benzersiz kimliği (Örn: 1, 'A')
        properties: Sözlük yapısında özellikler {'aktiflik': 0.8, 'etkilesim': 12, ...}
        x, y: Canvas üzerindeki koordinatlar
        """
        self.id = node_id
        
        # Koordinatlar verilmemişse rastgele ata (Canvas boyutu varsayılan 800x600 gibi)
        self.x = x if x is not None else random.randint(50, 750)
        self.y = y if y is not None else random.randint(50, 550)
        
        # CSV'den gelen özelliklerin atanması [cite: 56]
        # Eğer özellik gelmezse varsayılan 0 atanır (Hata almamak için)
        props = properties if properties else {}
        self.aktiflik = float(props.get('aktiflik', 0.0))       # Özellik I
        self.etkilesim = float(props.get('etkilesim', 0))       # Özellik II
        self.baglanti_sayisi = float(props.get('baglanti_sayisi', 0)) # Özellik III
        
        # Algoritmalar için gerekli alanlar
        self.color = "gray" # Varsayılan renk (Welsh-Powell için değişecek) 
        self.neighbors = [] # Komşu düğüm ID'leri listesi
        
        # Görselleştirme için yarıçap (Sabit olabilir)
        self.radius = 20 

    def get_coordinates(self):
        """Çizim için koordinatları döndürür."""
        return (self.x, self.y)

    def set_color(self, new_color):
        """Algoritma sonrası renk değişimi için."""
        self.color = new_color

    def __repr__(self):
        """Debug yaparken konsolda nesneyi okunaklı görmek için."""
        return f"Node(ID={self.id}, A={self.aktiflik}, E={self.etkilesim}, Renk={self.color})"

    def to_dict(self):
        """Düğümü JSON veya CSV'ye kaydederken sözlüğe çevirir."""
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "aktiflik": self.aktiflik,
            "etkilesim": self.etkilesim,
            "baglanti_sayisi": self.baglanti_sayisi,
            "color": self.color
        }