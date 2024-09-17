from qtpy.QtCore import Qt
from qtpy.QtGui import QPainter, QColor, QPixmap
from qtpy.QtWidgets import QWidget, QLabel, QPushButton


class CaptchaPopupContent(QLabel):

    def __init__(self, parent: QWidget = None):
        super(CaptchaPopupContent, self).__init__(parent)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(330, 476)
        self.setStyleSheet('background: #FFF; border: 1px solid gray; border-radius: 10px;')

        self.submit = QPushButton(self)
        self.submit.setText('SUBMIT')
        self.submit.setStyleSheet('color: #FFF; background: #1A73E8; border: none; border-radius: 5px')
        self.submit.setFixedSize(90, 36)
        self.submit.move(self.width() - self.submit.width() - 8, 432)
        font = self.submit.font()
        font.setBold(True)
        self.submit.setFont(font)

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setPen(Qt.PenStyle.NoPen)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(26, 115, 232))
        painter.drawRoundedRect(8, 8, 314, 95, 5, 5)
        painter.drawRect(8, 38, 314, 65)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)

        painter.setBrush(QColor(150, 150, 150))
        width = 102
        row_1 = 95 + 14 + 1
        row_2 = row_1 + width + 4
        row_3 = row_2 + width + 4
        col_1 = 8
        col_2 = col_1 + width + 4
        col_3 = col_2 + width + 4

        painter.drawRect(col_1, row_1, width, width)
        painter.drawRect(col_1, row_2, width, width)
        painter.drawRect(col_1, row_3, width, width)

        painter.drawRect(col_2, row_1, width, width)
        painter.drawRect(col_2, row_2, width, width)
        painter.drawRect(col_2, row_3, width, width)

        painter.drawRect(col_3, row_1, width, width)
        painter.drawRect(col_3, row_2, width, width)
        painter.drawRect(col_3, row_3, width, width)
