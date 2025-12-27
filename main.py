import os
from src.model.graph import Graph

def main():
    # 1. Graf Yöneticisini Başlat
    graph = Graph()
    
    # 2. Dosya Yolunu Bul (data klasöründe olduğunu varsayıyoruz)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, 'data', 'social_network.csv')
    
    # 3. Yüklemeyi Dene
    basarili = graph.load_from_csv(csv_path)
    
    if basarili:
        print("\n--- TEST RAPORU ---")
        # Düğümleri listele
        print("Düğümler:")
        for node_id, node in graph.nodes.items():
            print(f"  {node}")
            
        # Kenarları listele (Ağırlıkları kontrol et)
        print("\nKenarlar (Ve Otomatik Hesaplanan Ağırlıklar):")
        for edge in graph.edges:
            print(f"  {edge}")
            
    else:
        print("CSV dosyası yüklenemedi! Dosya yolunu ve ismini kontrol et.")

if __name__ == "__main__":
    main()