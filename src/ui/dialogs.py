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
    def __init__(self, parent=None, node_id="", label=""):
        super().__init__(parent)
        self.setWindowTitle("Edit Node Properties")
        self.setModal(True)
        
        layout = QFormLayout(self)
        
        self.id_input = QLineEdit(str(node_id))
        self.id_input.setReadOnly(True) # ID değişmez
        self.label_input = QLineEdit(str(label))
        
        layout.addRow("Node ID:", self.id_input)
        layout.addRow("Label/Name:", self.label_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
    def get_data(self):
        return self.label_input.text()
