from qtpy.QtCore import Qt
from qtpy.QtGui import QPainter, QPixmap, QPen
from qtpy.QtWidgets import QWidget, QPushButton
from .constants import *


class CaptchaImageButton(QPushButton):

    def __init__(self, parent: QWidget = None):
        super(CaptchaImageButton, self).__init__(parent)

        self.setStyleSheet('border: none; border-radius: 0px;')

        self.__image = None
        self.__selected = False
        
    def paintEvent(self, event) -> None:
        if self.__image:
            painter = QPainter(self)
            painter.drawPixmap(0, 0, self.__image)

            if self.__selected:
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)

                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(CAPTCHA_POPUP_ACCENT_COLOR)
                painter.drawEllipse(0, 0, 20, 20)

                painter.setPen(QPen(QColor('#FFF'), 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.SquareCap))
                painter.drawLine(4, 10, 8, 14)
                painter.drawLine(8, 14, 15, 6)

    def mousePressEvent(self, event) -> None:
        super().mousePressEvent(event)
        self.setSelected(not self.__selected)

    def getImage(self) -> QPixmap:
        return self.__image

    def setImage(self, image: QPixmap) -> None:
        self.__image = image
        self.setFixedSize(self.__image.size())

    def isSelected(self) -> bool:
        return self.__selected

    def setSelected(self, selected: bool) -> None:
        self.__selected = selected
        self.update()
