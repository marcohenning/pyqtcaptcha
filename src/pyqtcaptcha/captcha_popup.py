from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget
from .captcha_popup_content import CaptchaPopupContent
from .constants import *


class CaptchaPopup(QWidget):

    def __init__(self, parent: QWidget = None):
        super(CaptchaPopup, self).__init__(parent)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(CAPTCHA_POPUP_SIZE)

        self.__captcha_popup_content = CaptchaPopupContent(self)
        self.__captcha_popup_content.setFocus()
