from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class CasesFillPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("病例填寫")
        self.setGeometry(150, 150, 400, 300)

        layout = QVBoxLayout()
        label = QLabel("這是病例填寫頁面")
        label.setStyleSheet("font-size: 18px;")
        layout.addWidget(label)
        self.setLayout(layout)
