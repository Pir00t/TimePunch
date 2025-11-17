"""
Theme stylesheets for TimePunch
"""


def get_stylesheet(dark_mode=True):
	"""Return stylesheet based on theme"""
	if dark_mode:
		return """
			QMainWindow, QWidget {
				background-color: #1e1e1e;
				color: #e0e0e0;
				font-size: 13px;
			}
			QLineEdit, QComboBox {
				background-color: #2d2d2d;
				color: #e0e0e0;
				border: 2px solid #00d9ff;
				border-radius: 8px;
				padding: 8px;
				font-size: 13px;
			}
			QLineEdit:focus, QComboBox:focus {
				border-color: #00ffff;
				background-color: #333333;
			}
			QPushButton {
				background-color: #00d9ff;
				color: #1e1e1e;
				border: none;
				border-radius: 8px;
				padding: 8px 16px;
				font-size: 14px;
				font-weight: bold;
			}
			QPushButton#actionButton {
				background-color: #3d3d3d;
				color: #00d9ff;
				border: 1px solid #00d9ff;
				border-radius: 4px;
				padding: 8px 12px;
				font-size: 13px;
				font-weight: bold;
			}
			QPushButton#actionButton:hover {
				background-color: #4d4d4d;
				color: #00ffff;
			}
			QPushButton:hover {
				background-color: #00ffff;
			}
			QPushButton:pressed {
				background-color: #00b8d4;
			}
			QPushButton:disabled {
				background-color: #3d3d3d;
				color: #666666;
			}
			#timerFrame {
				background-color: #2d2d2d;
				border: 2px solid #00d9ff;
				border-radius: 12px;
				padding: 20px;
				margin: 10px 0;
			}
			QTableWidget {
				background-color: #2d2d2d;
				alternate-background-color: #252525;
				gridline-color: #3d3d3d;
				border: none;
				border-radius: 8px;
			}
			QTableWidget::item {
				padding: 8px;
				color: #e0e0e0;
			}
			QTableWidget::item:selected {
				background-color: #00d9ff;
				color: #1e1e1e;
			}
			QHeaderView::section {
				background-color: #3d3d3d;
				color: #e0e0e0;
				padding: 10px;
				border: none;
				font-weight: bold;
				font-size: 12px;
			}
			QLabel {
				color: #e0e0e0;
			}
			QTextEdit {
				background-color: #2d2d2d;
				color: #e0e0e0;
				border: 1px solid #3d3d3d;
				border-radius: 4px;
				padding: 8px;
				font-family: 'Courier New', monospace;
				font-size: 12px;
			}
			QDialog {
				background-color: #1e1e1e;
			}
		"""
	else:
		return """
			QMainWindow, QWidget {
				background-color: #f5f6fa;
				color: #2c3e50;
				font-size: 13px;
			}
			QLineEdit, QComboBox {
				background-color: #ffffff;
				color: #2c3e50;
				border: 2px solid #3498db;
				border-radius: 8px;
				padding: 8px;
				font-size: 13px;
			}
			QLineEdit:focus, QComboBox:focus {
				border-color: #2980b9;
				background-color: #ecf0f1;
			}
			QPushButton {
				background-color: #3498db;
				color: #ffffff;
				border: none;
				border-radius: 8px;
				padding: 8px 16px;
				font-size: 14px;
				font-weight: bold;
			}
			QPushButton#actionButton {
				background-color: #ffffff;
				color: #3498db;
				border: 1px solid #3498db;
				border-radius: 4px;
				padding: 8px 12px;
				font-size: 13px;
				font-weight: bold;
			}
			QPushButton#actionButton:hover {
				background-color: #ecf0f1;
				color: #2980b9;
			}
			QPushButton:hover {
				background-color: #2980b9;
			}
			QPushButton:pressed {
				background-color: #21618c;
			}
			QPushButton:disabled {
				background-color: #bdc3c7;
				color: #7f8c8d;
			}
			#timerFrame {
				background-color: #ffffff;
				border: 2px solid #3498db;
				border-radius: 12px;
				padding: 20px;
				margin: 10px 0;
			}
			QTableWidget {
				background-color: #ffffff;
				alternate-background-color: #ecf0f1;
				gridline-color: #bdc3c7;
				border: none;
				border-radius: 8px;
			}
			QTableWidget::item {
				padding: 8px;
				color: #2c3e50;
			}
			QTableWidget::item:selected {
				background-color: #3498db;
				color: #ffffff;
			}
			QHeaderView::section {
				background-color: #bdc3c7;
				color: #2c3e50;
				padding: 10px;
				border: none;
				font-weight: bold;
				font-size: 12px;
			}
			QLabel {
				color: #2c3e50;
			}
			QTextEdit {
				background-color: #ffffff;
				color: #2c3e50;
				border: 1px solid #bdc3c7;
				border-radius: 4px;
				padding: 8px;
				font-family: 'Courier New', monospace;
				font-size: 12px;
			}
			QDialog {
				background-color: #f5f6fa;
			}
		"""