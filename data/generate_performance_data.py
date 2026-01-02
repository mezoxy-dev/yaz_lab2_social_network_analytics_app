
import csv
import random
import os

def generate_performance_data(filename="performance_social_network.csv"):
    nodes = []
    edges = []
    
    # SENARYO V3 (The Trap):
    # Dijkstra "Ucuz" yolu sever. A* "Hedefe Giden" yolu sever.
    # Biz öyle bir tuzak kuracağız ki;
    # - Hedefe giden yol PAHALI olacak (Cost ~ 21).
    # - Hedefe gitmeyen (Tuzak) yollar UCUZ olacak (Cost ~ 2).
    #
    # Sonuç:
    # Dijkstra ucuz diye tuzaklara doluşacak.
    # A* pahalı da olsa doğru yönü seçecek çünkü Heuristic (Mesafe) azalacak.
    
    # Hedef Noktası: Aktiflik = 1000, Etkileşim = 0
    target_val = 1000.0
    
    # 1. Start Node
    nodes.append({
        "id": 1,
        "name": "Start",
        "aktiflik": 0.0,
        "etkilesim": 0.0,
        "baglanti_sayisi": 0.0, # Etkisiz eleman olması için küçük tutuyoruz veya sabit
        "type": "start"
    })
    
    # 2. Optimal Path (The Hardware - Pahalı Otoban)
    # 50 Adım. Her adımda Aktiflik +20 artacak.
    # Özellik Farkı (Feature Dist) = 20.
    # Edge Weight = 1 + 20 = 21.
    
    path_len = 50
    current_node = 1 # Start
    final_node = None
    
    for i in range(path_len):
        new_id = len(nodes) + 1
        val = (i + 1) * 20.0 # 20, 40, 60 ... 1000
        
        nodes.append({
            "id": new_id,
            "name": f"Path_{i+1}",
            "aktiflik": val,
            "etkilesim": 0.0,
            "baglanti_sayisi": 0.0,
            "type": "path"
        })
        
        edges.append((current_node, new_id))
        current_node = new_id
        
    final_node = current_node # End Node (ID: 51)
    
    # 3. Tuzak Ağı (The Cheap Swamp - Ucuz Bataklık)
    # 2000 Düğüm. 
    # Bunlar Start Node'dan başlayarak "Etkileşim" ekseninde (yanlara) yayılacak.
    # Adım başı değişim az olacak (Örn: +1). 
    # Feature Dist = 1. Edge Weight = 1 + 1 = 2.
    #
    # Dijkstra START noktasında bakacak:
    # A) Path_1 (Maliyet 21).
    # B) Decoy_1 (Maliyet 2).
    # Dijkstra B'yi seçecek. Sonra B'den C'ye (2)... Maliyeti 21 olana kadar 10 adım atabilir.
    # Bu yüzden binlerce düğümü gezecek.
    
    num_decoys = 2000
    decoy_start_index = len(nodes)
    
    # Tuzak ağacını özyinelemesiz manuel kuralım
    # İlk decoylar Start'a bağlı
    # Sonrakiler rastgele eski decoylara bağlı
    
    # Decoy ID'lerini tutalım
    decoy_ids = []
    
    for i in range(num_decoys):
        node_id = len(nodes) + 1
        
        # Kime bağlanacak?
        if i < 5:
            parent = 1 # Start node
        else:
            # Rastgele bir önceki decoy (Ağaç yapısı)
            # Ama çok eskiye gitmesin ki derinleşsin bataklık
            window = 50 
            start_idx = max(0, len(decoy_ids) - window)
            parent = decoy_ids[random.randint(start_idx, len(decoy_ids) - 1)]
            
        # Özellikler:
        # Aktiflik: Start gibi 0 kalsın (veya çok az değişsin). Hedefe yaklaşmasın!
        # Etkileşim: Parent'tan +1 veya -1 fark etsin.
        # Baglanti: Sabit.
        
        # Parent özelliklerini bul (Basitlik için listeden okumak yerine simüle ediyoruz, 
        # çünkü node listesinde dictionary var)
        # Daha temizi: Etkileşim sürekli artsın
        
        etkilesim_val = (i % 100) * 1.5 # Yanlara doğru gidiyor gibi
        
        nodes.append({
            "id": node_id,
            "name": f"Decoy_{i+1}",
            "aktiflik": random.uniform(0, 5.0), # Hedefe (1000) KESİNLİKLE yaklaşmıyor
            "etkilesim": etkilesim_val, 
            "baglanti_sayisi": 0.0,
            "type": "decoy"
        })
        
        edges.append((parent, node_id))
        decoy_ids.append(node_id)


    # Komşuluk Listesi
    adj_list = {node['id']: [] for node in nodes}
    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)
        
    for node in nodes:
        node['baglanti_sayisi'] = len(adj_list[node['id']])

    # CSV Yaz
    file_path = os.path.join(os.getcwd(), 'data', filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, mode='w', newline='', encoding='utf-8') as f:
        fieldnames = ['DugumId', 'Isim', 'Ozellik_I (Aktiflik)', 'Ozellik_II (Etkileşim)', 'Ozellik_III (Bagl. Sayisi)', 'Komsular']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for node in nodes:
            komsular_str = ",".join(map(str, adj_list[node['id']]))
            writer.writerow({
                'DugumId': node['id'],
                'Isim': node['name'],
                'Ozellik_I (Aktiflik)': f"{node['aktiflik']:.2f}",
                'Ozellik_II (Etkileşim)': f"{node['etkilesim']:.2f}",
                'Ozellik_III (Bagl. Sayisi)': f"{node['baglanti_sayisi']:.2f}",
                'Komsular': komsular_str
            })
            
    print(f"Dataset generated at: {file_path}")
    print(f"Start Node: 1")
    print(f"End Node: {final_node}")

if __name__ == "__main__":
    generate_performance_data()
