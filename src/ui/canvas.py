# GÖREV: Üye A - Arayüz Kodları
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene

class GraphCanvas(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
