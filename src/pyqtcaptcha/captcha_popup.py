from qtpy.QtCore import Qt, Signal
from qtpy.QtWidgets import QWidget
from .captcha_popup_content import CaptchaPopupContent
from .constants import *


class CaptchaPopup(QWidget):

    # Signals to be emitted
    aborted = Signal()
    failed = Signal()
    passed = Signal()

    def __init__(self, content: CaptchaPopupContent, position: QPoint, parent: QWidget = None):
        """Create a new CaptchaPopup instance

        :param content: the popup's content
        :param position: the popup's position
        :param parent: the parent widget
        """

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
        """Handle updating the position on widget resize"""

        self.move(QPoint(self.__position.x(), self.__position.y() - (self.height() // 2)))

    def resizeEvent(self, event) -> None:
        """Gets called every time the widget gets resized

        :param event: the event sent by PyQt
        """

        self.__update_position()

    def getContent(self) -> CaptchaPopupContent:
        """Get the current content

        :return: content
        """

        return self.__captcha_popup_content

    def setContent(self, content: CaptchaPopupContent) -> None:
        """Set the content

        :param content: new content
        """

        self.__captcha_popup_content = content

    def getPosition(self) -> QPoint:
        """Get the current position

        :return: position
        """

        return self.__position

    def setPosition(self, position: QPoint) -> None:
        """Set the position

        :param position: new position
        """

        self.__position = position
