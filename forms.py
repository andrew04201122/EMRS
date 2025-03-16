import os
import shutil
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton,
    QComboBox, QFileDialog, QWidget, QLabel, QScrollArea, QHBoxLayout
)
from PySide6.QtGui import QPixmap, QImage, QFont
from PySide6.QtCore import Qt
import fitz  # PyMuPDF

class FormsPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Viewer")
        self.resize(600, 800)  # 設定初始大小為 600x800
        self.mode = 'forms'
        self.target_folder = "Forms"
        self.current_file = None  # 紀錄目前開啟的檔案
        self.current_page = 0  # 當前頁數
        self.total_pages = 0  # 總頁數

        if not os.path.exists(self.target_folder):
            os.makedirs(self.target_folder)

        # 主畫面元件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # 水平佈局區域（放置按鈕）
        self.top_layout = QHBoxLayout()

        # 新增檔案按鈕
        self.add_button = QPushButton("新增檔案")
        self.add_button.clicked.connect(self.add_file)
        self.top_layout.addWidget(self.add_button)

        # 顯示檔案的按鈕
        self.display_button = QPushButton("顯示檔案")
        self.display_button.clicked.connect(self.display_file)
        self.top_layout.addWidget(self.display_button)

        # 打開檔案按鈕
        self.open_button = QPushButton("打開檔案")
        self.open_button.clicked.connect(self.open_file)
        self.top_layout.addWidget(self.open_button)

        # 列印檔案按鈕
        self.print_button = QPushButton("列印檔案")
        self.print_button.clicked.connect(self.print_file)
        self.top_layout.addWidget(self.print_button)

        # 回到主頁按鈕
        self.home_button = QPushButton("回到主頁")
        self.home_button.clicked.connect(self.go_to_home)
        self.top_layout.addWidget(self.home_button)

        self.main_layout.addLayout(self.top_layout)

        # 下拉選單
        self.file_selector_layout = QHBoxLayout()
        self.file_selector = QComboBox()
        self.file_selector.addItem("請選擇檔案")
        self.refresh_file_list()
        self.file_selector_layout.addWidget(self.file_selector)
        self.main_layout.addLayout(self.file_selector_layout)

        # 滾動區域來顯示檔案內容
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.pdf_display = QLabel("未選擇任何檔案")
        self.pdf_display.setAlignment(Qt.AlignCenter)
        self.scroll_area.setWidget(self.pdf_display)
        self.main_layout.addWidget(self.scroll_area)

        # 頁面控制按鈕
        self.navigation_layout = QHBoxLayout()
        self.prev_page_button = QPushButton("上一頁")
        self.prev_page_button.clicked.connect(self.go_to_previous_page)
        self.navigation_layout.addWidget(self.prev_page_button)

        self.next_page_button = QPushButton("下一頁")
        self.next_page_button.clicked.connect(self.go_to_next_page)
        self.navigation_layout.addWidget(self.next_page_button)

        self.main_layout.addLayout(self.navigation_layout)

    def add_file(self):
        """新增檔案到目標資料夾"""
        file_path, _ = QFileDialog.getOpenFileName(self, "選擇檔案")
        if file_path:
            file_name = os.path.basename(file_path)
            destination = os.path.join(self.target_folder, file_name)

            try:
                shutil.copy(file_path, destination)
                self.refresh_file_list()
            except Exception as e:
                self.pdf_display.setText(f"檔案新增失敗：{str(e)}")

    def refresh_file_list(self):
        """更新下拉選單的檔案列表"""
        self.file_selector.clear()
        self.file_selector.addItem("請選擇檔案")
        files = [f for f in os.listdir(self.target_folder) if f.endswith((".pdf", ".png", ".jpg", ".jpeg"))]
        self.file_selector.addItems(files)

    def display_file(self):
        """顯示選定檔案內容"""
        selected_file = self.file_selector.currentText()
        if selected_file != "請選擇檔案":
            file_path = os.path.join(self.target_folder, selected_file)
            self.current_file = file_path  # 紀錄目前開啟的檔案
            self.current_page = 0  # 重設為第一頁
            try:
                if file_path.endswith(".pdf"):
                    # 使用 PyMuPDF 打開 PDF 並記錄總頁數
                    self.pdf_document = fitz.open(file_path)
                    self.total_pages = len(self.pdf_document)
                    self.show_page(self.current_page)
                elif file_path.lower().endswith((".png", ".jpg", ".jpeg")):
                    pixmap = QPixmap(file_path)
                    scaled_pixmap = pixmap.scaled(
                        self.scroll_area.width(),
                        self.scroll_area.height(),
                        Qt.KeepAspectRatio, Qt.SmoothTransformation
                    )
                    self.pdf_display.setPixmap(scaled_pixmap)
                    self.pdf_display.setText("")
                else:
                    self.pdf_display.setText("不支援的檔案格式")
            except Exception as e:
                self.pdf_display.setText(f"檔案顯示失敗：{str(e)}")
        else:
            self.pdf_display.setText("請先選擇檔案")

    def show_page(self, page_number):
        """顯示指定頁面"""
        if self.current_file and self.current_file.endswith(".pdf"):
            try:
                pdf_page = self.pdf_document[page_number]
                pix = pdf_page.get_pixmap()
                image = QImage(
                    pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888
                )
                scaled_pixmap = QPixmap.fromImage(image).scaled(
                    self.scroll_area.width(),
                    self.scroll_area.height(),
                    Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                self.pdf_display.setPixmap(scaled_pixmap)
                self.pdf_display.setText("")
            except Exception as e:
                self.pdf_display.setText(f"頁面顯示失敗：{str(e)}")

    def go_to_previous_page(self):
        """切換到上一頁"""
        if self.current_file and self.current_file.endswith(".pdf") and self.current_page > 0:
            self.current_page -= 1
            self.show_page(self.current_page)

    def go_to_next_page(self):
        """切換到下一頁"""
        if self.current_file and self.current_file.endswith(".pdf") and self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.show_page(self.current_page)

    def open_file(self):
        """開啟選定檔案"""
        if self.current_file:
            try:
                if os.name == "nt":  # Windows
                    os.startfile(self.current_file)
                elif os.name == "posix":  # macOS/Linux
                    os.system(f"open \"{self.current_file}\"")
            except Exception as e:
                self.pdf_display.setText(f"檔案開啟失敗：{str(e)}")
        else:
            self.pdf_display.setText("請先選擇檔案")

    def print_file(self):
        """列印當前檔案"""
        if self.current_file:
            try:
                if os.name == "nt":  # Windows
                    os.startfile(self.current_file, "print")
                elif os.name == "posix":  # macOS/Linux
                    os.system(f"lpr \"{self.current_file}\"")
            except Exception as e:
                self.pdf_display.setText(f"檔案列印失敗：{str(e)}")
        else:
            self.pdf_display.setText("請先選擇檔案")
            
    def go_to_home(self):
        """回到主頁"""
        self.close()
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Adjust button height to be 1/12 of the window height
        button_height = self.height() // 12

        # Adjust button font size based on button height
        button_font_size = button_height // 3
        button_font = QFont()
        button_font.setPointSize(button_font_size)

        # Set font for all buttons
        for button in [self.add_button, self.display_button, self.open_button, self.print_button, self.home_button, self.prev_page_button, self.next_page_button]:
            button.setFont(button_font)

        # Calculate the maximum width among all buttons
        max_button_width = max(self.add_button.sizeHint().width(),
                               self.display_button.sizeHint().width(),
                               self.open_button.sizeHint().width(),
                               self.print_button.sizeHint().width(),
                               self.home_button.sizeHint().width(),
                               self.prev_page_button.sizeHint().width(),
                               self.next_page_button.sizeHint().width())

        # Set the size for all buttons
        for button in [self.add_button, self.display_button, self.open_button, self.print_button, self.home_button, self.prev_page_button, self.next_page_button]:
            button.setFixedSize(max_button_width, button_height)

        # Adjust file selector height to be 1/20 of the window height
        file_selector_height = self.height() // 20
        self.file_selector.setFixedHeight(file_selector_height)
        self.file_selector.setFixedWidth(self.width() - 20)  # Adjust width to fit within the window

        # Adjust file selector font size
        file_selector_font = QFont()
        file_selector_font.setPointSize(button_font_size)
        self.file_selector.setFont(file_selector_font)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FormsPage()
    window.show()
    sys.exit(app.exec())