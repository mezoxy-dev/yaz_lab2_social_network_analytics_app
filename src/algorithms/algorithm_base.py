from abc import ABC, abstractmethod

class Algorithm(ABC):
    """
    Algoritmalar için temel sınıf.
    """

    @abstractmethod
    def get_name(self):
        """Algoritmanın ekranda görünecek adını döndürür (Örn: 'BFS')."""
        pass

    @abstractmethod
    def execute(self, graph, start_node_id=None, end_node_id=None):
        """
        Algoritmanın ana çalışma mantığı.
        Args:
            graph: Üzerinde çalışılacak Graph nesnesi
            start_node_id: Başlangıç düğümü (Opsiyonel)
            end_node_id: Bitiş düğümü (Opsiyonel - Dijkstra için)
        Returns:
            list: Ziyaret edilen düğümlerin veya yolun listesi
        """
        pass