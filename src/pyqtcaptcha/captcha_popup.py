from qtpy.QtCore import Qt, Signal
from qtpy.QtWidgets import QWidget
from .captcha_popup_content import CaptchaPopupContent
from .constants import *


class CaptchaPopup(QWidget):

    aborted = Signal()
    failed = Signal()
    passed = Signal()

    def __init__(self, content: CaptchaPopupContent, position: QPoint, parent: QWidget = None):
        super(CaptchaPopup, self).__init__(parent)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(CAPTCHA_POPUP_SIZE_VISUAL)

        self.__captcha_popup_content = content
        self.__captcha_popup_content.setParent(self)
        self.__captcha_popup_content.setFocus()

        self.__position = position
        self.__update_position()

    def __update_position(self) -> None:
        self.move(QPoint(self.__position.x(), self.__position.y() - (self.height() // 2)))

    def resizeEvent(self, event) -> None:
        self.__update_position()

    def getContent(self) -> CaptchaPopupContent:
        return self.__captcha_popup_content

    def setContent(self, content: CaptchaPopupContent) -> None:
        self.__captcha_popup_content = content

    def getPosition(self) -> QPoint:
        return self.__position

    def setPosition(self, position: QPoint) -> None:
        self.__position = position
