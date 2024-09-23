from qtpy.QtCore import Qt, QTimeLine, QEasingCurve
from qtpy.QtGui import QPainter, QPixmap, QPen
from qtpy.QtWidgets import QWidget, QPushButton
from .constants import *


class CaptchaImageButton(QPushButton):

    def __init__(self, parent: QWidget = None):
        super(CaptchaImageButton, self).__init__(parent)

        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setStyleSheet('border: none; border-radius: 0px;')

        self.__image = None
        self.__selected = False
        self.__padding = 0
        self.__padding_max = 0
        self.__padding_min = 0
        self.__speed = 75

        self.__timeline_increase_padding = QTimeLine(self.__speed, self)
        self.__timeline_increase_padding.setFrameRange(self.__padding, self.__padding_max)
        self.__timeline_increase_padding.setEasingCurve(QEasingCurve.Type.Linear)
        self.__timeline_increase_padding.frameChanged.connect(self.__handle_timeline_increase_padding)

        self.__timeline_decrease_padding = QTimeLine(self.__speed, self)
        self.__timeline_decrease_padding.setFrameRange(self.__padding, self.__padding_min)
        self.__timeline_decrease_padding.setEasingCurve(QEasingCurve.Type.Linear)
        self.__timeline_decrease_padding.frameChanged.connect(self.__handle_timeline_decrease_padding)

    def __handle_timeline_increase_padding(self):
        self.__padding = self.__timeline_increase_padding.currentFrame()
        self.update()

    def __handle_timeline_decrease_padding(self):
        self.__padding = self.__timeline_decrease_padding.currentFrame()
        self.update()

    def paintEvent(self, event) -> None:
        if self.__image:
            painter = QPainter(self)

            if self.__padding == 0:
                painter.drawPixmap(0, 0, self.__image)
            else:
                image_scaled = self.__image.scaledToWidth(self.__image.width() - self.__padding * 2)
                painter.drawPixmap(self.__padding, self.__padding, image_scaled)

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

        if event.button() != Qt.MouseButton.LeftButton:
            return

        self.setSelected(not self.__selected)

        if self.isSelected():
            self.__timeline_decrease_padding.stop()
            self.__timeline_increase_padding.setFrameRange(self.__padding, self.__padding_max)
            self.__timeline_increase_padding.start()
        else:
            self.__timeline_increase_padding.stop()
            self.__timeline_decrease_padding.setFrameRange(self.__padding, self.__padding_min)
            self.__timeline_decrease_padding.start()

    def getImage(self) -> QPixmap:
        return self.__image

    def setImage(self, image: QPixmap) -> None:
        self.__image = image
        self.setFixedSize(self.__image.size())

        if self.size().width() == 102:
            self.__padding_max = 9
        elif self.size().width() == 77:
            self.__padding_max = 7

        self.update()

    def isSelected(self) -> bool:
        return self.__selected

    def setSelected(self, selected: bool) -> None:
        self.__selected = selected
        self.__timeline_increase_padding.stop()
        self.__timeline_decrease_padding.stop()
        self.__padding = 0

        self.update()
