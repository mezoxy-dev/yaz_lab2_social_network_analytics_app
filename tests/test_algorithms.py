import sys
import os

# Mevcut dosyanın yolunu al (tests/ klasörü)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Bir üst klasöre çık (Ana proje klasörü)
project_root = os.path.dirname(current_dir)

# Python'un arama yollarına ana klasörü ekle
sys.path.append(project_root)

# ARTIK IMPORT YAPABİLİRSİN
from src.model.node import Node
from src.model.edge import Edge

# Dökümandaki Örnek Tablodaki Veriler (Madde 4.3 Örnek Yapı)
# Düğüm 1: Aktiflik=0.8, Etkileşim=12, Bağlantı=3
n1 = Node(1, properties={'aktiflik': 0.8, 'etkilesim': 12, 'baglanti_sayisi': 3})

# Düğüm 2: Aktiflik=0.4, Etkileşim=5, Bağlantı=2
n2 = Node(2, properties={'aktiflik': 0.4, 'etkilesim': 5, 'baglanti_sayisi': 2})

# Kenar oluştur
edge = Edge(n1, n2)

print(edge)
# Beklenen Hesap:
# Farklar: (0.4)^2 + (7)^2 + (1)^2 
# Kareler: 0.16 + 49 + 1 = 50.16
# Karekök(50.16) ≈ 7.08
# Sonuç + 1 = 8.08