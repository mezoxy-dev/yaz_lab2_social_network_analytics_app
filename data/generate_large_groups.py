
import csv
import random
import os

def generate_large_groups(filename="large_groups_network.csv"):
    # 1. İsim ve Soyisim Havuzu (Rastgele İsim Üretimi İçin)
    first_names = [
        "Mehmet", "Fatma", "Mustafa", "Ayşe", "Ahmet", "Emine", "Ali", "Hatice", 
        "Hüseyin", "Zeynep", "Hasan", "Elif", "İbrahim", "Merve", "İsmail", 
        "Şerife", "Osman", "Zehra", "Yusuf", "Sultan", "Murat", "Hanife", 
        "Ömer", "Meryem", "Ramazan", "Havva", "Halil", "Zeliha", "Süleyman"
    ]
    last_names = [
        "Yılmaz", "Kaya", "Demir", "Çelik", "Şahin", "Yıldız", "Yıldırım", 
        "Öztürk", "Aydın", "Özdemir", "Arslan", "Doğan", "Kılıç", "Aslan", 
        "Çetin", "Kara", "Koç", "Kurt", "Özkan", "Şimşek"
    ]
    
    nodes = []
    edges = []
    
    total_nodes = 100
    num_groups = 7
    
    # Grupları oluştur (Yaklaşık 14-15 kişi)
    groups = []
    current_id = 1
    
    # 7 gruba böl
    # 100 / 7 = 14.28 -> [14, 14, 14, 14, 14, 14, 16] gibi dağıtalım
    group_sizes = [14] * 6 + [16] 
    
    all_names = set()
    
    for group_idx, size in enumerate(group_sizes):
        group_nodes = []
        for _ in range(size):
            # Benzersiz isim üret
            while True:
                name = f"{random.choice(first_names)} {random.choice(last_names)}"
                if name not in all_names:
                    all_names.add(name)
                    break
            
            node = {
                "id": current_id,
                "name": name,
                "group_id": group_idx,
                "aktiflik": round(random.uniform(0.1, 0.95), 2),
                "etkilesim": round(random.uniform(0.1, 0.95), 2),
                "baglanti_sayisi": 0
            }
            nodes.append(node)
            group_nodes.append(current_id)
            current_id += 1
            
        groups.append(group_nodes)

    # 2. Grup İçi Bağlantılar (Yoğunluk)
    for group in groups:
        # Her grup kendi içinde %25 oranında bağlı olsun
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                if random.random() < 0.25:
                    edges.append((group[i], group[j]))

    # 3. Gruplar Arası Bağlantılar (Zincir Yapısı: G1-G2-G3-G4-G5-G6-G7)
    # Her grup bir sonrakine 2-3 ortak arkadaş ile bağlansın
    for i in range(num_groups - 1):
        g_current = groups[i]
        g_next = groups[i+1]
        
        # Kaç bağlantı olacak? (2 veya 3)
        num_bridges = random.randint(2, 3)
        
        # Rastgele kişiler seç ve bağla
        # Her bağlantı farklı kişiler arasında olsun ki çeşitlilik artsın
        src_nodes = random.sample(g_current, num_bridges)
        tgt_nodes = random.sample(g_next, num_bridges)
        
        for u, v in zip(src_nodes, tgt_nodes):
            edges.append((u, v))

    # Komşuluk Listesi Hazırlama
    adj_list = {node['id']: [] for node in nodes}
    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)
        
    # Bağlantı Sayılarını Güncelle
    for node in nodes:
        node['baglanti_sayisi'] = len(adj_list[node['id']])

    # CSV Kaydet
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
            
    print(f"Large dataset generated at: {file_path}")

if __name__ == "__main__":
    generate_large_groups()
