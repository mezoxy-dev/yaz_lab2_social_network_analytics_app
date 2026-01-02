import random

class Node:
    def __init__(self, node_id: int, properties: dict = None, x: int = None, y: int = None, name: str = None):
        """
        Sosyal Ağ Analizi için Düğüm (Node) Sınıfı.
        
        Args:
            node_id (int): Düğümün benzersiz kimliği.
            properties (dict): 'aktiflik', 'etkilesim', 'baglanti_sayisi' özelliklerini içeren sözlük.
            x (int, optional): Canvas üzerindeki X koordinatı. 
            y (int, optional): Canvas üzerindeki Y koordinatı.
            name (str, optional): Düğümün görünen ismi.
        """
        self.id = node_id
        self.name = name if name else str(node_id) # İsim yoksa ID kullan
        
        # Koordinatlar verilmemişse rastgele ata
        self.x = x if x is not None else random.randint(50, 750)
        self.y = y if y is not None else random.randint(50, 550)
        
        # Özelliklerin güvenli bir şekilde atanması
        props = properties if properties else {}
        try:
            self.aktiflik = float(props.get('aktiflik', 0.0))
            self.etkilesim = float(props.get('etkilesim', 0.0))
            self.baglanti_sayisi = float(props.get('baglanti_sayisi', 0.0))
        except (ValueError, TypeError):
            # Hatalı veri durumunda varsayılan değerler
            self.aktiflik = 0.0
            self.etkilesim = 0.0
            self.baglanti_sayisi = 0.0
        
        # Algoritmalar için gerekli alanlar
        self.color = "gray" # Görselleştirme rengi
        self.neighbors = [] # Komşu düğüm ID'leri
        self.radius = 20 # Çizim yarıçapı

    def get_coordinates(self):
        """(x, y) demeti döndürür."""
        return (self.x, self.y)

    def set_color(self, new_color):
        self.color = new_color

    def __repr__(self):
        return f"Node(ID={self.id}, A={self.aktiflik}, E={self.etkilesim}, Neighbors={len(self.neighbors)})"

    def to_dict(self):
        """Dugumu JSON veya CSV'ye kaydetmek icin sözlüğe cevirir."""
        return {
            "id": self.id,
            "name": self.name,
            "x": self.x,
            "y": self.y,
            "aktiflik": self.aktiflik,
            "etkilesim": self.etkilesim,
            "baglanti_sayisi": self.baglanti_sayisi,
            "color": self.color
        }