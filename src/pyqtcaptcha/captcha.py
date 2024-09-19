from qtpy.QtCore import Signal
from qtpy.QtWidgets import QWidget, QPushButton
from .captcha_popup import CaptchaPopup


class Captcha(QPushButton):

    started = Signal()
    aborted = Signal()

    def __init__(self, parent: QWidget = None):
        super(Captcha, self).__init__(parent)

        self.__captcha_popup = None
        self.__text = ''
        super().setText('')

        self.clicked.connect(self.__show_captcha_popup)

    def __show_captcha_popup(self):
        self.__captcha_popup = CaptchaPopup()
        self.__captcha_popup.move(750, 300)
        self.__captcha_popup.show()
        self.__captcha_popup.aborted.connect(self.aborted.emit)
        self.started.emit()

    def text(self) -> str:
        return self.__text

    def setText(self, text: str) -> None:
        self.__text = text
