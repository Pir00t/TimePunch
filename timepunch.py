"""
TimePunch - Modern Time Tracking Application
Main entry point
"""

import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import TimePunchWindow


def main():
	"""Main entry point"""
	app = QApplication(sys.argv)
	app.setApplicationName("TimePunch")
	
	window = TimePunchWindow()
	window.show()
	
	sys.exit(app.exec())


if __name__ == "__main__":
	main()