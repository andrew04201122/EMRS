from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView
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

        keep_button = QPushButton("暫存")
        keep_button.clicked.connect(self.keep_data)
        layout.addWidget(keep_button)

        save_button = QPushButton("保存")
        save_button.clicked.connect(self.save_data)
        layout.addWidget(save_button)

        clear_button = QPushButton("清除")
        clear_button.clicked.connect(self.clear_data)
        layout.addWidget(clear_button)

        self.setLayout(layout)

    def keep_data(self):
        self.temp_data = []
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 1)  # Get data from the second column
            self.temp_data.append(item.text() if item else "")
        print("Data kept temporarily:", self.temp_data)

    def save_data(self):
        file_path = os.path.join("Data", "病例.csv")
        with open(file_path, mode='a', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            row_data = []
            for row in range(self.table.rowCount()):
                item = self.table.item(row, 1)  # Get data from the second column
                row_data.append(item.text() if item else "")
            writer.writerow(row_data)
        print("Data saved to CSV file:", row_data)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CasesFillPage()
    window.show()
    sys.exit(app.exec())