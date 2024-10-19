import random
import contextlib
with contextlib.redirect_stdout(None):  # Suppress import message
    from pygame import mixer
from qtpy.QtCore import Qt
from qtpy.QtGui import QPainter, QPixmap, QPen, QFont, QFontMetrics, QImage
from qtpy.QtWidgets import QWidget, QLabel, QPushButton
from .captcha_image_button import CaptchaImageButton
from .captcha_icon_button import CaptchaIconButton
from .captcha_textfield import CaptchaTextField
from .captcha_enums import CaptchaType, CaptchaTask, CaptchaDifficulty
from .image_labels import image_labels, image_label_types
from .square_labels import square_labels
from .audio_labels import audio_labels
from .constants import *


class CaptchaPopupContent(QLabel):

    def __init__(
        self,
        border_radius: int,
        foreground_color: QColor,
        background_color: QColor,
        border_color: QColor,
        primary_color: QColor,
        primary_color_hover: QColor,
        secondary_color: QColor,
        secondary_color_hover: QColor,
        parent: QWidget = None
    ):

        super(CaptchaPopupContent, self).__init__(parent)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(CAPTCHA_POPUP_SIZE_VISUAL)

        self.__type = CaptchaType.VISUAL
        self.__task = CaptchaTask.IMAGE
        self.__difficulty = CaptchaDifficulty.MEDIUM
        self.__files = [1]
        self.__task_category = image_label_types[0]

        self.__border_radius = border_radius
        self.__foreground_color = foreground_color
        self.__background_color = background_color
        self.__border_color = border_color
        self.__primary_color = primary_color
        self.__primary_color_hover = primary_color_hover
        self.__secondary_color = secondary_color
        self.__secondary_color_hover = secondary_color_hover

        self.setStyleSheet('background: {}; border: 1px solid {}; border-radius: {}px;'
                           .format(self.__background_color.name(),
                                   self.__border_color.name(),
                                   self.__border_radius))
        mixer.init()

        self.submit = QPushButton(self)
        self.submit.setText('SUBMIT')
        self.submit.setStyleSheet('QPushButton {color: %s; background: %s; border: none; border-radius: %spx;}'
                                  'QPushButton::hover {color: %s; background: %s; border: none; border-radius: %spx;}'
                                  % (self.__foreground_color.name(),
                                     self.__primary_color.name(),
                                     self.__border_radius // 2,
                                     self.__foreground_color.name(),
                                     self.__primary_color_hover.name(),
                                     self.__border_radius // 2))
        self.submit.setFixedSize(SUBMIT_BUTTON_SIZE)
        self.submit.move(SUBMIT_BUTTON_POSITION_VISUAL)
        self.submit.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.submit.clicked.connect(self.__handle_submit)

        font = self.submit.font()
        font.setBold(True)
        self.submit.setFont(font)

        self.__button_refresh = CaptchaIconButton(self)
        self.__button_refresh.move(8, SUBMIT_BUTTON_POSITION_VISUAL.y())
        self.__button_refresh.setColor(self.__secondary_color)
        self.__button_refresh.setHoveredColor(self.__secondary_color_hover)
        self.__button_refresh.setIcon(QImage(DIRECTORY + '/files/icons/refresh.png'))
        self.__button_refresh.clicked.connect(self.__handle_refresh)

        self.__button_visual = CaptchaIconButton(self)
        self.__button_visual.move(44, SUBMIT_BUTTON_POSITION_VISUAL.y())
        self.__button_visual.setColor(self.__secondary_color)
        self.__button_visual.setHoveredColor(self.__secondary_color_hover)
        self.__button_visual.setIcon(QImage(DIRECTORY + '/files/icons/eye.png'))
        self.__button_visual.setVisible(False)
        self.__button_visual.clicked.connect(self.__handle_visual)

        self.__button_audio = CaptchaIconButton(self)
        self.__button_audio.move(44, SUBMIT_BUTTON_POSITION_VISUAL.y())
        self.__button_audio.setColor(self.__secondary_color)
        self.__button_audio.setHoveredColor(self.__secondary_color_hover)
        self.__button_audio.setIcon(QImage(DIRECTORY + '/files/icons/headphones.png'))
        self.__button_audio.clicked.connect(self.__handle_audio)

        self.__button_play = QPushButton(self)
        self.__button_play.setText('PLAY')
        self.__button_play.setStyleSheet('QPushButton {color: %s; background: %s; border: none; border-radius: %spx;}'
                                         'QPushButton::hover {color: %s; background: %s; border: none; border-radius: %spx;}'
                                          % (self.__foreground_color.name(),
                                          self.__secondary_color.name(),
                                          self.__border_radius // 2,
                                          self.__foreground_color.name(),
                                          self.__secondary_color_hover.name(),
                                          self.__border_radius // 2))
        self.__button_play.setFixedSize(314, 60)
        self.__button_play.move(IMAGE_COLUMN_1, IMAGE_ROW_1)
        self.__button_play.setFont(font)
        self.__button_play.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.__button_play.setVisible(False)
        self.__button_play.clicked.connect(self.__handle_play)

        self.__textfield_audio = CaptchaTextField(self)
        self.__textfield_audio.setPlaceholderText('What did you hear?')
        self.__textfield_audio.setStyleSheet('color: %s; background: %s; border: 1px solid %s; border-radius: %spx; padding: 0 10 0 10px;'
                                             % (self.__secondary_color.name(),
                                                self.__background_color.name(),
                                                self.__secondary_color.name(),
                                                self.__border_radius // 2))
        self.__textfield_audio.setFixedSize(314, 45)
        self.__textfield_audio.move(IMAGE_COLUMN_1, IMAGE_ROW_1 + 67)
        font.setBold(False)
        self.__textfield_audio.setFont(font)
        self.__textfield_audio.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.__textfield_audio.setVisible(False)
        self.__textfield_audio.focus_out.connect(self.__handle_focus)

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

        self.__load_next_task()

    def __handle_submit(self):
        if self.__task == CaptchaTask.IMAGE:
            self.__validate_images()
        elif self.__task == CaptchaTask.SQUARE:
            self.__validate_squares()
        else:
            self.__validate_audio()

    def __handle_refresh(self):
        self.__load_next_task()

    def __handle_visual(self):
        self.__type = CaptchaType.VISUAL

        self.setFixedSize(CAPTCHA_POPUP_SIZE_VISUAL)
        self.parent().setFixedSize(CAPTCHA_POPUP_SIZE_VISUAL)
        self.submit.move(SUBMIT_BUTTON_POSITION_VISUAL)
        self.__button_visual.move(self.__button_visual.pos().x(), SUBMIT_BUTTON_POSITION_VISUAL.y())
        self.__button_refresh.move(self.__button_refresh.pos().x(), SUBMIT_BUTTON_POSITION_VISUAL.y())

        self.__button_play.setVisible(False)
        self.__textfield_audio.setVisible(False)
        self.__button_visual.setVisible(False)
        self.__button_audio.setVisible(True)
        self.__load_next_task()

    def __handle_audio(self):
        self.__type = CaptchaType.AUDIO

        self.setFixedSize(CAPTCHA_POPUP_SIZE_AUDIO)
        self.parent().setFixedSize(CAPTCHA_POPUP_SIZE_AUDIO)
        self.submit.move(SUBMIT_BUTTON_POSITION_AUDIO)
        self.__button_visual.move(self.__button_visual.pos().x(), SUBMIT_BUTTON_POSITION_AUDIO.y())
        self.__button_refresh.move(self.__button_refresh.pos().x(), SUBMIT_BUTTON_POSITION_AUDIO.y())

        for button in self.__buttons_image:
            button.setVisible(False)
        for button in self.__buttons_square:
            button.setVisible(False)

        self.__button_audio.setVisible(False)
        self.__button_visual.setVisible(True)
        self.__button_play.setVisible(True)
        self.__textfield_audio.clear()
        self.__textfield_audio.setVisible(True)

        self.__load_next_task()

    def __handle_play(self):
        mixer.music.play()

    def __validate_images(self):
        answer = []
        for button in self.__buttons_image:
            answer.append(button.isSelected())

        correct_answer = []
        for i in range(9):
            correct_answer.append(image_labels[str(self.__files[i])] == self.__task_category)

        if answer == correct_answer:
            self.parent().passed.emit()
            self.parent().close()
        else:
            self.parent().failed.emit()
            self.__load_next_task()

    def __validate_squares(self):
        answer = []
        row = []
        for button in self.__buttons_square:
            row.append(button.isSelected())
            if len(row) == 4:
                answer.append(row)
                row = []

        for label in square_labels:
            if int(label) == self.__files[0]:
                if answer == square_labels[label]:
                    self.parent().passed.emit()
                    self.parent().close()
                else:
                    self.parent().failed.emit()
                    self.__load_next_task()
                break

    def __validate_audio(self):
        for label in audio_labels:
            if int(label) == self.__files[0]:
                if self.__textfield_audio.text().lower() == audio_labels[label]:
                    self.parent().passed.emit()
                    self.parent().close()
                else:
                    self.parent().failed.emit()
                    self.__load_next_task()
                break

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
            self.__task_category = image_label_types[random.randint(0, len(image_label_types) - 2)]
            self.__files = self.__find_random_tasks('image')
            self.__load_images()
        elif self.__task == CaptchaTask.SQUARE:
            self.__files = self.__find_random_tasks('square')
            self.__load_squares()
        else:
            self.__files = self.__find_random_tasks('audio')
            self.__load_audio()

        self.update()

    def __find_random_tasks(self, folder: str) -> list:
        tasks = os.listdir(DIRECTORY + '/files/' + folder)
        if len(tasks) == 0:
            return [0]

        current_task = self.__files[0]
        if folder != 'image':
            while current_task == self.__files[0]:
                current_task = random.randint(1, len(tasks))
            return [current_task]

        new_tasks = []
        amount_correct = random.randint(3, 7)

        for i in range(amount_correct):
            current_task = self.__files[0]
            while current_task in self.__files or current_task in new_tasks or image_labels[str(current_task)] != self.__task_category:
                current_task = random.randint(1, len(tasks))
            new_tasks.append(current_task)

        for i in range(9 - amount_correct):
            current_task = self.__files[0]
            while current_task in self.__files or current_task in new_tasks or image_labels[str(current_task)] != 'none':
                current_task = random.randint(1, len(tasks))
            new_tasks.append(current_task)

        random.shuffle(new_tasks)
        return new_tasks

    def __load_images(self):

        for i in range(9):
            self.__buttons_image[i].setImage(QPixmap(DIRECTORY + '/files/image/{}.png'.format(self.__files[i])))
            self.__buttons_image[i].setSelected(False)
            self.__buttons_image[i].setVisible(True)

        for button in self.__buttons_square:
            button.setVisible(False)

    def __load_squares(self):

        image = QPixmap(DIRECTORY + '/files/square/{}.png'.format(self.__files[0]))

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
        mixer.music.load(DIRECTORY + '/files/audio/{}.mp3'.format(self.__files[0]))

    def __handle_focus(self):
        if not self.hasFocus() and not self.__textfield_audio.hasFocus():
            self.parent().aborted.emit()
            self.parent().close()

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setPen(Qt.PenStyle.NoPen)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(self.__primary_color)
        painter.drawRoundedRect(8, 8, 314, 95, self.__border_radius // 2, self.__border_radius // 2)
        painter.drawRect(8, 38, 314, 65)

        painter.setPen(QPen(self.__foreground_color, 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.SquareCap))
        painter.setFont(QFont('Arial', 12))
        font_metrics = QFontMetrics(painter.font())

        text1 = ''
        text2 = ''
        if self.__task == CaptchaTask.IMAGE:
            text1 = 'Select all images with'
            text2 = self.__task_category + 's'
        elif self.__task == CaptchaTask.SQUARE:
            text1 = 'Select all squares with'
            text2 = 'traffic lights'
        else:
            text1 = 'What word do you hear when'
            text2 = 'pressing play'

        height = font_metrics.tightBoundingRect(text1).height()
        painter.drawText(16, 40, text1)

        font_large = painter.font()
        font_large.setPointSize(15)
        font_large.setBold(True)
        painter.setFont(font_large)
        painter.drawText(16, 40 + height + int(height * 0.5), text2)

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.__handle_focus()
