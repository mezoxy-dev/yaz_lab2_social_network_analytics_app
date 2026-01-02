# GÖREV: Üye A - Arayüz Kodları
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, pyqtSignal
from .visuals import NodeItem, EdgeItem
from .dialogs import EdgeDialog, NodeDialog

class GraphCanvas(QGraphicsView):
    itemMoved = pyqtSignal(object) # oge tasindiginda tetiklenecek sinyal
    nodeAdded = pyqtSignal(str)    # yeni dugum eklendiginde (id gonderir)
    nodeDeleted = pyqtSignal(str)  # dugum silindiginde (id gonderir)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 800, 600) # Sahne boyutunu sabitle
        self.setScene(self.scene)
        
        # gorunum ayarlari
        self.setRenderHint(QPainter.Antialiasing)  # kirilmalari onle
        self.setDragMode(QGraphicsView.RubberBandDrag) # varsayilan: dikdortgen secim
        
        # mod durumu
        self.mode = "SELECT" # SELECT, ADD_NODE, ADD_EDGE
        self.next_node_id = 1
        self.temp_source_node = None # kenar eklerken ilk secilen dugum

    def set_mode(self, mode):
        self.mode = mode
        self.temp_source_node = None # mod degisince secimi sifirla
        if mode == "SELECT":
            self.setDragMode(QGraphicsView.RubberBandDrag)
        else:
            self.setDragMode(QGraphicsView.NoDrag)
            
    def mousePressEvent(self, event):
        pos = self.mapToScene(event.pos())
        
        if self.mode == "ADD_NODE":
            from .visuals import NodeItem # Local import
            from .dialogs import NodeDialog # Local import
            
            # 1. dialog ile sor (zorunlu)
            dialog = NodeDialog(self, str(self.next_node_id), f"Node {self.next_node_id}")
            if dialog.exec_():
                label, props = dialog.get_data()
                
                # 2. onaylanirsa ekle
                node = NodeItem(str(self.next_node_id), pos.x(), pos.y(), label=label, properties=props)
                self.scene.addItem(node)
                self.nodeAdded.emit(str(self.next_node_id))
                self.next_node_id += 1
            else:
                # 3. iptal edilirse ekleme
                print("Node creation cancelled.")
            
        elif self.mode == "ADD_EDGE":
            item = self.scene.itemAt(pos, self.transform())
            from .visuals import NodeItem, EdgeItem # Local import
            from PyQt5.QtGui import QBrush, QColor # Local import if needed or use class level
            
            if isinstance(item, NodeItem):
                if not self.temp_source_node:
                    # ilk dugum secimi
                    self.temp_source_node = item
                    # vurgula (turuncu)
                    self.temp_source_node.setBrush(QBrush(QColor("#e67e22")))
                    print(f"Source selected: {item.node_id}")
                else:
                    if item != self.temp_source_node:
                        # ikinci dugum secimi - direkt ekle
                        # dialog yok, varsayilan weight = 1.0
                        weight = 1.0
                        edge = EdgeItem(self.temp_source_node, item, weight)
                        self.scene.addItem(edge)
                        print(f"Edge added: {self.temp_source_node.node_id} -> {item.node_id}, w={weight}")
                        
                        # vurguyu kaldir (maviye don)
                        self.temp_source_node.setBrush(QBrush(QColor("#3498db")))
                        self.temp_source_node = None # secimi sifirla
                    else:
                        # ayni dugume tiklandiysa iptal etme veya pass gecme
                        # kullanici vazgecmek isterse ne olacak?
                        # simdilik ayni dugume tiklarsa secimi iptal etsin
                        self.temp_source_node.setBrush(QBrush(QColor("#3498db")))
                        self.temp_source_node = None
                        print("Selection cleared")
        else:
            super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        pos = self.mapToScene(event.pos())
        item = self.scene.itemAt(pos, self.transform())
        
        if isinstance(item, NodeItem):
            # mevcut ozellikleri gonder
            from .dialogs import NodeDialog # Local import
            dialog = NodeDialog(self, item.node_id, item.label, properties=item.properties)
            
            if dialog.exec_():
                new_label, new_props = dialog.get_data()
                item.set_label(new_label) 
                
                # baglanti sayisini koru (otomatik hesaplandigi icin elle girilen 0'i ezmemeli)
                # ancak kullanici sadece aktiflik/etkilesim degistirdi.
                # baglanti sayisi canvas uzerindeki edge'lerden hesaplanmali veya mevcut korunmali.
                current_baglanti = item.properties.get('baglanti_sayisi', 0)
                new_props['baglanti_sayisi'] = current_baglanti # mevcudu koru
                
                item.properties = new_props
                item.update_connected_edges() # agirliklari guncelle (aktiflik degistiyse weight degisir)
                
                print(f"Node {item.node_id} updated: Label={new_label}, Props={new_props}")
        else:
            super().mouseDoubleClickEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        # eger surukleme islemindeysek ve bir secim varsa
        if self.scene.selectedItems():
            # ilk secili ogeyi gonder (genelde tek secim olur veya primary olan)
            self.itemMoved.emit(self.scene.selectedItems()[0])

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.delete_selected_items()
        else:
            super().keyPressEvent(event)

    def delete_selected_items(self):
        # silinecekleri topla
        items_to_delete = self.scene.selectedItems()
        
        for item in items_to_delete:
            # zaten silinmisse gec (scene none ise)
            if item.scene() is None:
                continue

            if isinstance(item, NodeItem):
                # node siliniyorsa bagli edge'leri de guvenli sil
                for edge in list(item.edges): 
                    if edge.scene() is not None:
                        # diger uctaki dugumden de sil
                        if edge.source != item: edge.source.remove_edge(edge)
                        if edge.target != item: edge.target.remove_edge(edge)
                        
                        self.scene.removeItem(edge)
                
                # kendisi de silinmemisse sil
                if item.scene() is not None:
                    self.scene.removeItem(item)
                    self.nodeDeleted.emit(item.node_id)
            
            elif isinstance(item, EdgeItem):
                # sadece kenar secilip silindiyse
                if item.scene() is not None:
                    # node'larin listesinden cikar
                    item.source.remove_edge(item)
                    item.target.remove_edge(item)
                    
                    self.scene.removeItem(item)
