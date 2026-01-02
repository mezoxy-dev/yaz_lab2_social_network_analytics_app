from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, 
                             QLabel, QLineEdit, QGroupBox, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt

class PropertiesPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.current_item = None # su an secili nodeitem veya edgeitem
        
        # 1. secim bilgisi grubu
        self.group_box = QGroupBox("Seçili Öğe Özellikleri (Selected Item)")
        self.form_layout = QFormLayout()
        self.group_box.setLayout(self.form_layout)
        
        self.layout.addWidget(self.group_box)
        
        # 2. alanlar
        self.id_label = QLabel("-")
        self.x_input = QLineEdit()
        self.y_input = QLineEdit()
        
        # yeni alanlar (ozellikler)
        self.input_aktiflik = QLineEdit()
        self.input_etkilesim = QLineEdit()
        self.input_baglanti = QLineEdit()
        
        # validator eklenebilir ama simdilik try-float yapacagiz
        
        self.form_layout.addRow("ID:", self.id_label)
        self.form_layout.addRow("X Konumu:", self.x_input)
        self.form_layout.addRow("Y Konumu:", self.y_input)
        
        # ayirici
        self.form_layout.addRow(QLabel("--- Düğüm Bilgileri ---"))
        self.form_layout.addRow("Aktiflik Puanı:", self.input_aktiflik)
        self.form_layout.addRow("Etkileşim Puanı:", self.input_etkilesim)
        self.form_layout.addRow("Bağlantı Sayısı:", self.input_baglanti)
        
        # x,y readonly kalsin (canvas'tan tasinarak degisiyor)
        self.x_input.setReadOnly(True)
        self.y_input.setReadOnly(True)
        
        # 3. guncelle butonu
        self.btn_update = QPushButton("Bilgileri Güncelle (Update)")
        # stil stylesheet'ten gelecek ama ozellestirme kalabilir
        self.btn_update.setStyleSheet("background-color: #3498db; color: white; font-weight: bold;")
        self.btn_update.clicked.connect(self.apply_changes)
        self.layout.addWidget(self.btn_update)
        
        self.layout.addStretch()

    def update_selection(self, item):
        self.current_item = item
        
        if item is None:
            self.id_label.setText("-")
            self.x_input.setText("")
            self.y_input.setText("")
            self.input_aktiflik.setText("")
            self.input_etkilesim.setText("")
            self.input_baglanti.setText("")
            self.btn_update.setEnabled(False)
            return

        self.btn_update.setEnabled(True)

        # eger nodeitem ise
        if hasattr(item, 'node_id'):
            self.id_label.setText(str(item.node_id))
            self.x_input.setText(f"{item.scenePos().x():.2f}")
            self.y_input.setText(f"{item.scenePos().y():.2f}")
            
            # ozellikleri cek
            props = item.properties if hasattr(item, 'properties') else {}
            self.input_aktiflik.setText(str(props.get('aktiflik', 0.0)))
            self.input_etkilesim.setText(str(props.get('etkilesim', 0.0)))
            self.input_baglanti.setText(str(props.get('baglanti_sayisi', 0.0)))
            
        else:
            # edgeitem veya baska bir sey
            self.id_label.setText("Edge (Read Only)")
            self.x_input.setText("")
            self.y_input.setText("")
            self.input_aktiflik.setText("")
            self.btn_update.setEnabled(False)

    def apply_changes(self):
        """
        kullanicinin girdigi yeni degerleri secili ogeye uygular.
        """
        if not self.current_item or not hasattr(self.current_item, 'properties'):
            return

        try:
            # degerleri al
            new_aktiflik = float(self.input_aktiflik.text())
            new_etkilesim = float(self.input_etkilesim.text())
            new_baglanti = float(self.input_baglanti.text())
            
            # nodeitem properties guncelle
            self.current_item.properties['aktiflik'] = new_aktiflik
            self.current_item.properties['etkilesim'] = new_etkilesim
            self.current_item.properties['baglanti_sayisi'] = new_baglanti
            
            print(f"updated node {self.current_item.node_id}: {self.current_item.properties}")
            
            # --- kritik adim: kenar agirliklarini guncelle ---
            # nodeitem degistikce ona bagli kenarlarin agirligi yeniden hesaplanmali
            if hasattr(self.current_item, 'update_connected_edges'):
                self.current_item.update_connected_edges()
                
            QMessageBox.information(self, "Başarılı (Success)", "Düğüm özellikleri güncellendi!\n(Node properties updated)")
            
        except ValueError:
            QMessageBox.warning(self, "Hata (Error)", "Lütfen geçerli sayısal değerler giriniz.\n(Invalid numeric values)")
