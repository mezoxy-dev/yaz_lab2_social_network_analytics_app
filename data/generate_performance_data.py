
import csv
import random
import os

def generate_performance_data(filename="performance_social_network.csv"):
    nodes = []
    edges = []
    
    # SENARYO:
    # A*'ın bariz üstünlüğünü göstermek için "Coğrafi/Özellik" yönelimli bir labirent.
    # Start: (0, 0, 0)
    # Target: (1000, 0, 0) -> Sadece 'Aktiflik' özelliği çok yüksek.
    # Yol: (10,0,0) -> (20,0,0) -> ... dümdüz gidiyor.
    # Tuzaklar: Yan yollar (0, 10, 0) vb. veya geriye giden yollar.
    # Bu durumda Heuristic (Target'a kalan mesafe) doğru yolda sürekli azalırken,
    # yanlış yollarda artacak veya sabit kalacak.
    
    # 1. Optimal Yol (The Highway) - 100 Düğüm
    # Aktiflik 0'dan 1000'e gidiyor. Diğerleri 0.
    path_len = 100
    step_size = 1000 / path_len # 10 birim artış
    
    path_ids = []
    for i in range(path_len + 1): # 0..100
        val = i * step_size
        node_id = i + 1
        nodes.append({
            "id": node_id,
            "name": f"Path_{i}",
            "aktiflik": val, # Ana yönlendirici özellik
            "etkilesim": 0,
            "baglanti_sayisi": 0,
            "type": "path"
        })
        path_ids.append(node_id)
        
        # Zincirleme bağla
        if i > 0:
            edges.append((i, i + 1))
            
    start_id = 1
    end_id = path_len + 1

    # 2. Tuzak Ağacı (The Distraction Tree) - 1500 Düğüm
    # Bu düğümler 'Aktiflik' olarak ilerlemiyor (0 civarında kalıyor)
    # Ama 'Etkileşim' olarak yanlara açılıyor.
    # Dijkstra: Weight = 1 + dist. Yanlara gitmek (1 + 10) = 11 maliyet.
    # İleri gitmek (1 + 10) = 11 maliyet.
    # Dijkstra hepsini dener.
    # A*: Yanlara gitmek Heuristic'i (Target'a mesafe) azaltmaz. İleri gitmek azaltır.
    
    decoy_start_id = end_id + 1
    num_decoys = 1500
    
    # Tuzakları Start node ve yolun başındaki düğümlere ekleyelim
    for i in range(num_decoys):
        node_id = decoy_start_id + i
        
        # Rastgele bir decoy'a veya yolun başına bağla
        if i < 10:
             parent = random.choice(range(start_id, start_id + 5))
        else:
             # Ağaca bağla
             parent_offset = random.randint(1, min(i, 50))
             parent = node_id - parent_offset
        
        # Özellikler: Aktiflik DÜŞÜK (İlerlemiyor), Etkileşim RASTGELE (Yan yol)
        # Target (1000, 0, 0) olduğu için Etkileşim'in artması Heuristic'i büyütür (Kötüleştirir).
        # A* buraya girmek istemez.
        
        nodes.append({
            "id": node_id,
            "name": f"Decoy_{i}",
            "aktiflik": random.uniform(0, 50), # Hedefe gitmiyor
            "etkilesim": random.uniform(0, 1000), # Yanlara savruluyor
            "baglanti_sayisi": 0,
            "type": "decoy"
        })
        
        edges.append((parent, node_id))

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
    print(f"Nodes: {len(nodes)}, Edges: {len(edges)}")
    print(f"Start Node: {start_id} (Path_0)")
    print(f"End Node: {end_id} (Path_{path_len})")

if __name__ == "__main__":
    generate_performance_data()
