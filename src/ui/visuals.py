from PyQt5.QtWidgets import QGraphicsItem, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsPathItem, QStyle
from PyQt5.QtCore import Qt, QRectF, QLineF, QPointF
from PyQt5.QtGui import QPen, QBrush, QColor, QPainter, QPolygonF, QPainterPath, QPainterPathStroker
import math

class NodeItem(QGraphicsEllipseItem):
    def __init__(self, node_id, x, y, radius=20, label="", properties=None):
        super().__init__(-radius, -radius, 2 * radius, 2 * radius)
        self.node_id = node_id
        self.label = label
        self.radius = radius
        self.properties = properties if properties else {}
        
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
        # Bağlantı eklendiğinde sayıyı artır
        current_count = float(self.properties.get('baglanti_sayisi', 0))
        self.properties['baglanti_sayisi'] = current_count + 1
        
        # Diğer kenarların ağırlıklarını güncelle
        self.update_connected_edges()

    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)
            # Bağlantı silindiğinde sayıyı azalt
            current_count = float(self.properties.get('baglanti_sayisi', 0))
            if current_count > 0:
                self.properties['baglanti_sayisi'] = current_count - 1
            
            # Bu düğüme bağlı DİĞER kenarların ağırlıklarını güncelle
            # Çünkü bu düğümün 'baglanti_sayisi' değişti, dolayısıyla diğer kenarların maliyeti de değişmeli!
            self.update_connected_edges()

    def update_connected_edges(self):
        """Bu düğüme bağlı tüm kenarların ağırlığını yeniden hesaplar."""
        for edge in self.edges:
            edge.recalculate_weight()

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

    def recalculate_weight(self):
        """Node özelliklerine göre ağırlığı günceller (Model'den formülü çeker)."""
        from src.model.edge import Edge # Circular import kaçınmak için burada
        
        if self.source and self.target:
            p_source = self.source.properties
            p_target = self.target.properties
            
            # Model sınıfındaki statik metodu kullan
            new_weight, _ = Edge.calculate_weight(p_source, p_target)
            
            self.weight = new_weight
            self.update() # Görsel güncelle (draw_weight çalışacak)

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
        
        # Font Ayarları (Daha Okunaklı)
        font = painter.font()
        font.setPointSize(10)
        font.setBold(True)
        painter.setFont(font)
        
        # Metin Boyutunu Hesapla
        fm = painter.fontMetrics()
        text_width = fm.width(text)
        text_height = fm.height()
        
        # Arkaplan Kutusunu Metne Göre Ayarla (+Padding)
        padding = 10
        rect_width = text_width + padding
        rect_height = text_height + 4
        
        # Kutuyu ortala
        rect = QRectF(center_point.x() - rect_width / 2, 
                      center_point.y() - rect_height / 2, 
                      rect_width, rect_height)
        
        # Arkaplan kutusu (Beyaz, görünür çerçeve)
        painter.setBrush(QBrush(QColor(255, 255, 255, 255))) # Tam opak beyaz
        painter.setPen(QPen(Qt.black, 1)) # İnce siyah çerçeve
        painter.drawRoundedRect(rect, 5, 5) # Yuvarlatılmış köşeler
        
        # Metni Çiz
        painter.setPen(Qt.black)
        painter.drawText(rect, Qt.AlignCenter, text)
