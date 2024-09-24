from qtpy.QtCore import Signal
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QWidget, QPushButton
from .captcha_popup import CaptchaPopup
from .captcha_popup_content import CaptchaPopupContent
from .constants import *


class Captcha(QPushButton):

    started = Signal()
    aborted = Signal()
    failed = Signal()
    passed = Signal()

    def __init__(self, parent: QWidget = None):
        super(Captcha, self).__init__(parent)

        self.__captcha_popup = None
        self.__text = ''
        super().setText('')

        self.__captcha_border_radius = 10
        self.__captcha_foreground_color = CAPTCHA_POPUP_FOREGROUND_COLOR
        self.__captcha_background_color = CAPTCHA_POPUP_BACKGROUND_COLOR
        self.__captcha_border_color = CAPTCHA_POPUP_BORDER_COLOR
        self.__captcha_primary_color = CAPTCHA_POPUP_PRIMARY_COLOR
        self.__captcha_primary_color_hover = CAPTCHA_POPUP_PRIMARY_COLOR_HOVER
        self.__captcha_secondary_color = CAPTCHA_POPUP_SECONDARY_COLOR
        self.__captcha_secondary_color_hover = CAPTCHA_POPUP_SECONDARY_COLOR_HOVER

        self.clicked.connect(self.__show_captcha_popup)

    def __show_captcha_popup(self):
        self.__captcha_popup_content = CaptchaPopupContent(
            self.__captcha_border_radius,
            self.__captcha_foreground_color,
            self.__captcha_background_color,
            self.__captcha_border_color,
            self.__captcha_primary_color,
            self.__captcha_primary_color_hover,
            self.__captcha_secondary_color,
            self.__captcha_secondary_color_hover
        )
        self.__captcha_popup = CaptchaPopup(self.__captcha_popup_content)
        self.__captcha_popup.move(750, 300)
        self.__captcha_popup.show()
        self.__captcha_popup.aborted.connect(self.aborted.emit)
        self.__captcha_popup.failed.connect(self.failed.emit)
        self.__captcha_popup.passed.connect(self.passed.emit)
        self.started.emit()

    def text(self) -> str:
        return self.__text

    def setText(self, text: str) -> None:
        self.__text = text
