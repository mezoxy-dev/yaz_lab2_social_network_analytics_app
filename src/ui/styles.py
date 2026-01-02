
"""
modern ui stylesheet for social network analysis app
theme: professional, minimalist, clean
colors:
- background: #f5f6fa (light grey)
- surface: #ffffff (white)
- primary: #3498db (blue)
- primary hover: #2980b9
- text: #2c3e50 (dark blue/grey)
- border: #dcdde1
"""


def get_stylesheet(scale_factor=1.0):
    """
    olcek factorune gore stylesheet olusturur.
    scale_factor: 1.0 = %100, 1.5 = %150 vb.
    """
    # baz font boyutlari (kullanici dahi buyuk istedigi icin 14 -> 18 yaptik)
    font_size_base = int(18 * scale_factor)
    font_size_title = int(20 * scale_factor)
    
    # padding ve margin'leri de olcekle
    padding_base = int(8 * scale_factor)
    padding_small = int(4 * scale_factor)
    border_radius = int(4 * scale_factor)

    return f"""
/* genel uygulama ayarlari */
QWidget {{
    font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
    font-size: {font_size_base}px;
    color: #2c3e50;
    selection-background-color: #3498db;
    selection-color: white;
}}

/* ana pencere */
QMainWindow {{
    background-color: #f5f6fa;
}}

QDockWidget::title {{
    text-align: left;
    background-color: #ecf0f1;
    padding: {padding_base}px;
    border-radius: {border_radius}px;
    font-weight: bold;
    font-size: {font_size_title}px;
}}

/* tab widget */
QTabWidget::pane {{
    border: 1px solid #dcdde1;
    background: white;
    border-radius: {border_radius}px;
    top: -1px; 
}}

QTabBar::tab {{
    background: #ecf0f1;
    border: 1px solid #dcdde1;
    padding: {padding_base}px {2*padding_base}px;
    margin-right: 2px;
    border-top-left-radius: {border_radius}px;
    border-top-right-radius: {border_radius}px;
    color: #7f8c8d;
}}

QTabBar::tab:selected {{
    background: white;
    border-bottom-color: white; 
    color: #2c3e50;
    font-weight: bold;
}}

/* butonlar */
QPushButton {{
    background-color: #3498db;
    color: white;
    border: none;
    padding: {padding_base}px {2*padding_base}px;
    border-radius: {border_radius}px;
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: #2980b9;
}}

/* input alanlari */
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
    padding: {padding_base-2}px;
    border: 1px solid #dcdde1;
    border-radius: {border_radius}px;
    background-color: white;
    min-height: {int(20 * scale_factor)}px;
}}

/* tablolar */
QTableWidget {{
    background-color: white;
    alternate-background-color: #f9f9f9;
    gridline-color: #ecf0f1;
    border: 1px solid #dcdde1;
}}

QHeaderView::section {{
    background-color: #ecf0f1;
    padding: {padding_base}px;
    border: none;
    border-right: 1px solid #dcdde1;
    border-bottom: 1px solid #dcdde1;
    font-weight: bold;
    color: #2c3e50;
}}
"""
