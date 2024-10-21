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
        difficulty: CaptchaDifficulty,
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
        """Create a new CaptchaPopupContent instance.
        The captcha content is used to display the captcha popup including tasks etc.

        :param difficulty: difficulty
        :param border_radius: border radius
        :param foreground_color: foreground color
        :param background_color: background color
        :param border_color: border color
        :param primary_color: primary color
        :param primary_color_hover: hovered primary color
        :param secondary_color: secondary color
        :param secondary_color_hover: hovered secondary color
        :param parent: the parent widget
        """

        super(CaptchaPopupContent, self).__init__(parent)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(CAPTCHA_POPUP_SIZE_VISUAL)

        self.__type = CaptchaType.VISUAL
        self.__task = CaptchaTask.IMAGE
        self.__difficulty = difficulty
        self.__files = [1]
        self.__task_category = image_label_types[0]

        # Styling settings
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

        self.submit.setStyleSheet(
            'QPushButton {color: %s; background: %s; border: none; border-radius: %spx;}'
            'QPushButton::hover {color: %s; background: %s; border: none; border-radius: %spx;}'
            % (self.__foreground_color.name(),
               self.__primary_color.name(),
               self.__border_radius // 2,
               self.__foreground_color.name(),
               self.__primary_color_hover.name(),
               self.__border_radius // 2)
        )

        self.submit.setFixedSize(SUBMIT_BUTTON_SIZE)
        self.submit.move(SUBMIT_BUTTON_POSITION_VISUAL)
        self.submit.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.submit.clicked.connect(self.handle_submit)

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
        self.__button_visual.clicked.connect(self.handle_visual)

        self.__button_audio = CaptchaIconButton(self)
        self.__button_audio.move(44, SUBMIT_BUTTON_POSITION_VISUAL.y())
        self.__button_audio.setColor(self.__secondary_color)
        self.__button_audio.setHoveredColor(self.__secondary_color_hover)
        self.__button_audio.setIcon(QImage(DIRECTORY + '/files/icons/headphones.png'))
        self.__button_audio.clicked.connect(self.handle_audio)

        self.__button_play = QPushButton(self)
        self.__button_play.setText('PLAY')

        self.__button_play.setStyleSheet(
            'QPushButton {color: %s; background: %s; border: none; border-radius: %spx;}'
            'QPushButton::hover {color: %s; background: %s; border: none; border-radius: %spx;}'
            % (self.__foreground_color.name(),
               self.__secondary_color.name(),
               self.__border_radius // 2,
               self.__foreground_color.name(),
               self.__secondary_color_hover.name(),
               self.__border_radius // 2)
        )

        self.__button_play.setFixedSize(314, 60)
        self.__button_play.move(IMAGE_COLUMN_1, IMAGE_ROW_1)
        self.__button_play.setFont(font)
        self.__button_play.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.__button_play.setVisible(False)
        self.__button_play.clicked.connect(self.__handle_play)

        self.__textfield_audio = CaptchaTextField(self)
        self.__textfield_audio.setPlaceholderText('What word did you hear?')

        self.__textfield_audio.setStyleSheet(
            'color: %s; background: %s; border: 1px solid %s; border-radius: %spx; padding: 0 10 0 10px;'
            % (self.__secondary_color.name(),
               self.__background_color.name(),
               self.__secondary_color.name(),
               self.__border_radius // 2)
        )

        self.__textfield_audio.setFixedSize(314, 45)
        self.__textfield_audio.move(IMAGE_COLUMN_1, IMAGE_ROW_1 + 67)
        font.setBold(False)
        self.__textfield_audio.setFont(font)
        self.__textfield_audio.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.__textfield_audio.setVisible(False)
        self.__textfield_audio.focus_out.connect(self.__handle_focus)

        # Lists storing the buttons for selectable images and squares
        self.__buttons_image = []
        self.__buttons_square = []

        # Buttons for selectable images
        self.__button_image_1 = CaptchaImageButton(self.__foreground_color, self.__primary_color, self)
        self.__button_image_1.move(IMAGE_COLUMN_1, IMAGE_ROW_1)
        self.__buttons_image.append(self.__button_image_1)

        self.__button_image_2 = CaptchaImageButton(self.__foreground_color, self.__primary_color, self)
        self.__button_image_2.move(IMAGE_COLUMN_2, IMAGE_ROW_1)
        self.__buttons_image.append(self.__button_image_2)

        self.__button_image_3 = CaptchaImageButton(self.__foreground_color, self.__primary_color, self)
        self.__button_image_3.move(IMAGE_COLUMN_3, IMAGE_ROW_1)
        self.__buttons_image.append(self.__button_image_3)

        self.__button_image_4 = CaptchaImageButton(self.__foreground_color, self.__primary_color, self)
        self.__button_image_4.move(IMAGE_COLUMN_1, IMAGE_ROW_2)
        self.__buttons_image.append(self.__button_image_4)

        self.__button_image_5 = CaptchaImageButton(self.__foreground_color, self.__primary_color, self)
        self.__button_image_5.move(IMAGE_COLUMN_2, IMAGE_ROW_2)
        self.__buttons_image.append(self.__button_image_5)

        self.__button_image_6 = CaptchaImageButton(self.__foreground_color, self.__primary_color, self)
        self.__button_image_6.move(IMAGE_COLUMN_3, IMAGE_ROW_2)
        self.__buttons_image.append(self.__button_image_6)

        self.__button_image_7 = CaptchaImageButton(self.__foreground_color, self.__primary_color, self)
        self.__button_image_7.move(IMAGE_COLUMN_1, IMAGE_ROW_3)
        self.__buttons_image.append(self.__button_image_7)

        self.__button_image_8 = CaptchaImageButton(self.__foreground_color, self.__primary_color, self)
        self.__button_image_8.move(IMAGE_COLUMN_2, IMAGE_ROW_3)
        self.__buttons_image.append(self.__button_image_8)

        self.__button_image_9 = CaptchaImageButton(self.__foreground_color, self.__primary_color, self)
        self.__button_image_9.move(IMAGE_COLUMN_3, IMAGE_ROW_3)
        self.__buttons_image.append(self.__button_image_9)

        # Buttons for selectable squares
        self.__button_square_1 = CaptchaImageButton(self.__foreground_color, self.__primary_color, self)
        self.__button_square_1.move(SQUARE_COLUMN_1, SQUARE_ROW_1)
        self.__buttons_square.append(self.__button_square_1)

        self.__button_square_2 = CaptchaImageButton(self.__foreground_color, self.__primary_color, self)
        self.__button_square_2.move(SQUARE_COLUMN_2, SQUARE_ROW_1)
        self.__buttons_square.append(self.__button_square_2)

        self.__button_square_3 = CaptchaImageButton(self.__foreground_color, self.__primary_color, self)
        self.__button_square_3.move(SQUARE_COLUMN_3, SQUARE_ROW_1)
        self.__buttons_square.append(self.__button_square_3)

        self.__button_square_4 = CaptchaImageButton(self.__foreground_color, self.__primary_color, self)
        self.__button_square_4.move(SQUARE_COLUMN_4, SQUARE_ROW_1)
        self.__buttons_square.append(self.__button_square_4)

        self.__button_square_5 = CaptchaImageButton(self.__foreground_color, self.__primary_color, self)
        self.__button_square_5.move(SQUARE_COLUMN_1, SQUARE_ROW_2)
        self.__buttons_square.append(self.__button_square_5)

        self.__button_square_6 = CaptchaImageButton(self.__foreground_color, self.__primary_color, self)
        self.__button_square_6.move(SQUARE_COLUMN_2, SQUARE_ROW_2)
        self.__buttons_square.append(self.__button_square_6)

        self.__button_square_7 = CaptchaImageButton(self.__foreground_color, self.__primary_color, self)
        self.__button_square_7.move(SQUARE_COLUMN_3, SQUARE_ROW_2)
        self.__buttons_square.append(self.__button_square_7)

        self.__button_square_8 = CaptchaImageButton(self.__foreground_color, self.__primary_color, self)
        self.__button_square_8.move(SQUARE_COLUMN_4, SQUARE_ROW_2)
        self.__buttons_square.append(self.__button_square_8)

        self.__button_square_9 = CaptchaImageButton(self.__foreground_color, self.__primary_color, self)
        self.__button_square_9.move(SQUARE_COLUMN_1, SQUARE_ROW_3)
        self.__buttons_square.append(self.__button_square_9)

        self.__button_square_10 = CaptchaImageButton(self.__foreground_color, self.__primary_color, self)
        self.__button_square_10.move(SQUARE_COLUMN_2, SQUARE_ROW_3)
        self.__buttons_square.append(self.__button_square_10)

        self.__button_square_11 = CaptchaImageButton(self.__foreground_color, self.__primary_color, self)
        self.__button_square_11.move(SQUARE_COLUMN_3, SQUARE_ROW_3)
        self.__buttons_square.append(self.__button_square_11)

        self.__button_square_12 = CaptchaImageButton(self.__foreground_color, self.__primary_color, self)
        self.__button_square_12.move(SQUARE_COLUMN_4, SQUARE_ROW_3)
        self.__buttons_square.append(self.__button_square_12)

        self.__button_square_13 = CaptchaImageButton(self.__foreground_color, self.__primary_color, self)
        self.__button_square_13.move(SQUARE_COLUMN_1, SQUARE_ROW_4)
        self.__buttons_square.append(self.__button_square_13)

        self.__button_square_14 = CaptchaImageButton(self.__foreground_color, self.__primary_color, self)
        self.__button_square_14.move(SQUARE_COLUMN_2, SQUARE_ROW_4)
        self.__buttons_square.append(self.__button_square_14)

        self.__button_square_15 = CaptchaImageButton(self.__foreground_color, self.__primary_color, self)
        self.__button_square_15.move(SQUARE_COLUMN_3, SQUARE_ROW_4)
        self.__buttons_square.append(self.__button_square_15)

        self.__button_square_16 = CaptchaImageButton(self.__foreground_color, self.__primary_color, self)
        self.__button_square_16.move(SQUARE_COLUMN_4, SQUARE_ROW_4)
        self.__buttons_square.append(self.__button_square_16)

        for button in self.__buttons_image:
            button.setVisible(False)

        for button in self.__buttons_square:
            button.setVisible(False)

        self.load_next_task()

    def handle_submit(self):
        """Handle the submit button being pressed"""

        if self.__task == CaptchaTask.IMAGE:
            self.__validate_images()
        elif self.__task == CaptchaTask.SQUARE:
            self.__validate_squares()
        else:
            self.__validate_audio()

    def __handle_refresh(self):
        """Handle the refresh button being pressed"""

        self.load_next_task()

    def handle_visual(self):
        """Handle the visual button being pressed"""

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
        self.load_next_task()

    def handle_audio(self):
        """Handle the audio button being pressed"""

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

        self.load_next_task()

    def __handle_play(self):
        """Handle the play audio button being pressed"""

        mixer.music.play()

    def __validate_images(self):
        """Validate the user's submission for an image task"""

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
            self.load_next_task()

    def __validate_squares(self):
        """Validate the user's submission for a square task"""

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
                    self.load_next_task()
                break

    def __validate_audio(self):
        """Validate the user's submission for an audio task"""

        for label in audio_labels:
            if int(label) == self.__files[0]:
                if self.__textfield_audio.text().lower() == audio_labels[label]:
                    self.parent().passed.emit()
                    self.parent().close()
                else:
                    self.parent().failed.emit()
                    self.load_next_task()
                break

    def load_next_task(self):
        """Load the next task"""

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
        """Find a random task to choose as the next task"""

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
        """Handle loading the task's images onto the buttons"""

        for i in range(9):
            self.__buttons_image[i].setImage(QPixmap(DIRECTORY + '/files/image/{}.png'.format(self.__files[i])))
            self.__buttons_image[i].setSelected(False)
            self.__buttons_image[i].setVisible(True)

        for button in self.__buttons_square:
            button.setVisible(False)

    def __load_squares(self):
        """Handle loading the task's squares onto the buttons"""

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
        """Handle loading the audio"""

        mixer.music.load(DIRECTORY + '/files/audio/{}.mp3'.format(self.__files[0]))

    def __handle_focus(self):
        """Handle closing the popup and aborting when the user clicks anywhere outside the window"""

        if not self.hasFocus() and not self.__textfield_audio.hasFocus():
            self.parent().aborted.emit()
            self.parent().close()

    def paintEvent(self, event):
        """Handle the widget drawing

        :param event: the event sent by PyQt
        """

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
        """Handle the widget losing focus

        :param event: the event sent by PyQt
        """

        super().focusOutEvent(event)
        self.__handle_focus()

    def getType(self) -> CaptchaType:
        """Get the current captcha type

        :return: captcha type
        """

        return self.__type

    def getTask(self) -> CaptchaTask:
        """Get the current captcha task

        :return: captcha task
        """

        return self.__task

    def getDifficulty(self) -> CaptchaDifficulty:
        """Get the current captcha difficulty

        :return: captcha difficulty
        """

        return self.__difficulty

    def getForegroundColor(self) -> QColor:
        """Get the current foreground color

        :return: foreground color
        """

        return self.__foreground_color

    def getBackgroundColor(self) -> QColor:
        """Get the current background color

        :return: background color
        """

        return self.__background_color

    def getBorderColor(self) -> QColor:
        """Get the current border color

        :return: border color
        """

        return self.__border_color

    def getBorderRadius(self) -> int:
        """Get the current border radius

        :return: border radius
        """

        return self.__border_radius

    def getPrimaryColor(self) -> QColor:
        """Get the current primary color

        :return: primary color
        """

        return self.__primary_color

    def getPrimaryColorHovered(self) -> QColor:
        """Get the current hovered primary color

        :return: hovered primary color
        """

        return self.__primary_color_hover

    def getSecondaryColor(self) -> QColor:
        """Get the current secondary color

        :return: secondary color
        """

        return self.__secondary_color

    def getSecondaryColorHovered(self) -> QColor:
        """Get the current hovered secondary color

        :return: hovered secondary color
        """

        return self.__secondary_color_hover

    def getTextfieldContent(self) -> str:
        """Get the current textfield content

        :return: textfield content
        """

        return self.__textfield_audio.text()

    def setTextfieldContent(self, text: str) -> None:
        """Set the textfield content

        :param text: new textfield content
        """

        self.__textfield_audio.setText(text)

    def getFiles(self) -> list:
        """Get the current selected files

        :return: selected files
        """

        return self.__files

    def setFiles(self, files: list) -> None:
        """Set the selected files

        :param files: new selected files
        """

        self.__files = files

    def getImageButtonStates(self) -> list:
        """Get the current image button states (selected or not)

        :return: image button states
        """

        states = []
        for button in self.__buttons_image:
            states.append(button.isSelected())
        return states

    def setImageButtonStates(self, states: list) -> None:
        """Set the image button states

        :param states: new image button states
        """

        for i in range(len(self.__buttons_image)):
            self.__buttons_image[i].setSelected(states[i])

    def getSquareButtonStates(self) -> list:
        """Get the current square button states (selected or not)

        :return: square button states
        """

        state = []
        row = []
        for button in self.__buttons_square:
            row.append(button.isSelected())
            if len(row) == 4:
                state.append(row)
                row = []
        return state

    def setSquareButtonStates(self, states: list) -> None:
        """Set the square button states

        :param states: new square button states
        """

        count = 0
        for row in states:
            for state in row:
                self.__buttons_square[count].setSelected(state)
                count += 1

    def getTaskCategory(self) -> str:
        """Get the current task category (image labeling task)

        :return: task category
        """

        return self.__task_category

    def setTaskCategory(self, category: str) -> None:
        """Set the current task category (image labeling task)

        :param category: new task category
        """

        if category in image_label_types and category is not 'none':
            self.__task_category = category
