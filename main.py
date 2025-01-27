from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from cases_fill import CasesFillPage
from cases_search import CasesSearchPage
from education_material import EducationMaterialPage
from forms import FormsPage


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
        btn_cases_fill = QPushButton("病例填寫")
        btn_cases_search = QPushButton("病例查詢")
        btn_education_material = QPushButton("衛教單張")
        btn_forms = QPushButton("表單")

        # 設定按鈕事件
        btn_cases_fill.clicked.connect(self.open_cases_fill_page)
        btn_cases_search.clicked.connect(self.open_cases_search_page)
        btn_education_material.clicked.connect(self.open_education_material_page)
        btn_forms.clicked.connect(self.open_forms_page)

        # 加入按鈕到佈局
        h_layout1.addWidget(btn_cases_fill)
        h_layout1.addWidget(btn_cases_search)
        h_layout2.addWidget(btn_education_material)
        h_layout2.addWidget(btn_forms)

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


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainPage()
    window.show()
    sys.exit(app.exec())
