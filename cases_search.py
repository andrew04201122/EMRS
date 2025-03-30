from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QTableWidget, QMessageBox, QTableWidgetItem, QPushButton, QHeaderView, QComboBox, QSizePolicy, QLineEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication
import sys
import csv
import os
import re

class CasesSearchPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("病例查詢")
        self.setGeometry(150, 150, 600, 400)
        self.data_header = ["姓名", "身分證字號" ,"看診時間", "性別", "出生年月日", "手機號碼", "診斷", "病史", "主訴", "病程", "處置", "康復計劃", "康復目標", "康復方法", "家庭支持", "社會支持", "ROM", "MMT", "end feel", "STTT", "special test", "其他"]
        self.data_records = []
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
                self.data_records = list(reader)
        else:
            # 如果 data.csv 不存在，則創建它
            QMessageBox.warning(self, "沒找到檔案")

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # 搜尋欄位
        self.file_selector_layout = QHBoxLayout()
        self.file_selector_label = QLabel("查詢欄位:")
        self.file_selector = QComboBox()
        self.file_selector.addItems(["身分證字號", "出生年月日", "姓名"])
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("請輸入查詢內容")
        self.search_button = QPushButton("查詢")
        self.search_button.clicked.connect(self.search_data)
        
        self.file_selector_layout.addWidget(self.file_selector_label)
        self.file_selector_layout.addWidget(self.file_selector)
        self.file_selector_layout.addWidget(self.search_bar)
        self.file_selector_layout.addWidget(self.search_button)
        
        layout.addLayout(self.file_selector_layout)
        
        # 資料選項
        self.data_selector_layout = QHBoxLayout()
        self.data_select_label = QLabel("查詢結果:")
        self.data_selector = QComboBox()
        self.data_selector.setEnabled(False)  # 初始時不可選擇
        self.data_selector_layout.addWidget(self.data_select_label)
        self.data_selector_layout.addWidget(self.data_selector)
        
        layout.addLayout(self.data_selector_layout)

        self.table = QTableWidget(len(self.data_header), 2)
        self.table.setHorizontalHeaderLabels(["項目", "數據"])        

        for row, header in enumerate(self.data_header):
            item = QTableWidgetItem(header)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 0, item)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.table)

        button_layout = QHBoxLayout()
        self.save_button = QPushButton("保存")
        self.save_button.clicked.connect(self.save_data)
        button_layout.addWidget(self.save_button)

        self.home_button = QPushButton("回到主頁")
        self.home_button.clicked.connect(self.go_to_home)
        button_layout.addWidget(self.home_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def search_data(self):
        search_column = self.file_selector.currentText()
        search_value = self.search_bar.text().strip()

        if not search_value:
            QMessageBox.warning(self, "錯誤", "請輸入查詢內容")
            return

        if search_column not in self.data_header:
            QMessageBox.warning(self, "錯誤", "查詢欄位不存在")
            return

        column_index = self.data_header.index(search_column)
        self.matching_records = []  # 用來存符合條件的資料
        self.matching_indices = []  # 用來存符合條件的索引

        # 搜集所有符合條件的資料
        for i, row in enumerate(self.data_records):
            if row[column_index] == search_value:
                self.matching_records.append(row)
                self.matching_indices.append(i)  # 記錄該筆資料的索引位置

        if not self.matching_records:
            QMessageBox.warning(self, "查詢失敗", "查無資料")
            return

        # 清空選單，並加入匹配的看診時間
        self.data_selector.clear()
        self.data_selector.addItem("請選擇看診時間")
        for record in self.matching_records:
            consultation_time = record[self.data_header.index("看診時間")]
            self.data_selector.addItem(consultation_time, userData=record)

        # 讓使用者選擇看診時間
        self.data_selector.currentIndexChanged.connect(self.display_selected_record)
        self.data_selector.setEnabled(True)

    def display_selected_record(self, index):
        if index > 0:
            self.selected_index = self.matching_indices[index - 1]  # 記錄 CSV 中的索引
            selected_record = self.matching_records[index - 1]

            for i, value in enumerate(selected_record):
                self.table.setItem(i, 1, QTableWidgetItem(value))

    def go_to_home(self):
        """回到主頁，若有未儲存變更則提醒"""
        self.close()

    def validate_id_number(self, id_number):
        """檢查身分證字號格式是否為 1 個大寫英文 + 9 個數字"""
        pattern = r"^[A-Z][0-9]{9}$"
        return bool(re.match(pattern, id_number))
    
    def validate_phone_number(self, phone_number):
        """檢查手機號碼格式是否為XXXX-XXXXXX"""
        pattern = r"^\d{4}-\d{6}$"
        return bool(re.match(pattern, phone_number))
    
    def validate_birth_date(self, date_str):
        """檢查出生年月日格式是否為XXXX/XX/XX"""
        pattern = r"^\d{4}/\d{2}/\d{2}$"
        pattern1 = r"^\d{4}/\d{1}/\d{2}$"
        return bool(re.match(pattern, date_str)) or bool(re.match(pattern1, date_str))
    
    def save_data(self):
        if not hasattr(self, "selected_index") or self.selected_index is None:
            QMessageBox.warning(self, "錯誤", "請先查詢並選擇資料")
            return

        new_data = []
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 1)
            new_data.append(item.text() if item else "")

        # 確保身分證字號、手機號碼、出生年月日等格式正確
        id_index = self.data_header.index("身分證字號")
        if not self.validate_id_number(new_data[id_index]):
            QMessageBox.warning(self, "格式錯誤", "身分證字號格式錯誤！請輸入 1 個大寫英文字母 + 9 個數字。")
            return

        birth_date_index = self.data_header.index("出生年月日")
        if not self.validate_birth_date(new_data[birth_date_index]):
            QMessageBox.warning(self, "格式錯誤", "出生年月日格式錯誤，請輸入 XXXX/XX/XX")
            return

        gender_index = self.data_header.index("性別")
        if new_data[gender_index] not in ["男", "女"]:
            QMessageBox.warning(self, "格式錯誤", "性別錯誤，請輸入 男 或 女")
            return

        phone_index = self.data_header.index("手機號碼")
        if not self.validate_phone_number(new_data[phone_index]):
            QMessageBox.warning(self, "格式錯誤", "手機號碼格式錯誤，應為 XXXX-XXXXXX")
            return

        # 更新對應索引的資料
        self.data_records[self.selected_index] = new_data

        file_path = os.path.join("Data", "data.csv")
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(self.data_header)  # 寫入標頭
                writer.writerows(self.data_records)  # 寫入所有資料（包括已修改的行）

            QMessageBox.information(self, "成功", "資料已成功儲存")
        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"寫入檔案時發生錯誤：{str(e)}")

        print("Data saved to CSV file:", new_data)        

    def resizeEvent(self, event):
        super().resizeEvent(event)
        
        # 設定字體大小
        font_size = self.width() // 50  
        font = QFont()
        font.setPointSize(font_size)
        
        self.table.setFont(font)
        for row in range(self.table.rowCount()):
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                if item:
                    item.setFont(font)

        # 按鈕調整
        button_height = self.height() // 20
        button_font_size = button_height // 3
        button_font = QFont()
        button_font.setPointSize(button_font_size)
        
        for button in [self.save_button, self.home_button]:
            button.setFont(button_font)
        
        max_button_width = max(self.save_button.sizeHint().width(),
                            self.home_button.sizeHint().width())

        for button in [self.save_button, self.home_button]:
            button.setFixedSize(max_button_width, button_height)

        # 調整查詢欄位與選單大小
        input_height = self.height() // 20  # 調整搜尋欄位高度
        input_font_size = input_height // 3  # 調整搜尋欄位字體大小
        input_font = QFont()
        input_font.setPointSize(input_font_size)

        # 設定搜尋欄與按鈕的大小
        self.file_selector.setFont(input_font)
        self.search_bar.setFont(input_font)
        self.search_button.setFont(input_font)
        self.search_button.setFixedHeight(input_height)

        # 設定查詢結果下拉選單的大小
        self.data_selector.setFont(input_font)
        self.data_selector.setFixedHeight(input_height)

        # 強制調整內部元件大小
        self.file_selector.setFixedHeight(input_height)
        self.search_bar.setFixedHeight(input_height)

        self.file_selector_label.setFont(input_font)
        self.data_select_label.setFont(input_font)

        # 重新調整 layout
        self.file_selector_layout.setSpacing(self.width() // 50)
        self.data_selector_layout.setSpacing(self.width() // 50)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CasesSearchPage()
    window.show()
    sys.exit(app.exec())