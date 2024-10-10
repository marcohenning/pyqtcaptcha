import math
from qtpy.QtCore import Signal, Qt
from qtpy.QtGui import QColor, QPainter, QPen, QFont, QFontMetrics
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

    def paintEvent(self, event) -> None:
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setPen(QPen(QColor(150, 150, 150), 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.SquareCap))
        painter.setFont(QFont('Arial', 10))
        font_metrics = QFontMetrics(painter.font())
        rect = font_metrics.tightBoundingRect(self.__text)
        dimension = int(self.height() * 0.66)
        buffer = math.ceil((self.height() - dimension) / 2)

        print(self.height() - ((self.height() - dimension) // 2))

        painter.drawText(buffer * 2 + dimension, self.height() - math.floor((self.height() - rect.height()) / 2) - 1, self.__text)

        painter.drawRoundedRect(buffer, buffer, dimension, dimension, 5, 5)

        y_start = math.ceil(buffer + dimension / 2)
        painter.drawLine(buffer, y_start, buffer + ((buffer + int(dimension * 0.8)) - y_start), buffer + int(dimension * 0.8))
        x_start = buffer + ((buffer + int(dimension * 0.8)) - (buffer + dimension // 2))
        y_start = buffer + int(dimension * 0.8)
        y_end = buffer + int(dimension * 0.2)
        painter.drawLine(x_start, y_start, x_start + (y_start - y_end), y_end)

    def text(self) -> str:
        return self.__text

    def setText(self, text: str) -> None:
        self.__text = text
