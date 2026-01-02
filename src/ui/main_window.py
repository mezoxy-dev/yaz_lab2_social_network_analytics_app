# GÖREV: Üye A - Arayüz Kodları
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QDockWidget, QTabWidget, QPushButton, QComboBox, QLabel, QFormLayout, QHBoxLayout, QFileDialog, QMessageBox, QAction, QDialog, QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QColor, QBrush
import time
from .canvas import GraphCanvas
from .properties_panel import PropertiesPanel
from src.model.graph import Graph
from src.model.node import Node
from src.algorithms.bfs_dfs import BFSAlgorithm, DFSAlgorithm
from src.algorithms.shortest_path import DijkstraAlgorithm, AStarAlgorithm
from src.algorithms.analysis import DegreeCentralityAlgorithm, ConnectedComponentsAlgorithm
from src.algorithms.coloring import WelshPowellAlgorithm
from src.model.file_manager import CSVFileManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sosyal Ağ Analizi (Social Network Analysis)")
        self.setGeometry(100, 100, 1200, 800) # Biraz daha geniş başlasın
        
        # stili uygula (baslangic %100)
        from .styles import get_stylesheet
        self.current_scale = 1.0
        self.setStyleSheet(get_stylesheet(self.current_scale))
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        self.canvas = GraphCanvas(self)
        self.layout.addWidget(self.canvas)
        
        # algoritma ismi overlay
        self.lbl_algo_overlay = QLabel("", self.canvas)
        # daha profesyonel gorunum:
        # - segoe ui font (windows standardi) veya helvetica
        # - hafif golge efekti (border)
        # - yari saydam koyu arka plan + beyaz yazi (hud tarzi) veya tam tersi
        self.lbl_algo_overlay.setStyleSheet("""
            QLabel {
                background-color: rgba(30, 30, 30, 220); 
                color: #ecf0f1; 
                font-family: 'Segoe UI', sans-serif;
                font-size: 18px; 
                font-weight: 600; 
                padding: 12px 16px; 
                border-radius: 6px;
                border: 1px solid #555;
            }
        """)
        self.lbl_algo_overlay.hide()
        
        # bilgi overlay (sol ust)
        self.lbl_info_overlay = QLabel(
            "Sol Tık + Sürükle = Çoklu Seçim\n"
            "Delete Tuşu = Seçileni Sil", 
            self.canvas
        )
        self.lbl_info_overlay.setStyleSheet("""
            QLabel {
                background-color: rgba(255, 255, 255, 180);
                color: #2c3e50;
                font-family: 'Segoe UI', sans-serif;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
            }
        """)
        self.lbl_info_overlay.adjustSize()
        self.lbl_info_overlay.show()
        
        # panelleri olustur
        self.create_dock_panels()
        
        # menu bar (dock paneller olustuktan sonra cagrilmali)
        self.create_menu_bar()
        
        # sinyal baglantilari
        self.canvas.scene.selectionChanged.connect(self.on_selection_changed)
        self.canvas.itemMoved.connect(self.properties_panel.update_selection)
        self.canvas.nodeAdded.connect(self.update_combos)
        self.canvas.nodeDeleted.connect(self.update_combos)
        
        # status bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")

        # animasyon icin timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_step)
        self.animation_queue = []
        self.animation_visited = set()
        self.animation_path_edges = [] # [(u, v), ...]


    def set_zoom(self, scale_factor):
        """Arayüzü belirtilen oranda ölçekler."""
        print(f"Zoom set to: {scale_factor*100}%")
        self.current_scale = scale_factor
        
        # Stili Yeniden Oluştur ve Uygula
        from .styles import get_stylesheet
        self.setStyleSheet(get_stylesheet(self.current_scale))
        
        self.status_bar.showMessage(f"Arayüz ölçeği: %{int(scale_factor*100)}")

    def create_dock_panels(self):
        # --- sag panel (ozellikler) ---
        self.properties_dock = QDockWidget("Özellikler (Properties)", self)
        self.properties_dock.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)
        self.properties_panel = PropertiesPanel()
        self.properties_dock.setWidget(self.properties_panel)
        self.addDockWidget(Qt.RightDockWidgetArea, self.properties_dock)
        
        # --- sol panel (kontrol / analiz) ---
        self.control_dock = QDockWidget("Kontrol Paneli (Control Panel)", self)
        self.control_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        
        # tab yapisi (edit / analysis)
        self.tabs = QTabWidget()
        self.setup_edit_tab()
        self.setup_analysis_tab()
        
        self.control_dock.setWidget(self.tabs)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.control_dock)

    def setup_edit_tab(self):
        """duzenleme islevleri icin sekme"""
        edit_widget = QWidget()
        layout = QVBoxLayout(edit_widget)
        
        # butonlar (turkce)
        btn_select = QPushButton("Seçim Modu (Select)")
        btn_add_node = QPushButton("Düğüm Ekle (Add Node)")
        btn_add_edge = QPushButton("Kenar Ekle (Add Edge)")
        btn_clear = QPushButton("Temizle (Clear)")
        
        # temizle butonu icin ozel kirmizi stil
        btn_clear.setStyleSheet("background-color: #e74c3c; color: white;")
        
        layout.addWidget(btn_select)
        layout.addWidget(btn_add_node)
        layout.addWidget(btn_add_edge)
        layout.addStretch() # Boşluğu alta it
        layout.addWidget(btn_clear)
        
        self.tabs.addTab(edit_widget, "Düzenle (Edit)")
        
        # Bağlantılar
        btn_select.clicked.connect(lambda: self.canvas.set_mode("SELECT"))
        btn_add_node.clicked.connect(lambda: self.canvas.set_mode("ADD_NODE"))
        btn_add_edge.clicked.connect(lambda: self.canvas.set_mode("ADD_EDGE"))
        btn_clear.clicked.connect(self.canvas.scene.clear)

    def setup_analysis_tab(self):
        """algoritma analizi islevleri icin sekme"""
        analysis_widget = QWidget()
        layout = QVBoxLayout(analysis_widget)
        
        # algoritma secimi
        layout.addWidget(QLabel("Algoritma:"))
        self.combo_algo = QComboBox()
        self.combo_algo.addItems([
            "Dijkstra Shortest Path",
            "A* Shortest Path",
            "BFS (Breadth-First)",
            "DFS (Depth-First)",
            "Welsh-Powell Coloring",
            "Connected Components (Clustering)",
            "Degree Centrality"
        ])
        layout.addWidget(self.combo_algo)
        
        # baslangic / bitis node secimi
        self.lbl_start_node = QLabel("Başlangıç Düğümü:")
        layout.addWidget(self.lbl_start_node)
        self.combo_start_node = QComboBox()
        layout.addWidget(self.combo_start_node)
        
        self.lbl_end_node = QLabel("Bitiş (Hedef) Düğümü:")
        layout.addWidget(self.lbl_end_node)
        self.combo_end_node = QComboBox()
        layout.addWidget(self.combo_end_node)
        
        # animasyon checkbox
        self.chk_animate = QCheckBox("Animasyonlu Çalıştır")
        self.chk_animate.setChecked(True)
        layout.addWidget(self.chk_animate)
        
        # calistir butonu
        self.btn_run = QPushButton("Analizi Başlat (Run)")
        self.btn_run.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 10px;") # Yeşil
        layout.addWidget(self.btn_run)
        
        # sure gostergesi
        layout.addWidget(QLabel("Çalışma Süresi:"))
        self.lbl_time = QLabel("-")
        self.lbl_time.setStyleSheet("font-weight: bold; color: #e74c3c; border: 1px solid #bdc3c7; padding: 4px; border-radius: 4px; background: white;")
        layout.addWidget(self.lbl_time)

        # sonuc alani
        layout.addWidget(QLabel("Sonuç (Çıktı):"))
        self.lbl_result = QLabel("Hazır")
        self.lbl_result.setWordWrap(True)
        self.lbl_result.setStyleSheet("border: 1px solid #bdc3c7; padding: 8px; background: white; border-radius: 4px;")
        layout.addWidget(self.lbl_result)
        
        # tablo sonuc butonu
        self.btn_show_table = QPushButton("Tabloda Göster (Show Table)")
        self.btn_show_table.setStyleSheet("background-color: #7f8c8d; color: white; padding: 6px;")
        self.btn_show_table.setEnabled(False) # sonuc olusana kadar pasif
        layout.addWidget(self.btn_show_table)
        
        layout.addStretch()
        self.tabs.addTab(analysis_widget, "Analiz (Analysis)")
        
        # signal baglantisi
        self.btn_run.clicked.connect(self.run_algorithm)
        self.btn_show_table.clicked.connect(self.show_result_table)
        self.combo_algo.currentIndexChanged.connect(self.update_input_fields)
        
        # ilk acilista guncelle
        self.update_input_fields()
        
        # sonuc saklama
        self.last_result = None
        self.last_algo_type = None

    def update_input_fields(self):
        """secili algoritmaya gore input alanlarini gizle/goster."""
        algo = self.combo_algo.currentText()
        
        show_start = True
        show_end = True
        
        if "BFS" in algo or "DFS" in algo:
            show_end = False # traversals don't need end node
        elif "Clustering" in algo or "Coloring" in algo or "Centrality" in algo:
            show_start = False
            show_end = False # global algorithms don't need inputs
            
        self.lbl_start_node.setVisible(show_start)
        self.combo_start_node.setVisible(show_start)
        self.lbl_end_node.setVisible(show_end)
        self.combo_end_node.setVisible(show_end)

    def on_selection_changed(self):
        items = self.canvas.scene.selectedItems()
        if items:
            self.properties_panel.update_selection(items[0])
        else:
            self.properties_panel.update_selection(None)

    def update_combos(self):
        """combobox'lari kandaki dugumlerle gunceller."""
        from .visuals import NodeItem # Döngüsel importu önlemek için burada
        
        current_start = self.combo_start_node.currentText()
        current_end = self.combo_end_node.currentText()
        
        self.combo_start_node.clear()
        self.combo_end_node.clear()
        
        node_ids = []
        for item in self.canvas.scene.items():
            if isinstance(item, NodeItem):
                node_ids.append(item.node_id)
        
        # id'leri sirala (gorsel duzen icin)
        node_ids.sort()
        
        self.combo_start_node.addItems(node_ids)
        self.combo_end_node.addItems(node_ids)
        
        # secimleri korumaya calis
        if current_start in node_ids:
            self.combo_start_node.setCurrentText(current_start)
        if current_end in node_ids:
            self.combo_end_node.setCurrentText(current_end)


            
    def highlight_path(self, path_ids):
        """bulunan yolu canvas uzerinde boyar."""
        from .visuals import NodeItem, EdgeItem
        
        # once hepsini normale cevir (reset)
        for item in self.canvas.scene.items():
            if isinstance(item, NodeItem):
                item.setBrush(Qt.blue) # varsayilan renk (mavi)
            elif isinstance(item, EdgeItem):
                item.setPen(Qt.black) # varsayilan renk (siyah)

        # yolu boya
        # dugumler
        path_items = {} # id -> nodeitem
        for item in self.canvas.scene.items():
            if isinstance(item, NodeItem) and item.node_id in path_ids:
                path_items[item.node_id] = item
                item.setBrush(Qt.red) # secili yol rengi (kirmizi)
        
        # kenarlar (ardisik path elemanlari arasindaki kenarlari bul)
        for i in range(len(path_ids) - 1):
            u_id = path_ids[i]
            v_id = path_ids[i+1]
            
            for item in self.canvas.scene.items():
                if isinstance(item, EdgeItem):
                    if (item.source.node_id == u_id and item.target.node_id == v_id) or \
                       (item.source.node_id == v_id and item.target.node_id == u_id): # yonsuz
                        pen = item.pen()
                        pen.setColor(Qt.red)
                        pen.setWidth(4)
                        item.setPen(pen)

    def apply_coloring(self, node_colors):
        """dugumleri verilen renklere gore boyar (dict: {id: #hexcode})."""
        from .visuals import NodeItem
        from PyQt5.QtGui import QColor, QBrush
        
        # once reset
        for item in self.canvas.scene.items():
            if isinstance(item, NodeItem):
                item.setBrush(QBrush(QColor("#3498db"))) # reset to default blue
        
        # sonra boya
        for item in self.canvas.scene.items():
            if isinstance(item, NodeItem):
                if item.node_id in node_colors:
                    color_code = node_colors[item.node_id]
                    item.setBrush(QBrush(QColor(color_code)))

    def show_result_table(self):
        """sonuclari tablo olarak gosterir."""
        from PyQt5.QtWidgets import QAbstractItemView
        from PyQt5.QtGui import QColor, QBrush # safety import
        if not self.last_result:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle(f"Result Table - {self.last_algo_type}")
        dialog.resize(600, 400)
        layout = QVBoxLayout(dialog)
        
        table = QTableWidget()
        table.setEditTriggers(QAbstractItemView.NoEditTriggers) # salt okunur
        layout.addWidget(table)
        
        # helper to get node name
        from .visuals import NodeItem
        def get_node_name_by_id(nid):
            for item in self.canvas.scene.items():
                if isinstance(item, NodeItem) and item.node_id == nid:
                    return getattr(item, 'label_text', str(nid))
            return str(nid)

        if self.last_algo_type == "Path" or self.last_algo_type == "Traversal":
            # list of node ids
            # "order" sutunu kaldirildi (satir numarasi zaten var)
            headers = ["Node ID", "Name"]
            if self.last_algo_type == "Path":
                headers.append("Cumulative Cost (Approx)") # basitlik icin
                
            table.setColumnCount(len(headers))
            table.setHorizontalHeaderLabels(headers)
            table.setRowCount(len(self.last_result))
            
            for i, node_id in enumerate(self.last_result):
                table.setItem(i, 0, QTableWidgetItem(str(node_id)))
                table.setItem(i, 1, QTableWidgetItem(get_node_name_by_id(node_id)))
                if self.last_algo_type == "Path":
                    # gercek maliyeti graph uzerinden hesaplamak lazim ama simdilik bos gecelim veya
                    # run_algorithm icinde hesaplanip buraya object olarak gelmeliydi.
                    # istege gore burasi gelistirilebilir.
                    table.setItem(i, 2, QTableWidgetItem("-"))

        elif self.last_algo_type == "Coloring":
            # dict: {nodeid: hexcode}
            headers = ["Node ID", "Name", "Color Code"]
            table.setColumnCount(len(headers))
            table.setHorizontalHeaderLabels(headers)
            table.setRowCount(len(self.last_result))
            
            for i, (node_id, color) in enumerate(self.last_result.items()):
                table.setItem(i, 0, QTableWidgetItem(str(node_id)))
                table.setItem(i, 1, QTableWidgetItem(get_node_name_by_id(node_id)))
                
                item = QTableWidgetItem(str(color))
                item.setBackground(QColor(color))
                if color == "#000000": item.setForeground(QColor("white"))
                table.setItem(i, 2, item)

        elif self.last_algo_type == "Clustering":
            # list of lists: [[id, id], [id]]
            headers = ["Cluster ID", "Node Count", "Nodes"]
            table.setColumnCount(len(headers))
            table.setHorizontalHeaderLabels(headers)
            table.setRowCount(len(self.last_result))
            
            for i, component in enumerate(self.last_result):
                table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
                table.setItem(i, 1, QTableWidgetItem(str(len(component))))
                
                names = [f"{nid} ({get_node_name_by_id(nid)})" for nid in component]
                # cok uzun olmasin, ilk 10 tanesini goster
                content = ", ".join(names[:10])
                if len(names) > 10: content += f" ... (+{len(names)-10} more)"
                
                table.setItem(i, 2, QTableWidgetItem(content))
        
        elif self.last_algo_type == "Centrality":
             # list of tuples: [(id, score), ...]
            headers = ["Rank", "Node ID", "Name", "Score"]
            table.setColumnCount(len(headers))
            table.setHorizontalHeaderLabels(headers)
            table.setRowCount(len(self.last_result))
            
            for i, (node_id, score) in enumerate(self.last_result):
                table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
                table.setItem(i, 1, QTableWidgetItem(str(node_id)))
                table.setItem(i, 2, QTableWidgetItem(get_node_name_by_id(node_id)))
                table.setItem(i, 3, QTableWidgetItem(f"{score:.4f}"))

        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        btn_close = QPushButton("Close")
        btn_close.clicked.connect(dialog.accept)
        layout.addWidget(btn_close)
        
        dialog.exec_()

    def show_centrality_results(self, scores):
        """merkezilik skorlarini bir tabloda gosterir."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Degree Centrality Results")
        dialog.resize(400, 300)
        
        layout = QVBoxLayout(dialog)
        
        table = QTableWidget()
        table.setEditTriggers(QAbstractItemView.NoEditTriggers) # salt okunur
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Node ID", "Degree Score"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # en yuksek 5 tanesini goster
        top_scores = scores[:5]
        table.setRowCount(len(top_scores))
        
        for i, (node_id, score) in enumerate(top_scores):
            table.setItem(i, 0, QTableWidgetItem(str(node_id)))
            table.setItem(i, 1, QTableWidgetItem(str(score)))
            
        layout.addWidget(table)
        
        btn_close = QPushButton("Close")
        btn_close.clicked.connect(dialog.accept)
        layout.addWidget(btn_close)
        
        dialog.exec_()

    def start_animation(self, node_list, is_path=False):
        """animasyonu baslatir."""
        self.animation_queue = list(node_list) # kopyasini al ki last_result bozulmasin
        self.animation_is_path = is_path
        self.animation_visited.clear()
        
        # reset canvas
        from .visuals import NodeItem, EdgeItem
        from PyQt5.QtGui import QColor, QBrush
        
        for item in self.canvas.scene.items():
            if isinstance(item, NodeItem):
                item.setBrush(QBrush(QColor("#3498db"))) # mavi
            elif isinstance(item, EdgeItem):
                item.setPen(Qt.black)

        self.timer.start(300) # 300ms gecikme
        self.btn_run.setEnabled(False) 
        self.btn_show_table.setEnabled(False) # animasyon bitene kadar sonuc gosterme
        self.status_bar.showMessage("Animating...")

    def animate_step(self):
        """timer her tetiklendiginde calisir."""
        from .visuals import NodeItem, EdgeItem
        from PyQt5.QtGui import QColor, QBrush
        
        if not self.animation_queue:
            self.timer.stop()
            self.btn_run.setEnabled(True)
            if self.last_result: # eger sonuc varsa butonu ac
                self.btn_show_table.setEnabled(True)
            self.status_bar.showMessage("Animation Completed.")
            
            # eger path animasyonu ise, kenarlari da son asamada kirmizi yapalim tam gorunsun
            if self.animation_is_path:
                # (highlight_path fonksiyonunu cagirabiliriz veya burada manuel yapariz)
                pass
            return

        current_id = self.animation_queue.pop(0)
        self.animation_visited.add(current_id)
        
        # ilgili dugumu bul ve boya
        for item in self.canvas.scene.items():
            if isinstance(item, NodeItem) and item.node_id == current_id:
                if self.animation_is_path:
                    item.setBrush(QBrush(QColor("#e74c3c"))) # kirmizi (path)
                else:
                    item.setBrush(QBrush(QColor("#f39c12"))) # turuncu (ziyaret edilen)
                break
        
        # eger path ise bir onceki ile baglantiyi da boya
        # (bu basit animasyon, sadece node'lari yakar sonuk yapar)

    def run_algorithm(self):
        """secili algoritmaya gore calistir."""
        from .visuals import NodeItem, EdgeItem
        
        algo_name = self.combo_algo.currentText()
        start_id = self.combo_start_node.currentText()
        end_id = self.combo_end_node.currentText()
        
        # ... (validasyonlar ayni kalacak, sadece execute sonrasi degisecek)
        
        if not start_id and "Coloring" not in algo_name and "Clustering" not in algo_name and "Centrality" not in algo_name:
            self.lbl_result.setText("Error: Please select a start node.")
            return

        graph = Graph()
        # graph olusturma kismi ayni...
        for item in self.canvas.scene.items():
            if isinstance(item, NodeItem):
                props = item.properties if hasattr(item, 'properties') else {}
                model_node = Node(item.node_id, properties=props, x=item.x(), y=item.y())
                graph.add_node(model_node)
        for item in self.canvas.scene.items():
            if isinstance(item, EdgeItem):
                graph.add_edge(item.source.node_id, item.target.node_id)

        # algoritma nesnesi
        algorithm = None
        if "BFS" in algo_name: algorithm = BFSAlgorithm()
        elif "DFS" in algo_name: algorithm = DFSAlgorithm()
        elif "Dijkstra" in algo_name: algorithm = DijkstraAlgorithm()
        elif "A*" in algo_name: algorithm = AStarAlgorithm()
        elif "Coloring" in algo_name: algorithm = WelshPowellAlgorithm()
        elif "Clustering" in algo_name: algorithm = ConnectedComponentsAlgorithm()
        elif "Degree Centrality" in algo_name: algorithm = DegreeCentralityAlgorithm()
        else:
            self.lbl_result.setText(f"Not implemented: {algo_name}")
            return
            
        # DEBUG: Check if weights are all 1.0 (implying missing properties)
        weights = [e.weight for e in graph.edges]
        if weights and all(w == 1.0 for w in weights):
            print("WARNING: All edge weights are 1.0! Node properties might be missing.")
            QMessageBox.warning(self, "Data Warning", "All edge weights are 1.0!\n\nThis usually means node properties (Active, Interaction, etc.) are missing or zero.\n\nShortest Path will behave like BFS (fewest hops).")
            
        try:
            print(f"Running {algo_name}")
            
            # overlay guncelle
            self.lbl_algo_overlay.setText(f"Active Algorithm: {algo_name}")
            self.lbl_algo_overlay.adjustSize()
            self.lbl_algo_overlay.show()
            self.update_overlay_pos()
            
            start_time = time.time()
            
            # 1. renklendirme ve analizler (animasyonsuz veya farkli)
            if isinstance(algorithm, WelshPowellAlgorithm):
                colors = algorithm.execute(graph)
                elapsed_time = (time.time() - start_time) * 1000
                self.lbl_time.setText(f"{elapsed_time:.2f} ms")
                
                self.apply_coloring(colors)
                self.lbl_result.setText(f"Coloring applied. Total colors: {len(set(colors.values()))}")
                
                self.last_result = colors
                self.last_algo_type = "Coloring"
                self.btn_show_table.setEnabled(True)
                return
                
            elif isinstance(algorithm, ConnectedComponentsAlgorithm):
                components = algorithm.execute(graph)
                elapsed_time = (time.time() - start_time) * 1000
                self.lbl_time.setText(f"{elapsed_time:.2f} ms")
                
                # ... Renklendirme kodu ...
                colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF", "#FFA500", "#800080", "#008080", "#FFC0CB", "#800000", "#008000"]
                node_colors_map = {}
                for i, component in enumerate(components):
                    color = colors[i % len(colors)]
                    for node_id in component:
                        node_colors_map[node_id] = color
                self.apply_coloring(node_colors_map)
                self.lbl_result.setText(f"Components found: {len(components)}. Coloring applied.")
                
                self.last_result = components
                self.last_algo_type = "Clustering"
                self.btn_show_table.setEnabled(True)
                return
            
            elif isinstance(algorithm, DegreeCentralityAlgorithm):
                scores = algorithm.execute(graph)
                elapsed_time = (time.time() - start_time) * 1000
                self.lbl_time.setText(f"{elapsed_time:.2f} ms")
                
                self.show_centrality_results(scores)
                self.lbl_result.setText(f"Centrality scores calculated.")
                
                self.last_result = scores
                self.last_algo_type = "Centrality"
                self.btn_show_table.setEnabled(True)
                return 

            # 2. gezinti ve yol algoritmalari (animasyonlu)
            result_list = algorithm.execute(graph, start_id, end_id)
            elapsed_time = (time.time() - start_time) * 1000
            self.lbl_time.setText(f"{elapsed_time:.2f} ms")
            
            if not result_list:
                self.lbl_result.setText(f"No path/result found.")
                self.last_result = None
                self.btn_show_table.setEnabled(False)
                return

            result_str = " -> ".join(map(str, result_list))
            self.lbl_result.setText(f"{result_str}")
            
            # sonucu sakla
            self.last_result = result_list
            if "BFS" in algo_name or "DFS" in algo_name:
                self.last_algo_type = "Traversal"
            else:
                self.last_algo_type = "Path"
            self.btn_show_table.setEnabled(True)
            
            # animasyon isteniyor mu?
            if self.chk_animate.isChecked():
                # path mi yoksa visited list mi?
                # bfs/dfs visited doner (butun gezilenler)
                # dijkstra/a* path doner (sadece en kisa yol)
                is_path = "Shortest" in algo_name
                self.start_animation(result_list, is_path=is_path)
            else:
                self.highlight_path(result_list)
                
        except Exception as e:
            self.lbl_result.setText(f"Error: {str(e)}")
            print(e)
            import traceback
            traceback.print_exc()

            import traceback
            traceback.print_exc()

    def create_menu_bar(self):
        menubar = self.menuBar()
        menubar.clear() # temiz bir baslangic

        # --- dosya (file) menusu ---
        file_menu = menubar.addMenu("File")
        
        action_open = QAction("Open CSV", self)
        action_open.triggered.connect(self.load_graph)
        file_menu.addAction(action_open)
        
        action_save = QAction("Save CSV", self)
        action_save.triggered.connect(self.save_graph)
        file_menu.addAction(action_save)
        
        # --- gorunum (view) menusu ---
        # kullanici istegi: sadece "view" yazsin
        view_menu = menubar.addMenu("View")
        
        # Layout
        action_layout = QAction("Auto Layout (Force-Directed)", self)
        action_layout.triggered.connect(self.apply_layout)
        view_menu.addAction(action_layout)
        
        view_menu.addSeparator()

        # Zoom Seçenekleri
        zoom_50 = QAction("Zoom %50", self)
        zoom_50.triggered.connect(lambda: self.set_zoom(0.5))
        
        zoom_75 = QAction("Zoom %75", self)
        zoom_75.triggered.connect(lambda: self.set_zoom(0.75))

        zoom_100 = QAction("Zoom %100 (Default)", self)
        zoom_100.triggered.connect(lambda: self.set_zoom(1.0))
        
        zoom_150 = QAction("Zoom %150", self)
        zoom_150.triggered.connect(lambda: self.set_zoom(1.5))
        
        zoom_200 = QAction("Zoom %200", self)
        zoom_200.triggered.connect(lambda: self.set_zoom(2.0))
        
        view_menu.addAction(zoom_50)
        view_menu.addAction(zoom_75)
        view_menu.addAction(zoom_100)
        view_menu.addAction(zoom_150)
        view_menu.addAction(zoom_200)
        
        view_menu.addSeparator()
        
        # dock gorunurlukleri
        view_menu.addAction(self.control_dock.toggleViewAction())
        view_menu.addAction(self.properties_dock.toggleViewAction())

    def load_graph(self):
        """csv dosyasini acar ve ekrana cizer."""
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
            
            # node'lari ciz
            node_items = {} # id -> nodeitem
            max_id = 0
            
            for node_id, node in graph.nodes.items():
                # node(string or int) -> canvas item
                # x,y zaten node icinde var (varsayilan rastgele atanmistir graph.py icinde veya file_manager load icinde)
                # dikkat: csv'de x,y yoksa file_manager load ederken rastgele atamaliydi.
                # node.__init__ icinde rastgele ataniyor.
                
                # id, x, y ve ozellikleri nodeitem'a aktar
                props = {
                    'aktiflik': node.aktiflik,
                    'etkilesim': node.etkilesim,
                    'baglanti_sayisi': 0 # sifirdan baslat, kenarlar eklendikce artacak
                }
                item = NodeItem(str(node_id), node.x, node.y, properties=props, label=node.name)
                self.canvas.scene.addItem(item)
                node_items[node_id] = item
                
                # gelecek icin id sayacini guncelle
                try:
                    if int(node_id) > max_id: max_id = int(node_id)
                except: pass

            # edge'leri ciz
            for edge in graph.edges:
                source_item = node_items.get(edge.source.id)
                target_item = node_items.get(edge.target.id)
                
                if source_item and target_item:
                    # kararli cizimi engelle (yonsuz graf)
                    # graph edges listesinde a->b ve b->a olabilir ya da file_manager tek sefer eklemis olabilir.
                    # gorsel olarak tek cizgi yetiyorsa kontrol et.
                    # ama simdilik hepsini cizmek guvenli.
                    
                    # zaten var mi gorselde?
                    exists = False
                    # (optimize edilebilir ama simdilik basit tutalim)
                    
                    edge_item = EdgeItem(source_item, target_item, edge.weight)
                    self.canvas.scene.addItem(edge_item)

            self.canvas.next_node_id = max_id + 1
            self.update_combos()
            self.status_bar.showMessage(f"Loaded: {file_path}")
        else:
            QMessageBox.critical(self, "Error", "Failed to load file.")

    def save_graph(self):
        """mevcut gorunumu csv olarak kaydeder."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
        if not file_path:
            return
            
        from .visuals import NodeItem, EdgeItem
        
        # ui -> model
        graph = Graph()
        
        # 1. dugumler
        for item in self.canvas.scene.items():
            if isinstance(item, NodeItem):
                # Özellikleri şimdilik sabit veya random tutuyoruz
                # İleride PropertiesPanel'den güncellenen değerler NodeItem içinde saklanmalı
                # Özellikleri koru
                props = item.properties if hasattr(item, 'properties') else {}
                node = Node(item.node_id, properties=props, x=item.x(), y=item.y())
                
                # eger ozellik panelinden guncellenmis degerler varsa onlari al
                # (simdilik properties_panel ile canvas arasinda tam senkronizasyon yok, basitce yapiyoruz)
                graph.add_node(node)
                
        # 2. kenarlar
        for item in self.canvas.scene.items():
            if isinstance(item, EdgeItem):
                graph.add_edge(item.source.node_id, item.target.node_id)

        manager = CSVFileManager()
        if manager.save(file_path, graph):
             self.status_bar.showMessage(f"Saved: {file_path}")
        else:
             QMessageBox.critical(self, "Error", "Failed to save file.")

    def apply_layout(self):
        """grafa otomatik duzen (spring layout) uygular."""
        from src.algorithms.layout import SpringLayout
        from src.ui.visuals import NodeItem, EdgeItem
        
        node_items = [item for item in self.canvas.scene.items() if isinstance(item, NodeItem)]
        edge_items = [item for item in self.canvas.scene.items() if isinstance(item, EdgeItem)]
        
        if not node_items: return
        
        self.status_bar.showMessage("Applying layout...")
        # arayuz donmasin diye processevents yapilabilir ama 50 iterasyon hizli surer
        
        layout = SpringLayout(800, 600)
        new_positions = layout.calculate_layout(node_items, edge_items)
        
        for node in node_items:
            if node.node_id in new_positions:
                x, y = new_positions[node.node_id]
                node.setPos(x, y)
                # dugum hareket edince kenarlar otomatik guncellenir (itemchange ile).
        
        
        self.status_bar.showMessage("Layout applied.")

    def update_overlay_pos(self):
        """overlay etiketini sag/sol ust koseye sabitler."""
        if hasattr(self, 'lbl_algo_overlay') and self.lbl_algo_overlay.isVisible():
            # sag ust (right top)
            canvas_width = self.canvas.width()
            label_width = self.lbl_algo_overlay.width()
            margin_right = 30 # scrollbar payi vs.
            margin_top = 20
            
            x = canvas_width - label_width - margin_right
            y = margin_top
            
            self.lbl_algo_overlay.move(x, y)
            
        if hasattr(self, 'lbl_info_overlay') and self.lbl_info_overlay.isVisible():
            # sol ust (left top)
            # direkt 10,10 konumuna (canvas'a relative olarak)
            self.lbl_info_overlay.move(10, 10)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_overlay_pos()
