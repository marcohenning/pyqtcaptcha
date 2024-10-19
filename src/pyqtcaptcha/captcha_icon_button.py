from qtpy.QtCore import Qt
from qtpy.QtGui import QImage, QPixmap, QPainter, qRgba
from qtpy.QtWidgets import QWidget, QPushButton
from .constants import *


class CaptchaIconButton(QPushButton):

    def __init__(self, parent: QWidget = None):
        super(CaptchaIconButton, self).__init__(parent)

        self.setFixedSize(ICON_BUTTON_SIZE)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setStyleSheet('border: none; border-radius: 0px;')

        self.__icon = None
        self.__icon_hover = None
        self.__hover = False
        self.__color = QColor()
        self.__color_hover = QColor()

    def __recolor_icon(self, icon: QImage, color: QColor) -> QPixmap:
        for x in range(0, icon.width()):
            for y in range(0, icon.height()):
                current_color = icon.pixelColor(x, y)
                new_color_r = color.red()
                new_color_g = color.green()
                new_color_b = color.blue()
                new_color = QColor.fromRgba(
                    qRgba(new_color_r, new_color_g, new_color_b, current_color.alpha()))
                icon.setPixelColor(x, y, new_color)

        icon_pixmap = QPixmap.fromImage(icon)
        return icon_pixmap

    def paintEvent(self, event) -> None:
        if not self.__icon or not self.__icon_hover:
            return

        painter = QPainter(self)
        buffer = (self.width() - self.__icon.width()) // 2

        if not self.__hover:
            painter.drawPixmap(buffer, buffer, self.__icon)
        else:
            painter.drawPixmap(buffer, buffer, self.__icon_hover)

    def enterEvent(self, event) -> None:
        super().enterEvent(event)
        self.__hover = True
        self.update()

    def leaveEvent(self, event) -> None:
        super().leaveEvent(event)
        self.__hover = False
        self.update()

    def setVisible(self, visible: bool) -> None:
        super().setVisible(visible)
        self.__hover = False

    def getIcon(self) -> QPixmap:
        return self.__icon

    def getIconHover(self) -> QPixmap:
        return self.__icon_hover

    def setIcon(self, icon: QImage) -> None:
        self.__icon = self.__recolor_icon(icon, self.__color)
        self.__icon_hover = self.__recolor_icon(icon, self.__color_hover)
        self.update()

    def getColor(self) -> QColor:
        return self.__color

    def setColor(self, color: QColor) -> None:
        self.__color = color

    def getHoveredColor(self) -> QColor:
        return self.__color_hover

    def setHoveredColor(self, color: QColor) -> None:
        self.__color_hover = color
