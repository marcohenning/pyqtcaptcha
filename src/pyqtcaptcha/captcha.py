from qtpy.QtWidgets import QWidget, QPushButton
from .captcha_popup import CaptchaPopup


class Captcha(QPushButton):

    def __init__(self, parent: QWidget = None):
        super(Captcha, self).__init__(parent)

        self.__text = ''
        super().setText('')

        self.clicked.connect(self.__show_captcha)

    def __show_captcha(self):
        self.captcha = CaptchaPopup()
        self.captcha.move(750, 300)
        self.captcha.show()

    def text(self) -> str:
        return self.__text

    def setText(self, text: str) -> None:
        self.__text = text
