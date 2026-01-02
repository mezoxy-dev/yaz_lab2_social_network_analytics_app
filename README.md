# Sosyal Ağ Analizi ve Görselleştirme Aracı

Bu proje, sosyal ağları modellemek, görselleştirmek ve çeşitli graf teorisi algoritmaları ile analiz etmek için geliştirilmiş kapsamlı bir masaüstü uygulamasıdır. Python ve PyQt5 kullanılarak geliştirilmiştir.

## 🚀 Özellikler

Uygulama, graf verileri üzerinde aşağıdaki temel yetenekleri sunar:

### 1. Graf Görselleştirme ve Düzenleme
- **İnteraktif Canvas:** Düğümleri (kullanıcılar) ve kenarları (ilişkiler) görsel olarak oluşturun.
- **Sürükle & Bırak:** Düğümleri canvas üzerinde serbestçe hareket ettirin.
- **Özelleştirilebilir Özellikler:** Her bir düğüm için *Aktiflik*, *Etkileşim*, *Bağlantı Sayısı* gibi sosyal metrikleri tanımlayın.

### 2. Graf Algoritmaları
Proje, ağ üzerindeki yolları ve yapıları analiz etmek için güçlü algoritmalar içerir:

- **Dijkstra Algoritması:** Düğümler arasındaki en kısa yolu kenar ağırlıklarına göre hesaplar.
- **A* (A-Star) Algoritması:** Sosyal metrikleri (benzerlik, etkileşim vb.) sezgisel (heuristic) olarak kullanarak hedefe en uygun yolu bulur.
- **BFS (Genişlik Öncelikli Arama):** Grafı katman katman gezerek ağın yapısını keşfeder.
- **DFS (Derinlik Öncelikli Arama):** Grafın derinliklerine inerek uç noktaları keşfeder.

### 3. Ağ Analizi
Ağın topolojisi hakkında bilgi edinmek için analiz araçları:
- **Degree Centrality (Derece Merkeziliği):** Ağdaki en popüler veya en etkili düğümleri (kullanıcıları) belirler.
- **Connected Components (Bağlı Bileşenler):** Ağ içindeki ayrık toplulukları ve grupları tespit eder.

## 🛠️ Kurulum

Projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları izleyin:

1. **Gereksinimleri Yükleyin:**
   Python kurulu olduğundan emin olun ve gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

2. **Uygulamayı Başlatın:**
   Ana dizindeki `main.py` dosyasını çalıştırarak arayüzü başlatın:
   ```bash
   python main.py
   ```

## 📋 Gereksinimler

Proje aşağıdaki temel kütüphaneleri kullanır (detaylar `requirements.txt` dosyasındadır):
- **Python 3.x**
- **PyQt5** (Kullanıcı Arayüzü)
- **NetworkX** (Graf Veri Yapısı ve İşlemleri)
- **Pandas** (Veri İşleme)
- **Matplotlib** (Görselleştirme Altyapısı)

## 📁 Proje Yapısı

- `src/algorithms/`: BFS, DFS, Dijkstra, A* ve analiz algoritmalarının implementasyonları.
- `src/ui/`: Arayüz bileşenleri, canvas çizimi ve diyalog pencereleri.
- `src/model/`: Veri modelleri (Node, Edge, Graph).
- `data/`: Örnek veri setleri ve kaydedilen graflar.
