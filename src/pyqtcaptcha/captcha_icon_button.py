from qtpy.QtCore import Qt
from qtpy.QtGui import QImage, QPixmap, QPainter, qRgba
from qtpy.QtWidgets import QWidget, QPushButton
from .constants import *


class CaptchaIconButton(QPushButton):

    def __init__(self, parent: QWidget = None):
        """Create a new CaptchaIconButton instance

        :param parent: the parent widget
        """

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
        """Recolor the icon

        :param icon: icon to be recolored
        :param color: new icon color
        :return: recolored icon
        """

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
        """Handle drawing the widget

        :param event: the event sent by PyQt
        """

        if not self.__icon or not self.__icon_hover:
            return

        painter = QPainter(self)
        buffer = (self.width() - self.__icon.width()) // 2

        if not self.__hover:
            painter.drawPixmap(buffer, buffer, self.__icon)
        else:
            painter.drawPixmap(buffer, buffer, self.__icon_hover)

    def enterEvent(self, event) -> None:
        """Event that happens every time the mouse enters this widget

        :param event: the event sent by PyQt
        """

        super().enterEvent(event)
        self.__hover = True
        self.update()

    def leaveEvent(self, event) -> None:
        """Event that happens every time the mouse leaves this widget

        :param event: the event sent by PyQt
        """

        super().leaveEvent(event)
        self.__hover = False
        self.update()

    def setVisible(self, visible: bool) -> None:
        """Change the visibility of the widget

        :param visible: new visibility
        """

        super().setVisible(visible)
        self.__hover = False

    def getIcon(self) -> QPixmap:
        """Get the current icon

        :return: icon
        """

        return self.__icon

    def getIconHover(self) -> QPixmap:
        """Get the current hovered icon

        :return: hovered icon
        """

        return self.__icon_hover

    def setIcon(self, icon: QImage) -> None:
        """Set the icon

        :param icon: new icon
        """

        self.__icon = self.__recolor_icon(icon, self.__color)
        self.__icon_hover = self.__recolor_icon(icon, self.__color_hover)
        self.update()

    def getColor(self) -> QColor:
        """Get the current color

        :return: color
        """

        return self.__color

    def setColor(self, color: QColor) -> None:
        """Set the color

        :param color: new color
        """

        self.__color = color

    def getHoveredColor(self) -> QColor:
        """Get the current hovered color

        :return: hovered color
        """

        return self.__color_hover

    def setHoveredColor(self, color: QColor) -> None:
        """Set the hovered color

        :param color: new hovered color
        """

        self.__color_hover = color

    def isHovered(self) -> bool:
        """Is the widget currently being hovered over?

        :return: is the widget hovered
        """

        return self.__hover
