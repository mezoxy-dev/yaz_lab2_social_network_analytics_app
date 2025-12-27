from PyQt5.QtWidgets import QGraphicsItem, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsPathItem
from PyQt5.QtCore import Qt, QRectF, QLineF, QPointF
from PyQt5.QtGui import QPen, QBrush, QColor, QPainter, QPolygonF, QPainterPath
import math

class NodeItem(QGraphicsEllipseItem):
    def __init__(self, node_id, x, y, radius=20, label=""):
        super().__init__(-radius, -radius, 2 * radius, 2 * radius)
        self.node_id = node_id
        self.label = label
        self.radius = radius
        
        # Görsel ayarlar
        self.setPos(x, y)
        self.setBrush(QBrush(QColor("#3498db")))  # Modern mavi
        self.setPen(QPen(Qt.black, 1))
        
        # Etkileşim ayarları
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        
        self.edges = []  # Bağlı olduğu kenarlar

    def set_label(self, label):
        self.prepareGeometryChange() # Geometri değişiyor (boundingRect), Qt'ye haber ver
        self.label = label
        self.update()

    def boundingRect(self):
        # Normal daire alanı
        rect = super().boundingRect()
        # Eğer label varsa, alt kısma label yüksekliği kadar alan ekle
        if self.label:
            rect.setBottom(rect.bottom() + 25) # Label için pay bırak
            # Genişliği de biraz artır ki uzun isimler kesilmesin
            rect.setLeft(rect.left() - 20)
            rect.setRight(rect.right() + 20)
        return rect
        
    def paint(self, painter, option, widget):
        # Varsayılan çizim (Daire)
        super().paint(painter, option, widget)
        
        # Yazı Çizimi
        painter.setPen(Qt.white)
        font = painter.font()
        font.setBold(True)
        painter.setFont(font)
        
        # ID'yi merkeze yaz
        painter.drawText(self.rect(), Qt.AlignCenter, str(self.node_id))
        
        # Label varsa altına yaz (Dairenin dışında)
        if self.label:
            painter.setPen(Qt.black)
            # Metni dairenin (self.rect()) altına hizala, bounding box'a göre değil
            rect = QRectF(self.rect()) 
            rect.setTop(rect.bottom()) # Dairenin altı
            rect.setHeight(25) # Yükseklik ver
            
            # Genişliği artırarak ortala
            rect.setLeft(rect.left() - 20)
            rect.setRight(rect.right() + 20)
            
            painter.drawText(rect, Qt.AlignCenter, self.label)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            for edge in self.edges:
                edge.adjust()
        return super().itemChange(change, value)

    def add_edge(self, edge):
        self.edges.append(edge)

class EdgeItem(QGraphicsPathItem): # LineItem yerine PathItem kullanıyoruz
    def __init__(self, source_node, target_node, weight=1.0):
        super().__init__()
        self.source = source_node
        self.target = target_node
        self.weight = weight
        self.arrow_size = 10
        
        # Kalem ayarları
        pen = QPen(QColor("#2c3e50"), 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        self.setPen(pen)
        self.setZValue(-1)
        
        self.source.add_edge(self)
        self.target.add_edge(self)
        
        self.adjust()

    def adjust(self):
        if not self.source or not self.target:
            return
            
        self.prepareGeometryChange()
        
        start_pos = self.source.scenePos()
        end_pos = self.target.scenePos()
        line = QLineF(start_pos, end_pos)
        length = line.length()
        
        # Ters yönde bir kenar var mı kontrol et
        has_reverse_edge = False
        for edge in self.target.edges:
            if edge.source == self.target and edge.target == self.source:
                has_reverse_edge = True
                break
        
        # Yol Oluşturma
        path = QPainterPath()
        
        # Başlangıç ve bitiş noktalarını düğüm yarıçapına göre ayarla
        angle = math.atan2(line.dy(), line.dx())
        offset_source = self.source.radius
        offset_target = self.target.radius
        
        # Düzeltilmiş başlangıç/bitiş
        p1 = start_pos + QPointF(math.cos(angle) * offset_source, math.sin(angle) * offset_source)
        p2 = end_pos - QPointF(math.cos(angle) * offset_target, math.sin(angle) * offset_target)

        if has_reverse_edge and length > 0:
            # Eğri çiz (Quadratic Curve)
            # Orta noktayı biraz yukarı/yana kaydır
            
            # Normal vektör (Çizgiye dik)
            dx = line.dx()
            dy = line.dy()
            
            # Eğrilik miktarı (Mesafeye göre artabilir veya sabit olabilir)
            offset = 40 
            
            # Orta noktayı bul
            mid_point = (p1 + p2) / 2
            
            # Normal vektörü normalize et ve offset kadar ötele
            # (-dy, dx) 90 derece döndürür
            norm_len = math.sqrt(dx*dx + dy*dy)
            ctrl_point = mid_point + QPointF(-dy * offset / norm_len, dx * offset / norm_len)
            
            path.moveTo(p1)
            path.quadTo(ctrl_point, p2)
        else:
            # Düz çizgi
            path.moveTo(p1)
            path.lineTo(p2)
            
        self.setPath(path)

    def boundingRect(self):
        # Path'in sınırlarını döndür ama biraz genişlet
        rect = self.path().boundingRect()
        extra = (self.pen().width() + self.arrow_size + 20)
        return rect.adjusted(-extra, -extra, extra, extra)

    def paint(self, painter, option, widget):
        if not self.source or not self.target:
            return
            
        painter.setPen(self.pen())
        painter.drawPath(self.path())
        
        self.draw_arrow(painter)
        
        if self.weight != 1.0:
             self.draw_weight(painter)

    def draw_arrow(self, painter):
        path = self.path()
        if path.isEmpty(): return

        # Bitiş noktasındaki açıyı bul
        # Bitiş noktasından çok az öncesine bakıp açıyı hesaplıyoruz (Türevi)
        p_end = path.pointAtPercent(1.0)
        p_pre = path.pointAtPercent(0.95) # %95 noktasındaki açı
        
        angle = math.atan2(p_end.y() - p_pre.y(), p_end.x() - p_pre.x())

        arrow_p1 = p_end - QPointF(math.sin(angle + math.pi / 3) * self.arrow_size,
                                   math.cos(angle + math.pi / 3) * self.arrow_size)
        arrow_p2 = p_end - QPointF(math.sin(angle + math.pi - math.pi / 3) * self.arrow_size,
                                   math.cos(angle + math.pi - math.pi / 3) * self.arrow_size)

        arrow_head = QPolygonF([p_end, arrow_p1, arrow_p2])
        
        painter.setBrush(QBrush(QColor("#2c3e50")))
        painter.drawPolygon(arrow_head)

    def draw_weight(self, painter):
        path = self.path()
        if path.isEmpty(): return
        
        # Yolun tam ortasına yaz (%50)
        center_point = path.pointAtPercent(0.5)
        
        text = str(self.weight)
        rect = QRectF(center_point.x() - 15, center_point.y() - 10, 30, 20)
        
        # Arkaplan kutusu (okunabilirlik için)
        painter.setBrush(QBrush(QColor(255, 255, 255, 200))) 
        painter.setPen(Qt.NoPen)
        painter.drawRect(rect)
        
        painter.setPen(Qt.black)
        painter.drawText(rect, Qt.AlignCenter, text)
