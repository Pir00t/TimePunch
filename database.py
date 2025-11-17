"""
Database handler for TimePunch
"""

import sqlite3
from datetime import datetime
from pathlib import Path


class Database:
	"""SQLite database handler"""
	
	def __init__(self, db_file="timepunch.db"):
		self.db_file = db_file
		self.init_db()
	
	def init_db(self):
		"""Initialize database with tables"""
		conn = sqlite3.connect(self.db_file)
		cursor = conn.cursor()
		
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS tasks (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT NOT NULL,
				tags TEXT,
				start_time TEXT NOT NULL,
				end_time TEXT,
				duration_seconds INTEGER,
				is_running INTEGER DEFAULT 0
			)
		""")
		
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS settings (
				key TEXT PRIMARY KEY,
				value TEXT
			)
		""")
		
		conn.commit()
		conn.close()
	
	def start_task(self, name, tags=""):
		"""Start a new task"""
		conn = sqlite3.connect(self.db_file)
		cursor = conn.cursor()
		
		start_time = datetime.now().isoformat()
		cursor.execute(
			"INSERT INTO tasks (name, tags, start_time, is_running) VALUES (?, ?, ?, 1)",
			(name, tags, start_time)
		)
		task_id = cursor.lastrowid
		
		conn.commit()
		conn.close()
		return task_id
	
	def stop_task(self, task_id):
		"""Stop a running task"""
		conn = sqlite3.connect(self.db_file)
		cursor = conn.cursor()
		
		end_time = datetime.now().isoformat()
		cursor.execute("SELECT start_time FROM tasks WHERE id = ?", (task_id,))
		result = cursor.fetchone()
		
		if result:
			start = datetime.fromisoformat(result[0])
			end = datetime.fromisoformat(end_time)
			duration = int((end - start).total_seconds())
			
			cursor.execute(
				"UPDATE tasks SET end_time = ?, duration_seconds = ?, is_running = 0 WHERE id = ?",
				(end_time, duration, task_id)
			)
		
		conn.commit()
		conn.close()
	
	def get_running_task(self):
		"""Get currently running task"""
		conn = sqlite3.connect(self.db_file)
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM tasks WHERE is_running = 1 ORDER BY start_time DESC LIMIT 1")
		result = cursor.fetchone()
		conn.close()
		return result
	
	def get_all_tasks(self, limit=100):
		"""Get all tasks ordered by start time descending"""
		conn = sqlite3.connect(self.db_file)
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM tasks ORDER BY start_time DESC LIMIT ?", (limit,))
		results = cursor.fetchall()
		conn.close()
		return results
	
	def get_tasks_by_date_range(self, start_date, end_date):
		"""Get tasks within date range"""
		conn = sqlite3.connect(self.db_file)
		cursor = conn.cursor()
		cursor.execute(
			"SELECT * FROM tasks WHERE date(start_time) BETWEEN ? AND ? ORDER BY start_time DESC",
			(start_date, end_date)
		)
		results = cursor.fetchall()
		conn.close()
		return results
	
	def update_task(self, task_id, name, tags, start_time, end_time):
		"""Update an existing task"""
		conn = sqlite3.connect(self.db_file)
		cursor = conn.cursor()
		
		start = datetime.fromisoformat(start_time)
		end = datetime.fromisoformat(end_time)
		duration = int((end - start).total_seconds())
		
		cursor.execute(
			"UPDATE tasks SET name = ?, tags = ?, start_time = ?, end_time = ?, duration_seconds = ? WHERE id = ?",
			(name, tags, start_time, end_time, duration, task_id)
		)
		
		conn.commit()
		conn.close()
	
	def delete_task(self, task_id):
		"""Delete a task"""
		conn = sqlite3.connect(self.db_file)
		cursor = conn.cursor()
		cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
		conn.commit()
		conn.close()
	
	def get_all_tags(self):
		"""Get unique tags from all tasks"""
		conn = sqlite3.connect(self.db_file)
		cursor = conn.cursor()
		cursor.execute("SELECT DISTINCT tags FROM tasks WHERE tags IS NOT NULL AND tags != ''")
		results = cursor.fetchall()
		conn.close()
		
		# Parse multi-tags
		tags = set()
		for row in results:
			if row[0]:
				for tag in row[0].split(','):
					tags.add(tag.strip())
		return sorted(list(tags))
	
	def get_setting(self, key, default=None):
		"""Get a setting value"""
		conn = sqlite3.connect(self.db_file)
		cursor = conn.cursor()
		cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
		result = cursor.fetchone()
		conn.close()
		return result[0] if result else default
	
	def set_setting(self, key, value):
		"""Set a setting value"""
		conn = sqlite3.connect(self.db_file)
		cursor = conn.cursor()
		cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
		conn.commit()
		conn.close()