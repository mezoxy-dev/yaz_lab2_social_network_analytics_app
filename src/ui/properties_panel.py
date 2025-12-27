from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, 
                             QLabel, QLineEdit, QGroupBox)

class PropertiesPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Seçim Bilgisi Grubu
        self.group_box = QGroupBox("Selected Item Properties")
        self.form_layout = QFormLayout()
        self.group_box.setLayout(self.form_layout)
        
        self.layout.addWidget(self.group_box)
        self.layout.addStretch()
        
        # Alanlar
        self.id_label = QLabel("-")
        self.x_input = QLineEdit()
        self.y_input = QLineEdit()
        
        self.form_layout.addRow("ID:", self.id_label)
        self.form_layout.addRow("X:", self.x_input)
        self.form_layout.addRow("Y:", self.y_input)
        
        # Şimdilik düzenlemeyi kapatalım (sadece görüntüleme)
        self.x_input.setReadOnly(True)
        self.y_input.setReadOnly(True)

    def update_selection(self, item):
        if item is None:
            self.id_label.setText("-")
            self.x_input.setText("")
            self.y_input.setText("")
            return

        # Eğer NodeItem ise
        if hasattr(item, 'node_id'):
            self.id_label.setText(str(item.node_id))
            self.x_input.setText(f"{item.scenePos().x():.2f}")
            self.y_input.setText(f"{item.scenePos().y():.2f}")
