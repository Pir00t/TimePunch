"""
Dialog windows for TimePunch
"""

from PySide6.QtWidgets import (
	QDialog, QVBoxLayout, QLabel, QLineEdit, 
	QPushButton, QTextEdit, QDialogButtonBox
)


class EditTaskDialog(QDialog):
	"""Dialog for editing task details"""
	
	def __init__(self, task_data, parent=None):
		super().__init__(parent)
		self.task_data = task_data
		self.setup_ui()
	
	def setup_ui(self):
		self.setWindowTitle("Edit Task")
		self.setMinimumWidth(400)
		
		layout = QVBoxLayout()
		
		# Task name
		layout.addWidget(QLabel("Task Name:"))
		self.name_input = QLineEdit()
		self.name_input.setText(self.task_data[1])
		layout.addWidget(self.name_input)
		
		# Tags
		layout.addWidget(QLabel("Tags:"))
		self.tags_input = QLineEdit()
		self.tags_input.setText(self.task_data[2] or "")
		layout.addWidget(self.tags_input)
		
		# Start time
		layout.addWidget(QLabel("Start Time (YYYY-MM-DD HH:MM:SS):"))
		self.start_input = QLineEdit()
		self.start_input.setText(self.task_data[3])
		layout.addWidget(self.start_input)
		
		# End time
		layout.addWidget(QLabel("End Time (YYYY-MM-DD HH:MM:SS):"))
		self.end_input = QLineEdit()
		self.end_input.setText(self.task_data[4] or "")
		layout.addWidget(self.end_input)
		
		# Buttons
		buttons = QDialogButtonBox(
			QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
		)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)
		layout.addWidget(buttons)
		
		self.setLayout(layout)
	
	def get_data(self):
		"""Return edited data"""
		return {
			'name': self.name_input.text(),
			'tags': self.tags_input.text(),
			'start_time': self.start_input.text(),
			'end_time': self.end_input.text()
		}


class SummaryDialog(QDialog):
	"""Dialog for displaying summaries"""
	
	def __init__(self, title, content, parent=None):
		super().__init__(parent)
		self.setWindowTitle(title)
		self.setMinimumSize(500, 400)
		
		layout = QVBoxLayout()
		
		text_edit = QTextEdit()
		text_edit.setReadOnly(True)
		text_edit.setPlainText(content)
		layout.addWidget(text_edit)
		
		close_btn = QPushButton("Close")
		close_btn.clicked.connect(self.accept)
		layout.addWidget(close_btn)
		
		self.setLayout(layout)