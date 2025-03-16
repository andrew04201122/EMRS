from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from cases_fill import CasesFillPage
from cases_search import CasesSearchPage
from education_material import EducationMaterialPage
from forms import FormsPage
from PySide6.QtGui import QFont


class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("主頁面")
        self.setGeometry(100, 100, 400, 300)

        # 主要容器
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 佈局與按鈕
        main_layout = QVBoxLayout()
        grid_layout = QVBoxLayout()

        h_layout1 = QHBoxLayout()
        h_layout2 = QHBoxLayout()

        # 按鈕
        self.btn_cases_fill = QPushButton("病例填寫")
        self.btn_cases_search = QPushButton("病例查詢")
        self.btn_education_material = QPushButton("衛教單張")
        self.btn_forms = QPushButton("表單")

        # 設定按鈕事件
        self.btn_cases_fill.clicked.connect(self.open_cases_fill_page)
        self.btn_cases_search.clicked.connect(self.open_cases_search_page)
        self.btn_education_material.clicked.connect(self.open_education_material_page)
        self.btn_forms.clicked.connect(self.open_forms_page)

        # 加入按鈕到佈局
        h_layout1.addWidget(self.btn_cases_fill)
        h_layout1.addWidget(self.btn_cases_search)
        h_layout2.addWidget(self.btn_education_material)
        h_layout2.addWidget(self.btn_forms)

        grid_layout.addLayout(h_layout1)
        grid_layout.addLayout(h_layout2)
        main_layout.addLayout(grid_layout)

        central_widget.setLayout(main_layout)

    def open_cases_fill_page(self):
        self.cases_fill_page = CasesFillPage()
        self.cases_fill_page.show()

    def open_cases_search_page(self):
        self.cases_search_page = CasesSearchPage()
        self.cases_search_page.show()

    def open_education_material_page(self):
        self.education_material_page = EducationMaterialPage()
        self.education_material_page.show()

    def open_forms_page(self):
        self.forms_page = FormsPage()
        self.forms_page.show()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Adjust button height to be 1/5 of the window height
        button_height = self.height() // 5
        # Adjust button font size based on button height
        button_font_size = button_height // 3
        button_font = QFont()
        button_font.setPointSize(button_font_size)

        # Set font for all buttons
        for button in [self.btn_cases_fill, self.btn_cases_search, self.btn_education_material, self.btn_forms]:
            button.setFont(button_font)

        # Calculate the maximum width among all buttons
        max_button_width = max(self.btn_cases_fill.sizeHint().width(),
                               self.btn_cases_search.sizeHint().width(),
                               self.btn_education_material.sizeHint().width(),
                               self.btn_forms.sizeHint().width())

        # Set the size for all buttons
        for button in [self.btn_cases_fill, self.btn_cases_search, self.btn_education_material, self.btn_forms]:
            button.setFixedSize(max_button_width, button_height)

        # Ensure text fits within the button
        for button in [self.btn_cases_fill, self.btn_cases_search, self.btn_education_material, self.btn_forms]:
            font_metrics = self.fontMetrics()
            while font_metrics.boundingRect(button.text()).width() > button.width() - 10 or font_metrics.boundingRect(button.text()).height() > button.height() - 10:
                button_font_size -= 1
                button_font.setPointSize(button_font_size)
                button.setFont(button_font)
                font_metrics = self.fontMetrics()

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainPage()
    window.show()
    sys.exit(app.exec())
