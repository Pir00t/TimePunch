"""
Main window UI for TimePunch
"""

from PySide6.QtWidgets import (
	QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
	QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
	QComboBox, QMessageBox, QHeaderView, QFrame, QSplitter
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QKeySequence, QShortcut
from datetime import datetime, timedelta

from database import Database
from ui.dialogs import EditTaskDialog, SummaryDialog
from ui.styles import get_stylesheet


class TimePunchWindow(QMainWindow):
	"""Main application window"""
	
	def __init__(self):
		super().__init__()
		self.db = Database()
		self.current_task_id = None
		self.timer = QTimer()
		self.timer.timeout.connect(self.update_timer_display)
		self.dark_mode = self.db.get_setting('dark_mode', 'true') == 'true'
		
		self.setup_ui()
		self.apply_theme()
		self.check_running_task()
		self.setup_shortcuts()
	
	def setup_ui(self):
		"""Setup the user interface"""
		self.setWindowTitle("TimePunch")
		self.setMinimumSize(900, 600)
		
		# Central widget
		central = QWidget()
		self.setCentralWidget(central)
		main_layout = QHBoxLayout(central)
		
		# Left panel - Controls
		left_panel = QWidget()
		left_layout = QVBoxLayout(left_panel)
		left_layout.setSpacing(15)
		
		# Title
		title = QLabel("⏱ TimePunch")
		title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
		title.setAlignment(Qt.AlignmentFlag.AlignCenter)
		left_layout.addWidget(title)
		
		# Task input
		left_layout.addWidget(QLabel("Task Name:"))
		self.task_input = QLineEdit()
		self.task_input.setPlaceholderText("What are you working on?")
		self.task_input.setMinimumHeight(40)
		self.task_input.returnPressed.connect(self.toggle_task)
		left_layout.addWidget(self.task_input)
		
		# Tag input with dropdown
		left_layout.addWidget(QLabel("Tags (optional):"))
		self.tag_input = QComboBox()
		self.tag_input.setEditable(True)
		self.tag_input.lineEdit().setPlaceholderText("e.g., research, email")
		self.tag_input.setMinimumHeight(40)
		self.refresh_tags()
		left_layout.addWidget(self.tag_input)
		
		# Control buttons
		btn_layout = QHBoxLayout()
		self.start_btn = QPushButton("Start")
		self.start_btn.setMinimumHeight(50)
		self.start_btn.clicked.connect(self.start_task)
		
		self.stop_btn = QPushButton("Stop")
		self.stop_btn.setMinimumHeight(50)
		self.stop_btn.setEnabled(False)
		self.stop_btn.clicked.connect(self.stop_task)
		
		btn_layout.addWidget(self.start_btn)
		btn_layout.addWidget(self.stop_btn)
		left_layout.addLayout(btn_layout)
		
		# Timer display
		timer_frame = QFrame()
		timer_frame.setObjectName("timerFrame")
		timer_layout = QVBoxLayout(timer_frame)
		
		self.timer_label = QLabel("00:00:00")
		self.timer_label.setFont(QFont("Courier New", 42, QFont.Weight.Bold))
		self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		timer_layout.addWidget(self.timer_label)
		
		self.current_task_label = QLabel("No active task")
		self.current_task_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.current_task_label.setWordWrap(True)
		self.current_task_label.setFont(QFont("Arial", 11))
		timer_layout.addWidget(self.current_task_label)
		
		left_layout.addWidget(timer_frame)
		
		# Summary buttons
		summary_layout = QVBoxLayout()
		summary_layout.setSpacing(12)
		
		daily_btn = QPushButton("Daily Summary")
		daily_btn.setMinimumHeight(50)
		daily_btn.clicked.connect(self.show_daily_summary)
		summary_layout.addWidget(daily_btn)
		
		weekly_btn = QPushButton("Weekly Summary")
		weekly_btn.setMinimumHeight(50)
		weekly_btn.clicked.connect(self.show_weekly_summary)
		summary_layout.addWidget(weekly_btn)
		
		monthly_btn = QPushButton("Monthly Summary")
		monthly_btn.setMinimumHeight(50)
		monthly_btn.clicked.connect(self.show_monthly_summary)
		summary_layout.addWidget(monthly_btn)
		
		left_layout.addLayout(summary_layout)
		
		# Theme toggle
		self.theme_btn = QPushButton("Toggle Theme")
		self.theme_btn.setMinimumHeight(50)
		self.theme_btn.clicked.connect(self.toggle_theme)
		left_layout.addWidget(self.theme_btn)
		
		left_layout.addStretch()
		
		# Right panel - History table
		right_panel = QWidget()
		right_layout = QVBoxLayout(right_panel)
		
		history_title = QLabel("Task History")
		history_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
		right_layout.addWidget(history_title)
		
		self.history_table = QTableWidget()
		self.history_table.setColumnCount(6)
		self.history_table.setHorizontalHeaderLabels(["Task", "Tags", "Start", "End", "Duration", "Actions"])
		
		# Set column widths
		header = self.history_table.horizontalHeader()
		header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Task column stretches
		header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Tags
		header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Start
		header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # End
		header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Duration
		self.history_table.setColumnWidth(5, 150)  # Actions column fixed width
		
		self.history_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
		self.history_table.verticalHeader().setDefaultSectionSize(60)
		self.history_table.cellClicked.connect(self.on_task_clicked)
		right_layout.addWidget(self.history_table)
		
		# Splitter
		splitter = QSplitter(Qt.Orientation.Horizontal)
		splitter.addWidget(left_panel)
		splitter.addWidget(right_panel)
		splitter.setStretchFactor(0, 1)
		splitter.setStretchFactor(1, 2)
		
		main_layout.addWidget(splitter)
		
		self.refresh_history()
	
	def setup_shortcuts(self):
		"""Setup keyboard shortcuts"""
		QShortcut(QKeySequence("Ctrl+T"), self, self.focus_task_input)
		QShortcut(QKeySequence("Ctrl+H"), self, self.refresh_history)
		QShortcut(QKeySequence("Ctrl+W"), self, self.show_weekly_summary)
		QShortcut(QKeySequence("Ctrl+M"), self, self.show_monthly_summary)
		QShortcut(QKeySequence("Return"), self, self.toggle_task)
	
	def apply_theme(self):
		"""Apply dark or light theme"""
		self.setStyleSheet(get_stylesheet(self.dark_mode))
	
	def toggle_theme(self):
		"""Toggle between dark and light themes"""
		self.dark_mode = not self.dark_mode
		self.db.set_setting('dark_mode', 'true' if self.dark_mode else 'false')
		self.apply_theme()
	
	def focus_task_input(self):
		"""Focus the task input field"""
		self.task_input.setFocus()
	
	def toggle_task(self):
		"""Toggle between start and stop"""
		if self.current_task_id:
			self.stop_task()
		else:
			self.start_task()
	
	def check_running_task(self):
		"""Check if there's a running task on startup"""
		task = self.db.get_running_task()
		if task:
			self.current_task_id = task[0]
			self.task_input.setText(task[1])
			self.tag_input.setCurrentText(task[2] or "")
			self.start_btn.setEnabled(False)
			self.stop_btn.setEnabled(True)
			self.task_input.setEnabled(False)
			self.tag_input.setEnabled(False)
			self.current_task_label.setText(f"Active: {task[1]}")
			self.timer.start(1000)
	
	def start_task(self):
		"""Start tracking a new task"""
		task_name = self.task_input.text().strip()
		if not task_name:
			QMessageBox.warning(self, "No Task", "Please enter a task name.")
			return
		
		tags = self.tag_input.currentText().strip()
		self.current_task_id = self.db.start_task(task_name, tags)
		
		self.start_btn.setEnabled(False)
		self.stop_btn.setEnabled(True)
		self.task_input.setEnabled(False)
		self.tag_input.setEnabled(False)
		self.current_task_label.setText(f"Active: {task_name}")
		
		self.timer.start(1000)
	
	def stop_task(self):
		"""Stop the current task"""
		if not self.current_task_id:
			return
		
		self.db.stop_task(self.current_task_id)
		self.current_task_id = None
		
		self.timer.stop()
		self.timer_label.setText("00:00:00")
		self.current_task_label.setText("No active task")
		
		self.start_btn.setEnabled(True)
		self.stop_btn.setEnabled(False)
		self.task_input.setEnabled(True)
		self.tag_input.setEnabled(True)
		self.task_input.clear()
		self.tag_input.setCurrentText("")
		
		self.refresh_history()
		self.refresh_tags()
	
	def update_timer_display(self):
		"""Update the timer display"""
		if not self.current_task_id:
			return
		
		task = self.db.get_running_task()
		if task:
			start = datetime.fromisoformat(task[3])
			elapsed = datetime.now() - start
			hours, remainder = divmod(int(elapsed.total_seconds()), 3600)
			minutes, seconds = divmod(remainder, 60)
			self.timer_label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
	
	def refresh_history(self):
		"""Refresh the history table"""
		tasks = self.db.get_all_tasks()
		self.history_table.setRowCount(len(tasks))
		
		for row, task in enumerate(tasks):
			# Task name
			self.history_table.setItem(row, 0, QTableWidgetItem(task[1]))
			
			# Tags
			self.history_table.setItem(row, 1, QTableWidgetItem(task[2] or ""))
			
			# Start time
			start = datetime.fromisoformat(task[3])
			self.history_table.setItem(row, 2, QTableWidgetItem(start.strftime("%m/%d %H:%M")))
			
			# End time
			if task[4]:
				end = datetime.fromisoformat(task[4])
				self.history_table.setItem(row, 3, QTableWidgetItem(end.strftime("%m/%d %H:%M")))
			else:
				self.history_table.setItem(row, 3, QTableWidgetItem("Running..."))
			
			# Duration
			if task[5]:
				hours, remainder = divmod(task[5], 3600)
				minutes, seconds = divmod(remainder, 60)
				duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
				self.history_table.setItem(row, 4, QTableWidgetItem(duration_str))
			else:
				self.history_table.setItem(row, 4, QTableWidgetItem("-"))
			
			# Actions buttons
			actions_widget = QWidget()
			actions_layout = QHBoxLayout(actions_widget)
			actions_layout.setContentsMargins(8, 0, 8, 0)
			actions_layout.setSpacing(8)
			actions_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
			
			edit_btn = QPushButton("Edit")
			edit_btn.setObjectName("actionButton")
			edit_btn.setFixedHeight(35)
			edit_btn.setFixedWidth(60)
			edit_btn.clicked.connect(lambda checked, r=row: self.edit_task(r))
			
			delete_btn = QPushButton("Del")
			delete_btn.setObjectName("actionButton")
			delete_btn.setFixedHeight(35)
			delete_btn.setFixedWidth(60)
			delete_btn.clicked.connect(lambda checked, r=row: self.delete_task(r))
			
			actions_layout.addWidget(edit_btn)
			actions_layout.addWidget(delete_btn)
			
			self.history_table.setCellWidget(row, 5, actions_widget)
	
	def refresh_tags(self):
		"""Refresh the tag dropdown"""
		current = self.tag_input.currentText()
		self.tag_input.clear()
		tags = self.db.get_all_tags()
		self.tag_input.addItems(tags)
		self.tag_input.setCurrentText(current)
	
	def on_task_clicked(self, row, col):
		"""Handle task row click - resume task"""
		if col < 5:  # Don't trigger on action buttons
			task_name = self.history_table.item(row, 0).text()
			tags = self.history_table.item(row, 1).text()
			
			if not self.current_task_id:
				self.task_input.setText(task_name)
				self.tag_input.setCurrentText(tags)
	
	def edit_task(self, row):
		"""Edit a task"""
		tasks = self.db.get_all_tasks()
		if row >= len(tasks):
			return
		
		task = tasks[row]
		dialog = EditTaskDialog(task, self)
		
		if dialog.exec():
			data = dialog.get_data()
			try:
				self.db.update_task(
					task[0],
					data['name'],
					data['tags'],
					data['start_time'],
					data['end_time']
				)
				self.refresh_history()
			except Exception as e:
				QMessageBox.critical(self, "Error", f"Failed to update task: {str(e)}")
	
	def delete_task(self, row):
		"""Delete a task"""
		tasks = self.db.get_all_tasks()
		if row >= len(tasks):
			return
		
		task = tasks[row]
		reply = QMessageBox.question(
			self,
			"Confirm Delete",
			f"Delete task '{task[1]}'?",
			QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
		)
		
		if reply == QMessageBox.StandardButton.Yes:
			self.db.delete_task(task[0])
			self.refresh_history()
	
	def generate_summary(self, start_date, end_date, title):
		"""Generate a summary for a date range"""
		tasks = self.db.get_tasks_by_date_range(start_date, end_date)
		
		if not tasks:
			return f"No tasks found for {title.lower()}."
		
		task_totals = {}
		tag_totals = {}
		total_seconds = 0
		
		for task in tasks:
			if task[5]:  # Has duration
				name = task[1]
				tags = task[2] or ""
				duration = task[5]
				
				task_totals[name] = task_totals.get(name, 0) + duration
				total_seconds += duration
				
				for tag in tags.split(','):
					tag = tag.strip()
					if tag:
						tag_totals[tag] = tag_totals.get(tag, 0) + duration
		
		# Format summary
		lines = [f"{title}\n{'=' * len(title)}\n"]
		
		lines.append("BY TASK:")
		for task, seconds in sorted(task_totals.items(), key=lambda x: -x[1]):
			hours = seconds / 3600
			lines.append(f"  {task}: {hours:.2f}h")
		
		if tag_totals:
			lines.append("\nBY TAG:")
			for tag, seconds in sorted(tag_totals.items(), key=lambda x: -x[1]):
				hours = seconds / 3600
				lines.append(f"  {tag}: {hours:.2f}h")
		
		total_hours = total_seconds / 3600
		lines.append(f"\nTOTAL: {total_hours:.2f} hours")
		
		return "\n".join(lines)
	
	def show_daily_summary(self):
		"""Show daily summary"""
		today = datetime.now().date().isoformat()
		summary = self.generate_summary(today, today, "Daily Summary")
		dialog = SummaryDialog("Daily Summary", summary, self)
		dialog.exec()
	
	def show_weekly_summary(self):
		"""Show weekly summary"""
		today = datetime.now().date()
		week_start = (today - timedelta(days=today.weekday())).isoformat()
		summary = self.generate_summary(week_start, today.isoformat(), "Weekly Summary")
		dialog = SummaryDialog("Weekly Summary", summary, self)
		dialog.exec()
	
	def show_monthly_summary(self):
		"""Show monthly summary"""
		today = datetime.now().date()
		month_start = today.replace(day=1).isoformat()
		summary = self.generate_summary(month_start, today.isoformat(), "Monthly Summary")
		dialog = SummaryDialog("Monthly Summary", summary, self)
		dialog.exec()