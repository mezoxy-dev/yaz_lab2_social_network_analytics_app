import unittest
from src.model.graph import Graph
from src.model.node import Node
from src.algorithms.bfs_dfs import BFSAlgorithm, DFSAlgorithm
from src.algorithms.shortest_path import DijkstraAlgorithm

class TestAlgorithms(unittest.TestCase):
    def setUp(self):
        """Her testten önce basit bir graf oluşturur."""
        self.graph = Graph()
        
        # Düğümler: 1 --(1)--> 2 --(2)--> 3
        #           |          ^
        #           +--(5)-----+
        self.n1 = Node("1", x=0, y=0)
        self.n2 = Node("2", x=10, y=0)
        self.n3 = Node("3", x=20, y=0)
        
        self.graph.add_node(self.n1)
        self.graph.add_node(self.n2)
        self.graph.add_node(self.n3)
        
        self.graph.add_edge("1", "2")
        self.graph.add_edge("2", "3")
        self.graph.add_edge("1", "3") # Ağırlık hesaplaması Node özelliklerine bağlı ama varsayılan çalışır

    def test_bfs(self):
        algo = BFSAlgorithm()
        path = algo.execute(self.graph, start_node_id="1")
        # 1'den başlayınca 1, 2, 3 (veya 1, 3, 2) sırasıyla gezmeli
        self.assertIn("1", path)
        self.assertIn("2", path)
        self.assertIn("3", path)
        self.assertEqual(path[0], "1")

    def test_dijkstra_path_exists(self):
        algo = DijkstraAlgorithm()
        # 1 -> 3 yolu
        path = algo.execute(self.graph, start_node_id="1", end_node_id="3")
        self.assertTrue(len(path) > 0)
        self.assertEqual(path[0], "1")
        self.assertEqual(path[-1], "3")

    def test_invalid_node(self):
        algo = BFSAlgorithm()
        path = algo.execute(self.graph, start_node_id="99") # Yok
        self.assertEqual(path, [])

if __name__ == '__main__':
    unittest.main()
