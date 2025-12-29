import csv
import random
import os

def generate_social_network(num_nodes=50, max_neighbors=5, filename="large_social_network.csv"):
    nodes = []
    
    # 1. Generate Nodes
    for i in range(1, num_nodes + 1):
        node = {
            'id': i,
            'activity': round(random.uniform(0, 100), 1),
            'interaction': round(random.uniform(0, 100), 1),
            'neighbors': set()
        }
        nodes.append(node)

    # 2. Generate Edges (Randomly)
    for node in nodes:
        # Determine number of neighbors for this node (random)
        num_neighbors = random.randint(1, max_neighbors)
        
        # Try to connect to random other nodes
        potential_neighbors = [n for n in nodes if n['id'] != node['id']]
        
        # Shuffle to pick random ones
        random.shuffle(potential_neighbors)
        
        for potential in potential_neighbors:
            if len(node['neighbors']) >= num_neighbors:
                break
                
            # Add edge (undirected for simplicity in generation, though logic allows directed)
            # To make it undirected consistent:
            if potential['id'] not in node['neighbors']:
                node['neighbors'].add(potential['id'])
                potential['neighbors'].add(node['id'])

    # 3. Write to CSV
    # Format: DugumId, Ozellik_I (Aktiflik), Ozellik_II (Etkileşim), Ozellik_III (Bagl. Sayisi), Komsular
    
    file_path = os.path.join(os.path.dirname(__file__), filename)
    
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['DugumId', 'Ozellik_I (Aktiflik)', 'Ozellik_II (Etkileşim)', 'Ozellik_III (Bagl. Sayisi)', 'Komsular']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for node in nodes:
            neighbors_list = list(node['neighbors'])
            neighbors_str = ",".join(map(str, neighbors_list))
            
            writer.writerow({
                'DugumId': node['id'],
                'Ozellik_I (Aktiflik)': node['activity'],
                'Ozellik_II (Etkileşim)': node['interaction'],
                'Ozellik_III (Bagl. Sayisi)': len(neighbors_list),
                'Komsular': neighbors_str
            })
            
    print(f"Generated {filename} with {num_nodes} nodes at {file_path}")

if __name__ == "__main__":
    generate_social_network(num_nodes=50, max_neighbors=8, filename="large_social_network.csv")
