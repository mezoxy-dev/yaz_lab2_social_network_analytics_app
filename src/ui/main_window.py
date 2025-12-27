# GÖREV: Üye A - Arayüz Kodları
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QDockWidget
from PyQt5.QtCore import Qt
from .canvas import GraphCanvas
from .properties_panel import PropertiesPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Social Network Analysis")
        self.setGeometry(100, 100, 1000, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        self.canvas = GraphCanvas(self)
        self.layout.addWidget(self.canvas)
        
        # Araç Çubuğu Oluşturma
        self.create_toolbar()
        
        # Panelleri Oluştur
        self.create_dock_panels()
        
        # Sinyal Bağlantıları
        self.canvas.scene.selectionChanged.connect(self.on_selection_changed)
        self.canvas.itemMoved.connect(self.properties_panel.update_selection)

    def create_dock_panels(self):
        self.properties_dock = QDockWidget("Properties", self)
        self.properties_dock.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)
        
        self.properties_panel = PropertiesPanel()
        self.properties_dock.setWidget(self.properties_panel)
        
        self.addDockWidget(Qt.RightDockWidgetArea, self.properties_dock)

    def on_selection_changed(self):
        items = self.canvas.scene.selectedItems()
        if items:
            self.properties_panel.update_selection(items[0])
        else:
            self.properties_panel.update_selection(None)

    def create_toolbar(self):
        toolbar = self.addToolBar("Tools")
        
        # Aksiyonlar
        self.action_select = toolbar.addAction("Select")
        self.action_add_node = toolbar.addAction("Add Node")
        self.action_add_edge = toolbar.addAction("Add Edge")
        self.action_clear = toolbar.addAction("Clear")
        
        # Bağlantılar
        self.action_select.triggered.connect(lambda: self.canvas.set_mode("SELECT"))
        self.action_add_node.triggered.connect(lambda: self.canvas.set_mode("ADD_NODE"))
        self.action_add_edge.triggered.connect(lambda: self.canvas.set_mode("ADD_EDGE"))
        self.action_clear.triggered.connect(self.canvas.scene.clear)
