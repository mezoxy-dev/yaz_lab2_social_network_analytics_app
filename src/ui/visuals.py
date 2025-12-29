from PyQt5.QtWidgets import QGraphicsItem, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsPathItem, QStyle
from PyQt5.QtCore import Qt, QRectF, QLineF, QPointF
from PyQt5.QtGui import QPen, QBrush, QColor, QPainter, QPolygonF, QPainterPath, QPainterPathStroker
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

    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)

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
        
        # Seçilebilir yap (Silmek için gerekli)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        
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

    def shape(self):
        """Tıklamayı kolaylaştırmak için daha kalın bir yol döndür."""
        path = QPainterPathStroker()
        path.setWidth(10) # Tıklama alanı genişliği
        return path.createStroke(self.path())

    def paint(self, painter, option, widget):
        if not self.source or not self.target:
            return
        
        # Seçili ise farklı çiz
        # option.state & QStyle.State_Selected kontrolü için QStyle import edilmeli
        # veya int değeri 0x00000001 (State_Selected)
        
        # Daha temiz olması için QStyle.State_Selected kullanmayı tercih ederim ama import eklemem lazım.
        # Pratik çözüm: Qt.WA_... değil ama Style option flagleri.

        if option.state & QStyle.State_Selected:
            # Seçili: Kalın ve kırmızı
            pen = QPen(QColor("#e74c3c"), 3, Qt.DashLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen)
            painter.drawPath(self.path())
        else:
            # Normal
            painter.setPen(self.pen())
            painter.drawPath(self.path())
        
        if self.weight != 1.0:
             self.draw_weight(painter)

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
