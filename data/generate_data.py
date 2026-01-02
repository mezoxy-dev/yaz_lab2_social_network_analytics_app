import csv
import random
import os

def generate_social_network(num_nodes=50, filename="medium_social_network.csv"):
    nodes = []
    
    # 1. Düğümleri Oluştur
    for i in range(1, num_nodes + 1):
        node = {
            'id': i,
            'aktiflik': round(random.uniform(0.1, 1.0), 2),
            'etkilesim': random.randint(1, 100),
            'baglanti_sayisi': 0, # Sonradan güncellenecek
            'neighbors': set()
        }
        nodes.append(node)
    
    # 2. Bağlantıları Oluştur (Rastgele)
    # Her düğümün en az 2, en çok 6 komşusu olsun (Small World benzeri)
    for node in nodes:
        num_links = random.randint(2, 6)
        current_neighbors = len(node['neighbors'])
        
        needed = num_links - current_neighbors
        if needed <= 0: continue
        
        # Kendisi ve zaten komşu oldukları hariç rastgele seç
        potential_targets = [n for n in nodes if n['id'] != node['id'] and n['id'] not in node['neighbors']]
        
        if not potential_targets: continue
        
        targets = random.sample(potential_targets, min(needed, len(potential_targets)))
        
        for target in targets:
            node['neighbors'].add(target['id'])
            target['neighbors'].add(node['id']) # Yönsüz
            
    # 3. Bağlantı Sayısı Özelliğini Güncelle ve CSV Yaz
    # Format: DugumId, Ozellik_I (Aktiflik), Ozellik_II (Etkileşim), Ozellik_III (Bagl. Sayisi), Komsular
    
    header = ['DugumId', 'Ozellik_I (Aktiflik)', 'Ozellik_II (Etkileşim)', 'Ozellik_III (Bagl. Sayisi)', 'Komsular']
    
    file_path = os.path.join(os.path.dirname(__file__), filename)
    
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        
        for node in nodes:
            neighbor_list = sorted(list(node['neighbors']))
            node['baglanti_sayisi'] = len(neighbor_list) # Özellik olarak işle
            
            neighbors_str = ",".join(map(str, neighbor_list))
            
            writer.writerow([
                node['id'],
                node['aktiflik'],
                node['etkilesim'],
                node['baglanti_sayisi'],
                neighbors_str
            ])
            
    print(f"Data generated at: {file_path}")

if __name__ == "__main__":
    # generate_social_network(75, "medium_social_network.csv")
    generate_social_network(15, "small_social_network.csv")
