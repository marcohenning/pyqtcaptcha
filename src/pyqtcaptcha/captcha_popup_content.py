import os
import random
from qtpy.QtCore import Qt
from qtpy.QtGui import QPainter, QPixmap, QPen, QFont, QFontMetrics, QImage
from qtpy.QtWidgets import QWidget, QLabel, QPushButton
from .captcha_image_button import CaptchaImageButton
from .captcha_icon_button import CaptchaIconButton
from .captcha_enums import CaptchaType, CaptchaTask, CaptchaDifficulty
from .constants import *


class CaptchaPopupContent(QLabel):

    def __init__(self, parent: QWidget = None):
        super(CaptchaPopupContent, self).__init__(parent)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(CAPTCHA_POPUP_SIZE)
        self.setStyleSheet('background: #FFF; border: 1px solid gray; border-radius: 10px;')

        self.__type = CaptchaType.VISUAL
        self.__task = CaptchaTask.IMAGE
        self.__difficulty = CaptchaDifficulty.MEDIUM
        self.__file = None

        self.submit = QPushButton(self)
        self.submit.setText('SUBMIT')
        self.submit.setStyleSheet('QPushButton {color: #FFF; background: %s; border: none; border-radius: 5px;}'
                                  'QPushButton::hover {color: #FFF; background: %s; border: none; border-radius: 5px;}'
                                  % (CAPTCHA_POPUP_ACCENT_COLOR.name(), CAPTCHA_POPUP_ACCENT_COLOR_PRESSED.name()))
        self.submit.setFixedSize(SUBMIT_BUTTON_SIZE)
        self.submit.move(SUBMIT_BUTTON_POSITION)
        self.submit.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.submit.clicked.connect(self.__handle_submit)

        font = self.submit.font()
        font.setBold(True)
        self.submit.setFont(font)

        self.__button_refresh = CaptchaIconButton(self)
        self.__button_refresh.move(8, SUBMIT_BUTTON_POSITION.y())
        self.__button_refresh.setIcon(QImage(DIRECTORY + '/files/icons/refresh.png'))
        self.__button_refresh.clicked.connect(self.__handle_refresh)

        self.__button_visual = CaptchaIconButton(self)
        self.__button_visual.move(44, SUBMIT_BUTTON_POSITION.y())
        self.__button_visual.setIcon(QImage(DIRECTORY + '/files/icons/eye.png'))
        self.__button_visual.setVisible(False)

        self.__button_audio = CaptchaIconButton(self)
        self.__button_audio.move(44, SUBMIT_BUTTON_POSITION.y())
        self.__button_audio.setIcon(QImage(DIRECTORY + '/files/icons/headphones.png'))
        self.__button_audio.clicked.connect(self.__handle_audio)

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
            button.setVisible(False)

        for button in self.__buttons_square:
            button.setVisible(False)

    def __handle_submit(self):
        pass

    def __handle_refresh(self):
        self.__load_next_task()

    def __handle_visual(self):
        pass

    def __handle_audio(self):
        pass

    def __load_next_task(self):
        if self.__type == CaptchaType.VISUAL:
            if self.__difficulty == CaptchaDifficulty.EASY:
                self.__task = CaptchaTask.IMAGE
            elif self.__difficulty == CaptchaDifficulty.HARD:
                self.__task = CaptchaTask.SQUARE
            else:
                self.__task = CaptchaTask(random.randint(1, 2))
        else:
            self.__task = CaptchaTask.AUDIO

        if self.__task == CaptchaTask.IMAGE:
            self.__file = self.__find_random_task('image')
            self.__load_images()

        elif self.__task == CaptchaTask.SQUARE:
            self.__file = self.__find_random_task('square')
            self.__load_squares()

        else:
            self.__file = self.__find_random_task('audio')
            self.__load_audio()

    def __find_random_task(self, folder: str) -> int:
        tasks = os.listdir(DIRECTORY + '/files/' + folder)
        if len(tasks) == 0:
            return -1
        task = self.__file
        while task == self.__file:
            task = random.randint(1, len(tasks))
        return task

    def __load_images(self):
        pass

    def __load_squares(self):

        image = QPixmap(DIRECTORY + '/files/square/{}.png'.format(self.__file))

        self.__button_square_1.setImage(image.copy(SQUARE_SIZE * 0, SQUARE_SIZE * 0, SQUARE_SIZE, SQUARE_SIZE))
        self.__button_square_2.setImage(image.copy(SQUARE_SIZE * 1, SQUARE_SIZE * 0, SQUARE_SIZE, SQUARE_SIZE))
        self.__button_square_3.setImage(image.copy(SQUARE_SIZE * 2, SQUARE_SIZE * 0, SQUARE_SIZE, SQUARE_SIZE))
        self.__button_square_4.setImage(image.copy(SQUARE_SIZE * 3, SQUARE_SIZE * 0, SQUARE_SIZE, SQUARE_SIZE))

        self.__button_square_5.setImage(image.copy(SQUARE_SIZE * 0, SQUARE_SIZE * 1, SQUARE_SIZE, SQUARE_SIZE))
        self.__button_square_6.setImage(image.copy(SQUARE_SIZE * 1, SQUARE_SIZE * 1, SQUARE_SIZE, SQUARE_SIZE))
        self.__button_square_7.setImage(image.copy(SQUARE_SIZE * 2, SQUARE_SIZE * 1, SQUARE_SIZE, SQUARE_SIZE))
        self.__button_square_8.setImage(image.copy(SQUARE_SIZE * 3, SQUARE_SIZE * 1, SQUARE_SIZE, SQUARE_SIZE))

        self.__button_square_9.setImage(image.copy(SQUARE_SIZE * 0, SQUARE_SIZE * 2, SQUARE_SIZE, SQUARE_SIZE))
        self.__button_square_10.setImage(image.copy(SQUARE_SIZE * 1, SQUARE_SIZE * 2, SQUARE_SIZE, SQUARE_SIZE))
        self.__button_square_11.setImage(image.copy(SQUARE_SIZE * 2, SQUARE_SIZE * 2, SQUARE_SIZE, SQUARE_SIZE))
        self.__button_square_12.setImage(image.copy(SQUARE_SIZE * 3, SQUARE_SIZE * 2, SQUARE_SIZE, SQUARE_SIZE))

        self.__button_square_13.setImage(image.copy(SQUARE_SIZE * 0, SQUARE_SIZE * 3, SQUARE_SIZE, SQUARE_SIZE))
        self.__button_square_14.setImage(image.copy(SQUARE_SIZE * 1, SQUARE_SIZE * 3, SQUARE_SIZE, SQUARE_SIZE))
        self.__button_square_15.setImage(image.copy(SQUARE_SIZE * 2, SQUARE_SIZE * 3, SQUARE_SIZE, SQUARE_SIZE))
        self.__button_square_16.setImage(image.copy(SQUARE_SIZE * 3, SQUARE_SIZE * 3, SQUARE_SIZE, SQUARE_SIZE))

        for button in self.__buttons_image:
            button.setVisible(False)

        for button in self.__buttons_square:
            button.setSelected(False)
            button.setVisible(True)

    def __load_audio(self):
        pass

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setPen(Qt.PenStyle.NoPen)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(CAPTCHA_POPUP_ACCENT_COLOR)
        painter.drawRoundedRect(8, 8, 314, 95, 5, 5)
        painter.drawRect(8, 38, 314, 65)

        painter.setPen(QPen(QColor('#FFF'), 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.SquareCap))
        painter.setFont(QFont('Arial', 12))
        font_metrics = QFontMetrics(painter.font())
        height = font_metrics.tightBoundingRect('Select all squares with').height()
        painter.drawText(16, 40, 'Select all squares with')

        font_large = painter.font()
        font_large.setPointSize(15)
        font_large.setBold(True)
        painter.setFont(font_large)
        painter.drawText(16, 40 + height + int(height * 0.5), 'traffic lights')

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.parent().aborted.emit()
        self.parent().close()
