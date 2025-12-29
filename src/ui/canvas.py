# GÖREV: Üye A - Arayüz Kodları
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, pyqtSignal
from .visuals import NodeItem, EdgeItem
from .dialogs import EdgeDialog, NodeDialog

class GraphCanvas(QGraphicsView):
    itemMoved = pyqtSignal(object) # Sitem taşındığında tetiklenecek sinyal
    nodeAdded = pyqtSignal(str)    # Yeni düğüm eklendiğinde (ID gönderir)
    nodeDeleted = pyqtSignal(str)  # Düğüm silindiğinde (ID gönderir)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 800, 600) # Sahne boyutunu sabitle
        self.setScene(self.scene)
        
        # Görünüm ayarları
        self.setRenderHint(QPainter.Antialiasing)  # Kırılmaları önle
        self.setDragMode(QGraphicsView.ScrollHandDrag) # Sahne kaydırma modu (şimdilik)
        
        # Mod durumu
        self.mode = "SELECT" # SELECT, ADD_NODE, ADD_EDGE
        self.next_node_id = 1
        self.temp_source_node = None # Kenar eklerken ilk seçilen düğüm

    def set_mode(self, mode):
        self.mode = mode
        self.temp_source_node = None # Mod değişince seçimi sıfırla
        if mode == "SELECT":
            self.setDragMode(QGraphicsView.RubberBandDrag)
        else:
            self.setDragMode(QGraphicsView.NoDrag)
            
    def mousePressEvent(self, event):
        pos = self.mapToScene(event.pos())
        
        if self.mode == "ADD_NODE":
            node = NodeItem(str(self.next_node_id), pos.x(), pos.y())
            self.scene.addItem(node)
            self.nodeAdded.emit(str(self.next_node_id))
            self.next_node_id += 1
            
        elif self.mode == "ADD_EDGE":
            item = self.scene.itemAt(pos, self.transform())
            if isinstance(item, NodeItem):
                if not self.temp_source_node:
                    self.temp_source_node = item
                    print(f"Source selected: {item.node_id}")
                else:
                    if item != self.temp_source_node:
                        # Diyalog Aç
                        dialog = EdgeDialog(self, self.temp_source_node.node_id, item.node_id)
                        if dialog.exec_():
                            weight = dialog.get_weight()
                            edge = EdgeItem(self.temp_source_node, item, weight)
                            self.scene.addItem(edge)
                            print(f"Edge added: {self.temp_source_node.node_id} -> {item.node_id}, w={weight}")
                        
                        self.temp_source_node = None # Seçimi sıfırla
        else:
            super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        pos = self.mapToScene(event.pos())
        item = self.scene.itemAt(pos, self.transform())
        
        if isinstance(item, NodeItem):
            dialog = NodeDialog(self, item.node_id, item.label)
            if dialog.exec_():
                new_label = dialog.get_data()
                item.set_label(new_label) # Label'ı güncelle
                print(f"Node {item.node_id} updated: Label={new_label}")
        else:
            super().mouseDoubleClickEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        # Eğer sürükleme işlemindeysek ve bir seçim varsa
        if self.scene.selectedItems():
            # İlk seçili öğeyi gönder (Genelde tek seçim olur veya primary olan)
            self.itemMoved.emit(self.scene.selectedItems()[0])

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.delete_selected_items()
        else:
            super().keyPressEvent(event)

    def delete_selected_items(self):
        # Silinecekleri topla
        items_to_delete = self.scene.selectedItems()
        
        for item in items_to_delete:
            # Zaten silinmişse geç (Scene None ise)
            if item.scene() is None:
                continue

            if isinstance(item, NodeItem):
                # Node siliniyorsa bağlı edge'leri de güvenli sil
                for edge in list(item.edges): 
                    if edge.scene() is not None:
                        # Diğer uçtaki düğümden de sil
                        if edge.source != item: edge.source.remove_edge(edge)
                        if edge.target != item: edge.target.remove_edge(edge)
                        
                        self.scene.removeItem(edge)
                
                # Kendisi de silinmemişse sil
                if item.scene() is not None:
                    self.scene.removeItem(item)
                    self.nodeDeleted.emit(item.node_id)
            
            elif isinstance(item, EdgeItem):
                # Sadece kenar seçilip silindiyse
                if item.scene() is not None:
                    # Node'ların listesinden çıkar
                    item.source.remove_edge(item)
                    item.target.remove_edge(item)
                    
                    self.scene.removeItem(item)
