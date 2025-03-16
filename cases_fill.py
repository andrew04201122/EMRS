from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QTableWidget, QMessageBox, QTableWidgetItem, QPushButton, QHeaderView
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication
import sys
import csv
import os

class CasesFillPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("病例填寫")
        self.setGeometry(150, 150, 600, 400)

        if not os.path.exists("Data"):
            os.makedirs("Data")
        self.create_csv_file()

        self.init_ui()

    def create_csv_file(self):
        headers = [
            "姓名", "病歷號碼", "性別", "出生年月日", "診斷", "病史", "主訴", "病程", "處置", 
            "康復計劃", "康復目標", "康復方法", "家庭支持", "社會支持", "ROM", "MMT", 
            "end feel", "STTT", "special test"
        ]
        file_path = os.path.join("Data", "病例.csv")
        if not os.path.exists(file_path):
            with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(headers)

    def init_ui(self):
        layout = QVBoxLayout()

        headers = [
            "姓名", "病歷號碼", "性別", "出生年月日", "診斷", "病史", "主訴", "病程", "處置", 
            "康復計劃", "康復目標", "康復方法", "家庭支持", "社會支持", "ROM", "MMT", 
            "end feel", "STTT", "special test"
        ]
        self.table = QTableWidget(len(headers), 2)  # Number of rows equal to number of headers, 2 columns
        self.table.setHorizontalHeaderLabels(["項目", "數據"])

        for row, header in enumerate(headers):
            item = QTableWidgetItem(header)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make header cells non-editable
            self.table.setItem(row, 0, item)

        # Make the table headers stretch with the window size
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.table)

        button_layout = QHBoxLayout()

        self.keep_button = QPushButton("暫存")
        self.keep_button.clicked.connect(self.keep_data)
        button_layout.addWidget(self.keep_button)

        self.save_button = QPushButton("保存")
        self.save_button.clicked.connect(self.save_data)
        button_layout.addWidget(self.save_button)

        self.clear_button = QPushButton("清除")
        self.clear_button.clicked.connect(self.clear_data)
        button_layout.addWidget(self.clear_button)

        # 回到主頁按鈕
        self.home_button = QPushButton("回到主頁")
        self.home_button.clicked.connect(self.go_to_home)
        button_layout.addWidget(self.home_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def go_to_home(self):
        """回到主頁"""
        self.close()

    def keep_data(self):
        self.temp_data = []
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 1)  # Get data from the second column
            self.temp_data.append(item.text() if item else "")
        print("Data kept temporarily:", self.temp_data)

    def save_data(self):
        file_path = os.path.join("Data", "病例.csv")
        new_data = []
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 1)  # Get data from the second column
            new_data.append(item.text() if item else "")

        # Read existing data
        existing_data = []
        with open(file_path, mode='r', newline='', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            headers = next(reader)
            for row in reader:
                existing_data.append(row)

        # Check for existing 病歷號碼 and replace if found
        replaced = False
        for i, row in enumerate(existing_data):
            if row[1] == new_data[1]:  # Compare 病歷號碼
                existing_data[i] = new_data
                replaced = True
                break

        # If not replaced, append new data
        if not replaced:
            existing_data.append(new_data)

        # Write updated data back to CSV
        with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(existing_data)

        print("Data saved to CSV file:", new_data)

    def clear_data(self):
        for row in range(self.table.rowCount()):
            self.table.setItem(row, 1, QTableWidgetItem(""))  # Clear data in the second column

    def resizeEvent(self, event):
        super().resizeEvent(event)
        font_size = self.width() // 50  # Adjust the divisor to control the font size scaling
        font = QFont()
        font.setPointSize(font_size)
        self.table.setFont(font)
        for row in range(self.table.rowCount()):
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                if item:
                    item.setFont(font)

        # Adjust button height to be 1/10 of the window height
        button_height = self.height() // 10

        # Adjust button font size based on button height
        button_font_size = button_height // 3
        button_font = QFont()
        button_font.setPointSize(button_font_size)

        # Set font for all buttons
        for button in [self.keep_button, self.save_button, self.clear_button, self.home_button]:
            button.setFont(button_font)

        # Calculate the maximum width among all buttons
        max_button_width = max(self.keep_button.sizeHint().width(),
                               self.save_button.sizeHint().width(),
                               self.clear_button.sizeHint().width(),
                               self.home_button.sizeHint().width())

        # Set the size for all buttons
        for button in [self.keep_button, self.save_button, self.clear_button, self.home_button]:
            button.setFixedSize(max_button_width, button_height)

    def closeEvent(self, event):
        if hasattr(self, 'temp_data') and self.temp_data:
            reply = QMessageBox.question(self, '提示', '資料只存在暫存的狀態，是否要儲存資料？',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.save_data()
            else:
                event.accept()
        else:
            event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CasesFillPage()
    window.show()
    sys.exit(app.exec())