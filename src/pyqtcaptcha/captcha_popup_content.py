from qtpy.QtCore import Qt
from qtpy.QtGui import QPainter, QPixmap
from qtpy.QtWidgets import QWidget, QLabel, QPushButton
from .constants import *


class CaptchaPopupContent(QLabel):

    def __init__(self, parent: QWidget = None):
        super(CaptchaPopupContent, self).__init__(parent)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(CAPTCHA_POPUP_SIZE)
        self.setStyleSheet('background: #FFF; border: 1px solid gray; border-radius: 10px;')

        self.submit = QPushButton(self)
        self.submit.setText('SUBMIT')
        self.submit.setStyleSheet('QPushButton {color: #FFF; background: %s; border: none; border-radius: 5px;}'
                                  'QPushButton::pressed {color: #FFF; background: %s; border: none; border-radius: 5px;}'
                                  % (CAPTCHA_POPUP_ACCENT_COLOR.name(), CAPTCHA_POPUP_ACCENT_COLOR_PRESSED.name()))
        self.submit.setFixedSize(SUBMIT_BUTTON_SIZE)
        self.submit.move(SUBMIT_BUTTON_POSITION)
        self.submit.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        font = self.submit.font()
        font.setBold(True)
        self.submit.setFont(font)

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setPen(Qt.PenStyle.NoPen)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(CAPTCHA_POPUP_ACCENT_COLOR)
        painter.drawRoundedRect(8, 8, 314, 95, 5, 5)
        painter.drawRect(8, 38, 314, 65)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)

        painter.setBrush(QColor(150, 150, 150))

        width = 102

        painter.drawRect(IMAGE_COLUMN_1, IMAGE_ROW_1, width, width)
        painter.drawRect(IMAGE_COLUMN_1, IMAGE_ROW_2, width, width)
        painter.drawRect(IMAGE_COLUMN_1, IMAGE_ROW_3, width, width)

        painter.drawRect(IMAGE_COLUMN_2, IMAGE_ROW_1, width, width)
        painter.drawRect(IMAGE_COLUMN_2, IMAGE_ROW_2, width, width)
        painter.drawRect(IMAGE_COLUMN_2, IMAGE_ROW_3, width, width)

        painter.drawRect(IMAGE_COLUMN_3, IMAGE_ROW_1, width, width)
        painter.drawRect(IMAGE_COLUMN_3, IMAGE_ROW_2, width, width)
        painter.drawRect(IMAGE_COLUMN_3, IMAGE_ROW_3, width, width)

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.parent().close()
