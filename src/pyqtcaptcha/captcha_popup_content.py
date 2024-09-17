from qtpy.QtCore import Qt
from qtpy.QtGui import QPainter, QPixmap
from qtpy.QtWidgets import QWidget, QLabel, QPushButton
from .captcha_image_button import CaptchaImageButton
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

        self.__buttons_image = []
        self.__buttons_square = []

        self.__button_image_1 = CaptchaImageButton(self)
        self.__button_image_1.move(IMAGE_COLUMN_1, IMAGE_ROW_1)
        self.__buttons_image.append(self.__button_image_1)

        self.__button_image_2 = CaptchaImageButton(self)
        self.__button_image_2.move(IMAGE_COLUMN_2, IMAGE_ROW_1)
        self.__buttons_image.append(self.__button_image_2)

        self.__button_image_3 = CaptchaImageButton(self)
        self.__button_image_3.move(IMAGE_COLUMN_3, IMAGE_ROW_1)
        self.__buttons_image.append(self.__button_image_3)

        self.__button_image_4 = CaptchaImageButton(self)
        self.__button_image_4.move(IMAGE_COLUMN_1, IMAGE_ROW_2)
        self.__buttons_image.append(self.__button_image_4)

        self.__button_image_5 = CaptchaImageButton(self)
        self.__button_image_5.move(IMAGE_COLUMN_2, IMAGE_ROW_2)
        self.__buttons_image.append(self.__button_image_5)

        self.__button_image_6 = CaptchaImageButton(self)
        self.__button_image_6.move(IMAGE_COLUMN_3, IMAGE_ROW_2)
        self.__buttons_image.append(self.__button_image_6)

        self.__button_image_7 = CaptchaImageButton(self)
        self.__button_image_7.move(IMAGE_COLUMN_1, IMAGE_ROW_3)
        self.__buttons_image.append(self.__button_image_7)

        self.__button_image_8 = CaptchaImageButton(self)
        self.__button_image_8.move(IMAGE_COLUMN_2, IMAGE_ROW_3)
        self.__buttons_image.append(self.__button_image_8)

        self.__button_image_9 = CaptchaImageButton(self)
        self.__button_image_9.move(IMAGE_COLUMN_3, IMAGE_ROW_3)
        self.__buttons_image.append(self.__button_image_9)

        self.__button_square_1 = CaptchaImageButton(self)
        self.__button_square_1.move(SQUARE_COLUMN_1, SQUARE_ROW_1)
        self.__buttons_square.append(self.__button_square_1)

        self.__button_square_2 = CaptchaImageButton(self)
        self.__button_square_2.move(SQUARE_COLUMN_2, SQUARE_ROW_1)
        self.__buttons_square.append(self.__button_square_2)

        self.__button_square_3 = CaptchaImageButton(self)
        self.__button_square_3.move(SQUARE_COLUMN_3, SQUARE_ROW_1)
        self.__buttons_square.append(self.__button_square_3)

        self.__button_square_4 = CaptchaImageButton(self)
        self.__button_square_4.move(SQUARE_COLUMN_4, SQUARE_ROW_1)
        self.__buttons_square.append(self.__button_square_4)

        self.__button_square_5 = CaptchaImageButton(self)
        self.__button_square_5.move(SQUARE_COLUMN_1, SQUARE_ROW_2)
        self.__buttons_square.append(self.__button_square_5)

        self.__button_square_6 = CaptchaImageButton(self)
        self.__button_square_6.move(SQUARE_COLUMN_2, SQUARE_ROW_2)
        self.__buttons_square.append(self.__button_square_6)

        self.__button_square_7 = CaptchaImageButton(self)
        self.__button_square_7.move(SQUARE_COLUMN_3, SQUARE_ROW_2)
        self.__buttons_square.append(self.__button_square_7)

        self.__button_square_8 = CaptchaImageButton(self)
        self.__button_square_8.move(SQUARE_COLUMN_4, SQUARE_ROW_2)
        self.__buttons_square.append(self.__button_square_8)

        self.__button_square_9 = CaptchaImageButton(self)
        self.__button_square_9.move(SQUARE_COLUMN_1, SQUARE_ROW_3)
        self.__buttons_square.append(self.__button_square_9)

        self.__button_square_10 = CaptchaImageButton(self)
        self.__button_square_10.move(SQUARE_COLUMN_2, SQUARE_ROW_3)
        self.__buttons_square.append(self.__button_square_10)

        self.__button_square_11 = CaptchaImageButton(self)
        self.__button_square_11.move(SQUARE_COLUMN_3, SQUARE_ROW_3)
        self.__buttons_square.append(self.__button_square_11)

        self.__button_square_12 = CaptchaImageButton(self)
        self.__button_square_12.move(SQUARE_COLUMN_4, SQUARE_ROW_3)
        self.__buttons_square.append(self.__button_square_12)

        self.__button_square_13 = CaptchaImageButton(self)
        self.__button_square_13.move(SQUARE_COLUMN_1, SQUARE_ROW_4)
        self.__buttons_square.append(self.__button_square_13)

        self.__button_square_14 = CaptchaImageButton(self)
        self.__button_square_14.move(SQUARE_COLUMN_2, SQUARE_ROW_4)
        self.__buttons_square.append(self.__button_square_14)

        self.__button_square_15 = CaptchaImageButton(self)
        self.__button_square_15.move(SQUARE_COLUMN_3, SQUARE_ROW_4)
        self.__buttons_square.append(self.__button_square_15)

        self.__button_square_16 = CaptchaImageButton(self)
        self.__button_square_16.move(SQUARE_COLUMN_4, SQUARE_ROW_4)
        self.__buttons_square.append(self.__button_square_16)

        for button in self.__buttons_image:
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            button.setVisible(False)

        for button in self.__buttons_square:
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            button.setVisible(False)

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setPen(Qt.PenStyle.NoPen)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(CAPTCHA_POPUP_ACCENT_COLOR)
        painter.drawRoundedRect(8, 8, 314, 95, 5, 5)
        painter.drawRect(8, 38, 314, 65)

        self.image = QPixmap(DIRECTORY + '/files/square/6.png')
        dimension = 77

        self.__button_square_1.setImage(self.image.copy(0, 0, dimension, dimension))
        self.__button_square_2.setImage(self.image.copy(dimension, 0, dimension, dimension))
        self.__button_square_3.setImage(self.image.copy(dimension * 2, 0, dimension, dimension))
        self.__button_square_4.setImage(self.image.copy(dimension * 3, 0, dimension, dimension))

        self.__button_square_5.setImage(self.image.copy(0, dimension, dimension, dimension))
        self.__button_square_6.setImage(self.image.copy(dimension, dimension, dimension, dimension))
        self.__button_square_7.setImage(self.image.copy(dimension * 2, dimension, dimension, dimension))
        self.__button_square_8.setImage(self.image.copy(dimension * 3, dimension, dimension, dimension))

        self.__button_square_9.setImage(self.image.copy(0, dimension * 2, dimension, dimension))
        self.__button_square_10.setImage(self.image.copy(dimension, dimension * 2, dimension, dimension))
        self.__button_square_11.setImage(self.image.copy(dimension * 2, dimension * 2, dimension, dimension))
        self.__button_square_12.setImage(self.image.copy(dimension * 3, dimension * 2, dimension, dimension))

        self.__button_square_13.setImage(self.image.copy(0, dimension * 3, dimension, dimension))
        self.__button_square_14.setImage(self.image.copy(dimension, dimension * 3, dimension, dimension))
        self.__button_square_15.setImage(self.image.copy(dimension * 2, dimension * 3, dimension, dimension))
        self.__button_square_16.setImage(self.image.copy(dimension * 3, dimension * 3, dimension, dimension))

        for button in self.__buttons_square:
            button.setVisible(True)

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.parent().close()
