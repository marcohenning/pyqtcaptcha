import sys
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QGridLayout
from src.pyqtcaptcha import Captcha


class Window(QMainWindow):

    def __init__(self):
        super().__init__(parent=None)

        # Window settings
        self.setWindowTitle('Example')
        self.resize(500, 300)

        # Create layout
        grid_layout = QGridLayout()
        captcha = Captcha()
        captcha.setFixedSize(130, 39)
        grid_layout.addWidget(captcha)

        # Apply layout
        central_widget = QWidget()
        central_widget.setLayout(grid_layout)
        self.setCentralWidget(central_widget)
        self.setFocus()


# Run the example
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
