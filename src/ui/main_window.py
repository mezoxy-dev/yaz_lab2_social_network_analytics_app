# GÖREV: Üye A - Arayüz Kodları
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QDockWidget, QTabWidget, QPushButton, QComboBox, QLabel, QFormLayout, QHBoxLayout, QFileDialog, QMessageBox, QAction
from PyQt5.QtCore import Qt, QSize
from .canvas import GraphCanvas
from .properties_panel import PropertiesPanel
from src.model.graph import Graph
from src.model.node import Node
from src.algorithms.bfs_dfs import BFSAlgorithm, DFSAlgorithm
from src.algorithms.shortest_path import DijkstraAlgorithm, AStarAlgorithm
from src.model.file_manager import CSVFileManager

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
        self.create_menubar()
        
        # Panelleri Oluştur
        self.create_dock_panels()
        
        # Sinyal Bağlantıları
        self.canvas.scene.selectionChanged.connect(self.on_selection_changed)
        # Sinyal Bağlantıları
        self.canvas.scene.selectionChanged.connect(self.on_selection_changed)
        self.canvas.itemMoved.connect(self.properties_panel.update_selection)
        self.canvas.nodeAdded.connect(self.update_combos)
        self.canvas.nodeDeleted.connect(self.update_combos)
        
        # Status Bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")

    def create_dock_panels(self):
        # --- SAĞ PANEL (Özellikler) ---
        self.properties_dock = QDockWidget("Properties", self)
        self.properties_dock.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)
        self.properties_panel = PropertiesPanel()
        self.properties_dock.setWidget(self.properties_panel)
        self.addDockWidget(Qt.RightDockWidgetArea, self.properties_dock)
        
        # --- SOL PANEL (Kontrol / Analiz) ---
        self.control_dock = QDockWidget("Control Panel", self)
        self.control_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        
        # Tab Yapısı (Edit / Analysis)
        self.tabs = QTabWidget()
        self.setup_edit_tab()
        self.setup_analysis_tab()
        
        self.control_dock.setWidget(self.tabs)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.control_dock)

    def setup_edit_tab(self):
        """Düzenleme işlevleri için sekme"""
        edit_widget = QWidget()
        layout = QVBoxLayout(edit_widget)
        
        btn_select = QPushButton("Select Mode")
        btn_add_node = QPushButton("Add Node")
        btn_add_edge = QPushButton("Add Edge")
        btn_clear = QPushButton("Clear All")
        
        # Butonlara ikon veya stil eklenebilir
        btn_clear.setStyleSheet("background-color: #ffcccc;")
        
        layout.addWidget(btn_select)
        layout.addWidget(btn_add_node)
        layout.addWidget(btn_add_edge)
        layout.addStretch() # Boşluğu alta it
        layout.addWidget(btn_clear)
        
        self.tabs.addTab(edit_widget, "Edit")
        
        # Bağlantılar
        btn_select.clicked.connect(lambda: self.canvas.set_mode("SELECT"))
        btn_add_node.clicked.connect(lambda: self.canvas.set_mode("ADD_NODE"))
        btn_add_edge.clicked.connect(lambda: self.canvas.set_mode("ADD_EDGE"))
        btn_clear.clicked.connect(self.canvas.scene.clear)

    def setup_analysis_tab(self):
        """Algoritmalar için sekme"""
        analysis_widget = QWidget()
        layout = QVBoxLayout(analysis_widget)
        
        # Algoritma Seçimi
        layout.addWidget(QLabel("<b>Algorithm:</b>"))
        self.combo_algo = QComboBox()
        self.combo_algo.addItems([
            "BFS (Breadth-First)", 
            "DFS (Depth-First)", 
            "Dijkstra Shortest Path", 
            "A* Shortest Path",
            "Clustering",
            "Welsh-Powell Coloring"
        ])
        layout.addWidget(self.combo_algo)
        
        # Parametreler (Start/End Node)
        # Not: Bu combobox'ların içi Node eklendikçe dolmalı
        form_layout = QFormLayout()
        self.combo_start_node = QComboBox()
        self.combo_end_node = QComboBox()
        
        form_layout.addRow("Start Node:", self.combo_start_node)
        form_layout.addRow("End Node:", self.combo_end_node)
        layout.addLayout(form_layout)
        
        # Çalıştır Butonu
        self.btn_run = QPushButton("Run Algorithm")
        self.btn_run.setStyleSheet("background-color: #ccffcc; font-weight: bold;")
        layout.addWidget(self.btn_run)
        
        # Sonuç Alanı
        layout.addWidget(QLabel("<b>Result:</b>"))
        self.lbl_result = QLabel("Result will appear here...")
        self.lbl_result.setWordWrap(True)
        self.lbl_result.setStyleSheet("border: 1px solid #ccc; padding: 5px; background: white;")
        layout.addWidget(self.lbl_result)
        
        layout.addStretch()
        self.tabs.addTab(analysis_widget, "Analysis")
        
        # Signal Bağlantısı
        self.btn_run.clicked.connect(self.run_algorithm)

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
        self.action_add_edge.triggered.connect(lambda: self.canvas.set_mode("ADD_EDGE"))
        self.action_clear.triggered.connect(self.canvas.scene.clear)
        self.action_clear.triggered.connect(self.update_combos)

    def update_combos(self):
        """Combobox'ları kandaki düğümlerle günceller."""
        from .visuals import NodeItem # Döngüsel importu önlemek için burada
        
        current_start = self.combo_start_node.currentText()
        current_end = self.combo_end_node.currentText()
        
        self.combo_start_node.clear()
        self.combo_end_node.clear()
        
        node_ids = []
        for item in self.canvas.scene.items():
            if isinstance(item, NodeItem):
                node_ids.append(item.node_id)
        
        # ID'leri sırala (görsel düzen için)
        node_ids.sort()
        
        self.combo_start_node.addItems(node_ids)
        self.combo_end_node.addItems(node_ids)
        
        # Seçimleri korumaya çalış
        if current_start in node_ids:
            self.combo_start_node.setCurrentText(current_start)
        if current_end in node_ids:
            self.combo_end_node.setCurrentText(current_end)

    def run_algorithm(self):
        """Seçili algoritmayı çalıştırır."""
        from .visuals import NodeItem, EdgeItem
        
        algo_name = self.combo_algo.currentText()
        start_id = self.combo_start_node.currentText()
        end_id = self.combo_end_node.currentText()
        
        if not start_id:
            self.lbl_result.setText("Error: Please select a start node.")
            return

        # 1. UI Modelini Algorithm Model'ine (Graph) Dönüştür
        graph = Graph()
        
        # Once dugumleri ekle
        for item in self.canvas.scene.items():
            if isinstance(item, NodeItem):
                # UI'daki NodeItem'ın sadece ID'si ve posu var, properties şimdilik boş
                # TODO: PropertiesPanel'den güncellenen veriyi buraya çekmek gerekebilir
                model_node = Node(item.node_id, x=item.x(), y=item.y())
                graph.add_node(model_node)
        
        # Sonra kenarlari ekle
        for item in self.canvas.scene.items():
            if isinstance(item, EdgeItem):
                graph.add_edge(item.source.node_id, item.target.node_id)
                # Not: add_edge otomatik weight hesaplar. Eğer biz elle girilen 
                # ağırlığı kullanmak istersek graph.edges listesinden son eklenen edge'i bulup güncellemeliyiz.
                # Şimdilik basitçe bırakıyoruz.

        # 2. Algoritma Seçimi
        algorithm = None
        if "BFS" in algo_name:
            algorithm = BFSAlgorithm()
        elif "DFS" in algo_name:
            algorithm = DFSAlgorithm()
        elif "Dijkstra" in algo_name:
            algorithm = DijkstraAlgorithm()
        elif "A*" in algo_name:
            algorithm = AStarAlgorithm()
        else:
            self.lbl_result.setText(f"Not implemented: {algo_name}")
            return
            
        # 3. Çalıştır
        try:
            print(f"Running {algo_name} from {start_id} to {end_id}")
            result_path = algorithm.execute(graph, start_id, end_id)
            
            # 4. Sonucu Göster
            if result_path:
                result_str = " -> ".join(map(str, result_path))
                self.lbl_result.setText(f"Path: {result_str}")
                self.highlight_path(result_path)
            else:
                self.lbl_result.setText("No path found.")
                
        except Exception as e:
            self.lbl_result.setText(f"Error: {str(e)}")
            print(e)
            
    def highlight_path(self, path_ids):
        """Bulunan yolu canvas üzerinde boyar."""
        from .visuals import NodeItem, EdgeItem
        
        # Önce hepsini normale çevir (Reset)
        for item in self.canvas.scene.items():
            if isinstance(item, NodeItem):
                item.setBrush(Qt.blue) # Varsayılan renk (Mavi)
            elif isinstance(item, EdgeItem):
                item.setPen(Qt.black) # Varsayılan renk (Siyah)

        # Yolu boya
        # Düğümler
        path_items = {} # id -> NodeItem
        for item in self.canvas.scene.items():
            if isinstance(item, NodeItem) and item.node_id in path_ids:
                path_items[item.node_id] = item
                item.setBrush(Qt.red) # Seçili yol rengi (Kırmızı)
        
        # Kenarlar (Ardışık path elemanları arasındaki kenarları bul)
        for i in range(len(path_ids) - 1):
            u_id = path_ids[i]
            v_id = path_ids[i+1]
            
            for item in self.canvas.scene.items():
                if isinstance(item, EdgeItem):
                    if (item.source.node_id == u_id and item.target.node_id == v_id) or \
                       (item.source.node_id == v_id and item.target.node_id == u_id): # Yönsüz
                        pen = item.pen()
                        pen.setColor(Qt.red)
                        pen.setWidth(4)
                        item.setPen(pen)

    def create_menubar(self):
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("File")
        
        action_open = QAction("Open CSV", self)
        action_open.triggered.connect(self.load_graph)
        file_menu.addAction(action_open)
        
        action_save = QAction("Save CSV", self)
        action_save.triggered.connect(self.save_graph)
        file_menu.addAction(action_save)

    def load_graph(self):
        """CSV dosyasını açar ve ekrana çizer."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if not file_path:
            return
            
        from .visuals import NodeItem, EdgeItem
        
        graph = Graph()
        manager = CSVFileManager()
        
        if manager.load(file_path, graph):
            # Başarılı ise ekranı temizle ve yeniden çiz
            self.canvas.scene.clear()
            self.canvas.next_node_id = 1
            
            # Node'ları çiz
            node_items = {} # id -> NodeItem
            max_id = 0
            
            for node_id, node in graph.nodes.items():
                # Node(String or Int) -> Canvas Item
                # x,y zaten node içinde var (varsayılan rastgele atanmıştır graph.py içinde veya file_manager load içinde)
                # DİKKAT: CSV'de X,Y yoksa file_manager load ederken rastgele atamalıydı.
                # Node.__init__ içinde rastgele atanıyor.
                
                item = NodeItem(str(node_id), node.x, node.y)
                self.canvas.scene.addItem(item)
                node_items[node_id] = item
                
                # Gelecek için ID sayacını güncelle
                try:
                    if int(node_id) > max_id: max_id = int(node_id)
                except: pass

            # Edge'leri çiz
            for edge in graph.edges:
                source_item = node_items.get(edge.source.id)
                target_item = node_items.get(edge.target.id)
                
                if source_item and target_item:
                    # Tekrarlı çizimi engelle (Yönsüz graf)
                    # Graph edges listesinde A->B ve B->A olabilir ya da file_manager tek sefer eklemiş olabilir.
                    # Görsel olarak tek çizgi yetiyorsa kontrol et.
                    # Ama şimdilik hepsini çizmek güvenli.
                    
                    # Zaten var mı görselde?
                    exists = False
                    # (Optimize edilebilir ama şimdilik basit tutalım)
                    
                    edge_item = EdgeItem(source_item, target_item, edge.weight)
                    self.canvas.scene.addItem(edge_item)

            self.canvas.next_node_id = max_id + 1
            self.update_combos()
            self.status_bar.showMessage(f"Loaded: {file_path}")
        else:
            QMessageBox.critical(self, "Error", "Failed to load file.")

    def save_graph(self):
        """Mevcut görünümü CSV olarak kaydeder."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
        if not file_path:
            return
            
        from .visuals import NodeItem, EdgeItem
        
        # UI -> Model
        graph = Graph()
        
        # 1. Düğümler
        for item in self.canvas.scene.items():
            if isinstance(item, NodeItem):
                # Özellikleri şimdilik sabit veya random tutuyoruz
                # İleride PropertiesPanel'den güncellenen değerler NodeItem içinde saklanmalı
                node = Node(item.node_id, x=item.x(), y=item.y())
                
                # Eğer özellik panelinden güncellenmiş değerler varsa onları al
                # (Şimdilik properties_panel ile Canvas arasında tam senkronizasyon yok, basitçe yapıyoruz)
                graph.add_node(node)
                
        # 2. Kenarlar
        for item in self.canvas.scene.items():
            if isinstance(item, EdgeItem):
                graph.add_edge(item.source.node_id, item.target.node_id)

        manager = CSVFileManager()
        if manager.save(file_path, graph):
             self.status_bar.showMessage(f"Saved: {file_path}")
        else:
             QMessageBox.critical(self, "Error", "Failed to save file.")
