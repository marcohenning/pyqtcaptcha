import math
from qtpy.QtCore import Signal, Qt, QTimeLine, QEasingCurve
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
        self.__passed = False
        self.resize(130, 39)
        super().setText('')

        self.__button_foreground_color = QColor(0, 0, 0)
        self.__button_background_color = QColor(255, 255, 255)
        self.__button_border_color = QColor(125, 125, 125)
        self.__button_border_width = 1
        self.__button_border_radius = 4
        self.__checkbox_color = QColor(125, 125, 125)
        self.__checkbox_width = 2
        self.__checkmark_color = CHECKMARK_COLOR

        self.__captcha_border_radius = 10
        self.__captcha_foreground_color = CAPTCHA_POPUP_FOREGROUND_COLOR
        self.__captcha_background_color = CAPTCHA_POPUP_BACKGROUND_COLOR
        self.__captcha_border_color = CAPTCHA_POPUP_BORDER_COLOR
        self.__captcha_primary_color = CAPTCHA_POPUP_PRIMARY_COLOR
        self.__captcha_primary_color_hover = CAPTCHA_POPUP_PRIMARY_COLOR_HOVER
        self.__captcha_secondary_color = CAPTCHA_POPUP_SECONDARY_COLOR
        self.__captcha_secondary_color_hover = CAPTCHA_POPUP_SECONDARY_COLOR_HOVER

        self.__timeline_checkmark_1 = QTimeLine(200)
        self.__timeline_checkmark_1.setEasingCurve(QEasingCurve.Type.InQuad)
        self.__timeline_checkmark_1.valueChanged.connect(self.update)

        self.__timeline_checkmark_2 = QTimeLine(300)
        self.__timeline_checkmark_2.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.__timeline_checkmark_2.valueChanged.connect(self.update)
        self.__timeline_checkmark_1.finished.connect(self.__timeline_checkmark_2.start)

        self.__update_style_sheet()
        self.__update_checkmark_timelines()

        self.clicked.connect(self.__show_captcha_popup)

    def __show_captcha_popup(self):
        if self.__passed:
            return

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

        actual_height = self.height() - self.__button_border_width * 2
        dimension = int(actual_height * 0.66)
        buffer = self.__button_border_width + math.ceil((actual_height - dimension) / 2)
        x_position = self.parent().mapToGlobal(self.pos()).x() + dimension + buffer * 2
        y_position = self.parent().mapToGlobal(self.pos()).y() + self.height() // 2

        self.__captcha_popup = CaptchaPopup(self.__captcha_popup_content, QPoint(x_position, y_position))
        self.__captcha_popup.show()
        self.__captcha_popup.aborted.connect(self.aborted.emit)
        self.__captcha_popup.failed.connect(self.failed.emit)
        self.__captcha_popup.passed.connect(self.__handle_passed)
        self.started.emit()

    def __handle_passed(self):
        self.__passed = True
        self.passed.emit()
        self.__timeline_checkmark_1.start()

    def __update_style_sheet(self):
        """Updates the stylesheet according to the current values."""

        self.setStyleSheet('color: %s;'
                           'background-color: %s;'
                           'border: %dpx solid %s;'
                           'border-radius: %dpx;'
                           % (self.__button_foreground_color.name(),
                              self.__button_background_color.name(),
                              self.__button_border_width,
                              self.__button_border_color.name(),
                              self.__button_border_radius))

    def paintEvent(self, event) -> None:
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setPen(QPen(self.__checkbox_color, self.__checkbox_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.SquareCap))
        painter.setFont(self.font())
        font_metrics = QFontMetrics(self.font())

        actual_height = self.height() - self.__button_border_width * 2
        dimension = int(actual_height * 0.66)
        buffer = self.__button_border_width + math.ceil((actual_height - dimension) / 2)

        rect = font_metrics.tightBoundingRect(self.__text)
        text_start_x = buffer * 2 + dimension
        text_start_y = self.height() - math.floor((self.height() - rect.height()) / 2) - 1
        max_text_width = self.width() - text_start_x - buffer
        text = font_metrics.elidedText(self.__text, Qt.ElideRight, max_text_width)

        painter.drawText(text_start_x, text_start_y, text)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if not self.__passed:
            painter.drawRoundedRect(buffer, buffer, dimension, dimension, int(dimension * 0.2), int(dimension * 0.2))
        else:
            painter.setPen(QPen(self.__checkmark_color, self.__checkbox_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.SquareCap))

            x_start_1 = buffer + int(dimension * 0.1)
            y_start_1 = math.ceil(buffer + dimension / 2)
            y_end_1 = buffer + int(dimension * 0.8)
            x_end_1 = x_start_1 + (y_end_1 - y_start_1)

            x_start_2 = x_end_1
            y_start_2 = y_end_1
            y_end_2 = buffer + int(dimension * 0.2)
            x_end_2 = x_start_2 + (y_start_2 - y_end_2)

            if self.__timeline_checkmark_1.state() == QTimeLine.State.Running:
                added = self.__timeline_checkmark_1.currentFrame()
                x_end_1 = x_start_1 + added
                y_end_1 = y_start_1 + added

                painter.drawLine(x_start_1, y_start_1, x_end_1, y_end_1)
                return

            elif self.__timeline_checkmark_2.state() == QTimeLine.State.Running:
                added = self.__timeline_checkmark_2.currentFrame()
                x_end_2 = x_start_2 + added
                y_end_2 = y_start_2 - added

            painter.drawLine(x_start_1, y_start_1, x_end_1, y_end_1)
            painter.drawLine(x_start_2, y_start_2, x_end_2, y_end_2)

    def __update_checkmark_timelines(self) -> None:
        actual_height = self.height() - self.__button_border_width * 2
        dimension = int(actual_height * 0.66)
        buffer = self.__button_border_width + math.ceil((actual_height - dimension) / 2)

        y_start_1 = math.ceil(buffer + dimension / 2)
        y_end_1 = buffer + int(dimension * 0.8)
        self.__timeline_checkmark_1.setFrameRange(0, y_end_1 - y_start_1)

        y_start_2 = y_end_1
        y_end_2 = buffer + int(dimension * 0.2)
        self.__timeline_checkmark_2.setFrameRange(0, y_start_2 - y_end_2)

    def resizeEvent(self, event) -> None:
        self.__update_checkmark_timelines()

    def text(self) -> str:
        return self.__text

    def setText(self, text: str) -> None:
        self.__text = text

    def getButtonForegroundColor(self) -> QColor:
        return self.__button_foreground_color

    def setButtonForegroundColor(self, color: QColor) -> None:
        self.__button_foreground_color = color
        self.__update_style_sheet()

    def getButtonBackgroundColor(self) -> QColor:
        return self.__button_background_color

    def setButtonBackgroundColor(self, color: QColor) -> None:
        self.__button_background_color = color
        self.__update_style_sheet()

    def getButtonBorderColor(self) -> QColor:
        return self.__button_border_color

    def setButtonBorderColor(self, color: QColor) -> None:
        self.__button_border_color = color
        self.__update_style_sheet()

    def getButtonBorderWidth(self) -> int:
        return self.__button_border_width

    def setButtonBorderWidth(self, width: int) -> None:
        self.__button_border_width = width
        self.__update_style_sheet()
        self.__update_checkmark_timelines()

    def getButtonBorderRadius(self) -> int:
        return self.__button_border_radius

    def setButtonBorderRadius(self, radius: int) -> None:
        self.__button_border_radius = radius
        self.__update_style_sheet()

    def getCheckboxColor(self) -> QColor:
        return self.__checkbox_color

    def setCheckboxColor(self, color: QColor) -> None:
        self.__checkbox_color = color

    def getCheckboxWidth(self) -> int:
        return self.__checkbox_width

    def setCheckboxWidth(self, width: int) -> None:
        self.__checkbox_width = width

    def getCheckmarkColor(self) -> QColor:
        return self.__checkmark_color

    def setCheckmarkColor(self, color: QColor) -> None:
        self.__checkmark_color = color

    def getCaptchaForegroundColor(self) -> QColor:
        return self.__captcha_foreground_color

    def setCaptchaForegroundColor(self, color: QColor) -> None:
        self.__captcha_foreground_color = color

    def getCaptchaBackgroundColor(self) -> QColor:
        return self.__captcha_background_color

    def setCaptchaBackgroundColor(self, color: QColor) -> None:
        self.__captcha_background_color = color

    def getCaptchaBorderColor(self) -> QColor:
        return self.__captcha_border_color

    def setCaptchaBorderColor(self, color: QColor) -> None:
        self.__captcha_border_color = color

    def getCaptchaBorderRadius(self) -> int:
        return self.__captcha_border_radius

    def setCaptchaBorderRadius(self, radius: int) -> None:
        self.__captcha_border_radius = radius

    def getCaptchaPrimaryColor(self) -> QColor:
        return self.__captcha_primary_color

    def setCaptchaPrimaryColor(self, color: QColor) -> None:
        self.__captcha_primary_color = color

    def getCaptchaPrimaryColorHovered(self) -> QColor:
        return self.__captcha_primary_color_hover

    def setCaptchaPrimaryColorHovered(self, color: QColor) -> None:
        self.__captcha_primary_color_hover = color

    def getCaptchaSecondaryColor(self) -> QColor:
        return self.__captcha_secondary_color

    def setCaptchaSecondaryColor(self, color: QColor) -> None:
        self.__captcha_secondary_color = color

    def getCaptchaSecondaryColorHovered(self) -> QColor:
        return self.__captcha_secondary_color_hover

    def setCaptchaSecondaryColorHovered(self, color: QColor) -> None:
        self.__captcha_secondary_color_hover = color

    def isPassed(self) -> bool:
        return self.__passed

    def reset(self) -> None:
        self.__passed = False
        self.update()
