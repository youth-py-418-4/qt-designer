import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget,
                            QTableWidgetItem)
from PyQt6.QtCore import Qt
import mysql.connector
from dotenv import load_dotenv

class UserManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Management")
        self.setGeometry(100, 100, 600, 400)

        # Load environment variables
        load_dotenv()

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Form section
        form_widget = QWidget()
        form_layout = QHBoxLayout(form_widget)

        # Name input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter user name")
        form_layout.addWidget(QLabel("Name:"))
        form_layout.addWidget(self.name_input)

        # Add button
        add_button = QPushButton("Add User")
        add_button.clicked.connect(self.add_user)
        form_layout.addWidget(add_button)

        layout.addWidget(form_widget)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["ID", "Name"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        # Load initial data
        self.load_users()

    def get_db_connection(self):
        return mysql.connector.connect(
            database=os.getenv('DATABASE_DB'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASS'),
            host=os.getenv('DATABASE_HOST'),
            port=int(os.getenv('DATABASE_PORT'))
        )

    def load_users(self):
        try:
            conn = self.get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, name FROM users")
            users = cur.fetchall()

            self.table.setRowCount(len(users))
            for row, user in enumerate(users):
                self.table.setItem(row, 0, QTableWidgetItem(str(user[0])))
                self.table.setItem(row, 1, QTableWidgetItem(user[1]))

            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error loading users: {e}")

    def add_user(self):
        name = self.name_input.text().strip()
        if not name:
            return

        try:
            conn = self.get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO users (name) VALUES (%s)", (name,))
            conn.commit()
            user_id = cur.lastrowid

            # Add new row to table
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(user_id)))
            self.table.setItem(row, 1, QTableWidgetItem(name))

            # Clear input
            self.name_input.clear()

            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error adding user: {e}")

app = QApplication(sys.argv)
window = UserManagementApp()
window.show()
sys.exit(app.exec())