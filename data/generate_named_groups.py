
import csv
import random
import math
import os

def generate_named_groups(filename="groups_social_network.csv"):
    # İsim Listesi (15 Adet)
    names = [
        "Ayşe", "Fatma", "Hayriye", "Nuriye", "Perihan", # Grup 1 (İzole)
        "Ali", "Veli", "Can", "Cem", "Deniz",           # Grup 2
        "Hasan", "Hüseyin", "Kamil", "Kazım", "Mahmut"  # Grup 3
    ]
    
    nodes = []
    edges = []
    
    # 3 Grup Yapısı
    # Grup 1: 0-4 (İzole)
    # Grup 2: 5-9
    # Grup 3: 10-14
    
    # Bridge: Node 9 (Deniz) ile Node 10 (Hasan) arasında bağlantı kuralım mi?
    # Yoksa "Ortak Arkadaş" mı? 
    # İstek: "sadece 1 ortak arkadaş olsun"
    # Yani G2 ve G3'ün kesişiminde 1 kişi var.
    # Node 9 (Deniz) hem G2'ye hem G3'e bağlı olsun.
    
    group1 = [0, 1, 2, 3, 4]
    group2 = [5, 6, 7, 8] # Deniz'i (9) ayırdık, o köprü olacak
    group3 = [10, 11, 12, 13, 14]
    bridge_node = 9 # Deniz
    
    # Node Özelliklerini Oluştur
    for i in range(15):
        nodes.append({
            "id": i + 1,
            "name": names[i],
            "aktiflik": round(random.uniform(0.1, 0.9), 2),
            "etkilesim": round(random.uniform(0.1, 0.9), 2),
            "baglanti_sayisi": 0 # Sonradan hesaplanacak
        })

    # Kenarları Oluştur
    
    # Grup 1 Kendi İçinde (Rastgele)
    for i in group1:
        for j in group1:
            if i < j and random.random() > 0.3: # %70 ihtimalle bağla
                edges.append((i+1, j+1))

    # Grup 2 Kendi İçinde
    for i in group2:
        for j in group2:
            if i < j and random.random() > 0.3:
                edges.append((i+1, j+1))
                
    # Grup 3 Kendi İçinde
    for i in group3:
        for j in group3:
            if i < j and random.random() > 0.3:
                edges.append((i+1, j+1))
                
    # Köprü (Deniz) Bağlantıları
    # G2'den birkaç kişiye bağla
    for person in group2:
        if random.random() > 0.4:
            edges.append((person+1, bridge_node+1))
            
    # G3'ten birkaç kişiye bağla
    for person in group3:
        if random.random() > 0.4:
            edges.append((person+1, bridge_node+1))
            
    # Köprü hiç bağlanmadıysa zorla bağla
    # (Basitlik için manuel eklemeler yapalım)
    if not any(e for e in edges if bridge_node+1 in e):
         edges.append((group2[0]+1, bridge_node+1))
         edges.append((group3[0]+1, bridge_node+1))

    # Komşuluk Listesi Hazırla
    adj_list = {node['id']: [] for node in nodes}
    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)
        
    # Bağlantı Sayılarını Güncelle
    for node in nodes:
        node['baglanti_sayisi'] = len(adj_list[node['id']])

    # CSV'ye Yaz
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
                'Ozellik_I (Aktiflik)': node['aktiflik'],
                'Ozellik_II (Etkileşim)': node['etkilesim'],
                'Ozellik_III (Bagl. Sayisi)': node['baglanti_sayisi'],
                'Komsular': komsular_str
            })
            
    print(f"Data generated at: {file_path}")

if __name__ == "__main__":
    generate_named_groups()
