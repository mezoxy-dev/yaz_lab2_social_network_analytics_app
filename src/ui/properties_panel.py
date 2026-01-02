from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, 
                             QLabel, QLineEdit, QGroupBox, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt

class PropertiesPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.current_item = None # Şu an seçili NodeItem veya EdgeItem
        
        # 1. Seçim Bilgisi Grubu
        self.group_box = QGroupBox("Selected Item Properties")
        self.form_layout = QFormLayout()
        self.group_box.setLayout(self.form_layout)
        
        self.layout.addWidget(self.group_box)
        
        # 2. Alanlar
        self.id_label = QLabel("-")
        self.x_input = QLineEdit()
        self.y_input = QLineEdit()
        
        # Yeni Alanlar (Özellikler)
        self.input_aktiflik = QLineEdit()
        self.input_etkilesim = QLineEdit()
        self.input_baglanti = QLineEdit()
        
        # Validator eklenebilir ama şimdilik try-float yapacagiz
        
        self.form_layout.addRow("ID:", self.id_label)
        self.form_layout.addRow("X:", self.x_input)
        self.form_layout.addRow("Y:", self.y_input)
        
        # Ayırıcı
        self.form_layout.addRow(QLabel("--- Node Attributes ---"))
        self.form_layout.addRow("Active (0-1):", self.input_aktiflik)
        self.form_layout.addRow("Interaction:", self.input_etkilesim)
        self.form_layout.addRow("Connections:", self.input_baglanti)
        
        # X,Y ReadOnly kalsın (Canvas'tan taşınarak değişiyor)
        self.x_input.setReadOnly(True)
        self.y_input.setReadOnly(True)
        
        # 3. Güncelle Butonu
        self.btn_update = QPushButton("Update Properties")
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

        # Eğer NodeItem ise
        if hasattr(item, 'node_id'):
            self.id_label.setText(str(item.node_id))
            self.x_input.setText(f"{item.scenePos().x():.2f}")
            self.y_input.setText(f"{item.scenePos().y():.2f}")
            
            # Özellikleri Çek
            props = item.properties if hasattr(item, 'properties') else {}
            self.input_aktiflik.setText(str(props.get('aktiflik', 0.0)))
            self.input_etkilesim.setText(str(props.get('etkilesim', 0.0)))
            self.input_baglanti.setText(str(props.get('baglanti_sayisi', 0.0)))
            
        else:
            # EdgeItem veya başka bir şey
            self.id_label.setText("Edge (Read Only)")
            self.x_input.setText("")
            self.y_input.setText("")
            self.input_aktiflik.setText("")
            self.btn_update.setEnabled(False)

    def apply_changes(self):
        """Kullanıcının girdiği yeni değerleri seçili öğeye uygular."""
        if not self.current_item or not hasattr(self.current_item, 'properties'):
            return

        try:
            # Değerleri al
            new_aktiflik = float(self.input_aktiflik.text())
            new_etkilesim = float(self.input_etkilesim.text())
            new_baglanti = float(self.input_baglanti.text())
            
            # NodeItem properties güncelle
            self.current_item.properties['aktiflik'] = new_aktiflik
            self.current_item.properties['etkilesim'] = new_etkilesim
            self.current_item.properties['baglanti_sayisi'] = new_baglanti
            
            print(f"Updated Node {self.current_item.node_id}: {self.current_item.properties}")
            
            # --- KRİTİK ADIM: Kenar Ağırlıklarını Güncelle ---
            # NodeItem değiştikçe ona bağlı kenarların ağırlığı yeniden hesaplanmalı
            if hasattr(self.current_item, 'update_connected_edges'):
                self.current_item.update_connected_edges()
                
            QMessageBox.information(self, "Success", "Node properties updated successfully!")
            
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter valid numeric values.")
