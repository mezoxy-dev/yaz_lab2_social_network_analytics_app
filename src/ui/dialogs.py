from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QDoubleSpinBox, QLabel

class EdgeDialog(QDialog):
    def __init__(self, parent=None, source_id="", target_id="", weight=1.0):
        super().__init__(parent)
        self.setWindowTitle("Add/Edit Edge")
        self.setModal(True)
        
        layout = QFormLayout(self)
        
        self.source_label = QLabel(str(source_id))
        self.target_label = QLabel(str(target_id))
        self.weight_input = QDoubleSpinBox()
        self.weight_input.setRange(0.0, 1000.0)
        self.weight_input.setValue(float(weight))
        self.weight_input.setSingleStep(0.5)
        
        layout.addRow("Source Node:", self.source_label)
        layout.addRow("Target Node:", self.target_label)
        layout.addRow("Weight:", self.weight_input)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
    def get_weight(self):
        return self.weight_input.value()

class NodeDialog(QDialog):
    def __init__(self, parent=None, node_id="", label="", properties=None):
        super().__init__(parent)
        self.setWindowTitle("Düğüm Özellikleri (Node Properties)")
        self.setModal(True)
        
        layout = QFormLayout(self)
        
        self.id_input = QLineEdit(str(node_id))
        self.id_input.setReadOnly(True) 
        self.label_input = QLineEdit(str(label))
        
        # varsayilan degerler
        default_aktif = 0.0
        default_etki = 0.0
        if properties:
            default_aktif = float(properties.get('aktiflik', 0.0))
            default_etki = float(properties.get('etkilesim', 0.0))
            
        self.spin_aktif = QDoubleSpinBox()
        self.spin_aktif.setRange(0.0, 1000.0)
        self.spin_aktif.setValue(default_aktif)
        self.spin_aktif.setSingleStep(1.0) # v3: hata duzeltme, genelde tam sayi veya 1.0 adimli
        
        self.spin_etki = QDoubleSpinBox()
        self.spin_etki.setRange(0.0, 1000.0)
        self.spin_etki.setValue(default_etki)
        self.spin_etki.setSingleStep(1.0)
        
        layout.addRow("Düğüm ID:", self.id_input)
        layout.addRow("İsim (Name):", self.label_input)
        layout.addRow("Aktiflik (Activity):", self.spin_aktif)
        layout.addRow("Etkileşim (Interaction):", self.spin_etki)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
    def get_data(self):
        props = {
            'aktiflik': self.spin_aktif.value(),
            'etkilesim': self.spin_etki.value(),
            'baglanti_sayisi': 0 # bu otomatik hesaplanir, elle girilemez
        }
        return self.label_input.text(), props
