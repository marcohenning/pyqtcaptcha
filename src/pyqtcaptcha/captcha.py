from qtpy.QtCore import Signal
from qtpy.QtWidgets import QWidget, QPushButton
from .captcha_popup import CaptchaPopup


class Captcha(QPushButton):

    started = Signal()

    def __init__(self, parent: QWidget = None):
        super(Captcha, self).__init__(parent)

        self.__text = ''
        super().setText('')

        self.clicked.connect(self.__show_captcha_popup)

    def __show_captcha_popup(self):
        self.__captcha_popup = CaptchaPopup()
        self.__captcha_popup.move(750, 300)
        self.__captcha_popup.show()
        self.started.emit()

    def text(self) -> str:
        return self.__text

    def setText(self, text: str) -> None:
        self.__text = text
