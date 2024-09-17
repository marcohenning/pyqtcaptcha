from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget
from .captcha_popup_content import CaptchaPopupContent


class CaptchaPopup(QWidget):

    def __init__(self, parent: QWidget = None):
        super(CaptchaPopup, self).__init__(parent)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(330, 476)

        self.widget = CaptchaPopupContent(self)
