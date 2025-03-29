from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QTableWidget, QMessageBox, QTableWidgetItem, QPushButton, QHeaderView
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication
import sys
import csv
import os
import re

class CasesFillPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("病例填寫")
        self.setGeometry(150, 150, 600, 400)
        self.data_header = ["姓名", "身分證字號" ,"看診時間", "性別", "出生年月日", "診斷", "病史", "主訴", "病程", "處置", "康復計劃", "康復目標", "康復方法", "家庭支持", "社會支持", "ROM", "MMT", "end feel", "STTT", "special test"]

        data_folder = "Data"
        data_file = os.path.join(data_folder, "data.csv")

        # 檢查是否有 Data 資料夾，沒有的話就創建
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        # 檢查 data.csv 是否存在
        if os.path.exists(data_file):
            # 讀取 CSV 並更新 header
            with open(data_file, "r", encoding="utf-8-sig") as file:
                reader = csv.reader(file)
                header = next(reader, None)  # 取得第一行作為 header
                if header:
                    self.data_header = header
                    print("self.data_header:", self.data_header)
                else:
                    print("data.csv 為空，無法讀取 header")
        else:
            # 如果 data.csv 不存在，則創建它
            self.create_csv_file()

        self.init_ui()

    def create_csv_file(self):
        file_path = os.path.join("Data", "data.csv")
        if not os.path.exists(file_path):
            with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(self.data_header)

    def init_ui(self):
        layout = QVBoxLayout()

        self.table = QTableWidget(len(self.data_header), 2)  # Number of rows equal to number of headers, 2 columns
        self.table.setHorizontalHeaderLabels(["項目", "數據"])

        for row, header in enumerate(self.data_header):
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

    def validate_id_number(self, id_number):
        """檢查身分證字號格式是否為 1 個大寫英文 + 9 個數字"""
        pattern = r"^[A-Z][0-9]{9}$"
        return bool(re.match(pattern, id_number))
    
    def validate_birth_date(self, date_str):
        """檢查出生年月日格式是否為XXXX/XX/XX"""
        pattern = r"^\d{4}/\d{2}/\d{2}$"
        return bool(re.match(pattern, date_str))
    
    def save_data(self):
        file_path = os.path.join("Data", "data.csv")
        new_data = []
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 1)  # Get data from the second column
            new_data.append(item.text() if item else "")

        # 找出 "身分證字號" 的索引
        try:
            id_index = self.data_header.index("身分證字號")
        except ValueError:
            QMessageBox.warning(self, "錯誤", "找不到 '身分證字號' 欄位")
            return

        # 檢查身份證字號格式
        id_number = new_data[id_index]
        if not self.validate_id_number(id_number):
            QMessageBox.warning(self, "格式錯誤", "身分證字號格式錯誤！請輸入 1 個大寫英文字母 + 9 個數字。")
            return  # 不儲存資料

        # 檢查出生年月日格式
        try:
            birth_date_index = self.data_header.index("出生年月日")
        except ValueError:
            QMessageBox.warning(self, "錯誤", "找不到 '出生年月日' 欄位")
            return
        
        birth_date = new_data[birth_date_index]
        if not self.validate_birth_date(birth_date):
            QMessageBox.warning(self, "格式錯誤", "出生年月日錯誤 請輸入西元生日 XXXX/XX/XX ")
            return  # 不儲存資料

        # 檢查性別格式
        try:
            gender_index = self.data_header.index("性別")
        except ValueError:
            QMessageBox.warning(self, "錯誤", "找不到 '性別' 欄位")
            return
        
        gender = new_data[gender_index]
        if gender not in ["男", "女"]:
            QMessageBox.warning(self, "格式錯誤", "性別錯誤 請輸入 男 或 女 ")
            return  # 不儲存資料

        try:
            # Write updated data back to CSV
            with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(self.data_header)
                writer.writerow(new_data)
        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"寫入檔案時發生錯誤：{str(e)}")        
        
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