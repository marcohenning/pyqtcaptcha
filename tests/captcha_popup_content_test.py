from PyQt6.QtCore import QPoint, QRect
from PyQt6.QtGui import QColor, QPaintEvent
from PyQt6.QtTest import QTest, QSignalSpy
from pytestqt.qt_compat import qt_api
from src.pyqtcaptcha.captcha_popup import CaptchaPopup
from src.pyqtcaptcha.captcha_popup_content import CaptchaPopupContent
from src.pyqtcaptcha.captcha_enums import *
from src.pyqtcaptcha.audio_labels import audio_labels
from src.pyqtcaptcha.square_labels import square_labels
from src.pyqtcaptcha.image_labels import image_labels
from src.pyqtcaptcha.constants import *


def test_initial_values(qtbot):
    """Test initial values after instantiating"""

    color = QColor(0, 0, 0)
    content = CaptchaPopupContent(CaptchaDifficulty.HARD, 0, color, color, color, color, color, color, color)
    qtbot.addWidget(content)

    assert content.getTask() == CaptchaTask.SQUARE
    assert content.getDifficulty() == CaptchaDifficulty.HARD
    assert content.getBorderRadius() == 0
    assert content.getForegroundColor() == color
    assert content.getBackgroundColor() == color
    assert content.getBorderColor() == color
    assert content.getPrimaryColor() == color
    assert content.getPrimaryColorHovered() == color
    assert content.getSecondaryColor() == color
    assert content.getSecondaryColorHovered() == color


def test_set_files(qtbot):
    """Test setting the files"""

    color = QColor(0, 0, 0)
    content = CaptchaPopupContent(CaptchaDifficulty.HARD, 0, color, color, color, color, color, color, color)
    qtbot.addWidget(content)

    files = [1, 2, 3]
    content.setFiles(files)

    assert content.getFiles() == files


def test_set_textfield_content(qtbot):
    """Test setting the audio textfield content"""

    color = QColor(0, 0, 0)
    content = CaptchaPopupContent(CaptchaDifficulty.HARD, 0, color, color, color, color, color, color, color)
    qtbot.addWidget(content)

    text = 'test'
    content.setTextfieldContent(text)

    assert content.getTextfieldContent() == text


def test_set_image_button_states(qtbot):
    """Test setting the image button states"""

    color = QColor(0, 0, 0)
    content = CaptchaPopupContent(CaptchaDifficulty.HARD, 0, color, color, color, color, color, color, color)
    qtbot.addWidget(content)

    states = [False, False, False, False, False, False, False, False, False]
    content.setImageButtonStates(states)

    assert content.getImageButtonStates() == states


def test_set_square_button_states(qtbot):
    """Test setting the square button states"""

    color = QColor(0, 0, 0)
    content = CaptchaPopupContent(CaptchaDifficulty.HARD, 0, color, color, color, color, color, color, color)
    qtbot.addWidget(content)

    states = [[False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False]]
    content.setSquareButtonStates(states)

    assert content.getSquareButtonStates() == states


def test_set_task_category(qtbot):
    """Test setting the task category for the image task"""

    color = QColor(0, 0, 0)
    content = CaptchaPopupContent(CaptchaDifficulty.HARD, 0, color, color, color, color, color, color, color)
    qtbot.addWidget(content)

    category = 'car'
    content.setTaskCategory(category)
    assert content.getTaskCategory() == category

    content.setTaskCategory('none')
    assert content.getTaskCategory() == category


def test_switch_visual_audio(qtbot):
    """Test switching between visual and audio challenges"""

    position = QPoint(0, 0)
    color = QColor(0, 0, 0)

    content = CaptchaPopupContent(CaptchaDifficulty.HARD, 0, color, color, color, color, color, color, color)
    captcha_popup = CaptchaPopup(content, position)
    qtbot.addWidget(content)

    assert content.getType() == CaptchaType.VISUAL
    assert content.size() == CAPTCHA_POPUP_SIZE_VISUAL

    content.handle_audio()
    assert content.getType() == CaptchaType.AUDIO
    assert content.size() == CAPTCHA_POPUP_SIZE_AUDIO

    content.handle_visual()
    assert content.getType() == CaptchaType.VISUAL
    assert content.size() == CAPTCHA_POPUP_SIZE_VISUAL


def test_load_next_task(qtbot):
    """Test loading the next task"""

    position = QPoint(0, 0)
    color = QColor(0, 0, 0)

    content = CaptchaPopupContent(CaptchaDifficulty.HARD, 0, color, color, color, color, color, color, color)
    captcha_popup = CaptchaPopup(content, position)
    qtbot.addWidget(content)

    content.handle_visual()
    assert len(content.getFiles()) == 1

    content.handle_audio()
    assert len(content.getFiles()) == 1

    content = CaptchaPopupContent(CaptchaDifficulty.EASY, 0, color, color, color, color, color, color, color)
    captcha_popup = CaptchaPopup(content, position)
    qtbot.addWidget(content)

    content.handle_visual()
    assert len(content.getFiles()) == 9

    content.handle_audio()
    assert len(content.getFiles()) == 1


def test_submit_image_correct(qtbot):
    """Test submitting a correct answer for the image task"""

    position = QPoint(0, 0)
    color = QColor(0, 0, 0)

    content = CaptchaPopupContent(CaptchaDifficulty.EASY, 0, color, color, color, color, color, color, color)
    captcha_popup = CaptchaPopup(content, position)
    qtbot.addWidget(content)

    spy_passed = QSignalSpy(captcha_popup.passed)
    spy_failed = QSignalSpy(captcha_popup.failed)

    files = [1, 2, 3, 4, 5, 6, 7, 8, 201]
    category = 'car'
    content.setFiles(files)
    content.setTaskCategory(category)

    correct_answer = []
    for i in range(9):
        correct_answer.append(image_labels[str(files[i])] == category)

    content.setImageButtonStates(correct_answer)
    content.handle_submit()

    # Wait for the signals to be emitted
    QTest.qWait(250)

    assert len(spy_passed) == 1
    assert len(spy_failed) == 0


def test_submit_image_incorrect(qtbot):
    """Test submitting an incorrect answer for the image task"""

    position = QPoint(0, 0)
    color = QColor(0, 0, 0)

    content = CaptchaPopupContent(CaptchaDifficulty.EASY, 0, color, color, color, color, color, color, color)
    captcha_popup = CaptchaPopup(content, position)
    qtbot.addWidget(content)

    spy_passed = QSignalSpy(captcha_popup.passed)
    spy_failed = QSignalSpy(captcha_popup.failed)

    files = [1, 2, 3, 4, 5, 6, 7, 8, 201]
    category = 'car'
    content.setFiles(files)
    content.setTaskCategory(category)

    incorrect_answer = [False, False, False, False, False, False, False, False, False]
    content.setImageButtonStates(incorrect_answer)
    content.handle_submit()

    # Wait for the signals to be emitted
    QTest.qWait(250)

    assert len(spy_passed) == 0
    assert len(spy_failed) == 1


def test_submit_square_correct(qtbot):
    """Test submitting a correct answer for the square task"""

    position = QPoint(0, 0)
    color = QColor(0, 0, 0)

    content = CaptchaPopupContent(CaptchaDifficulty.HARD, 0, color, color, color, color, color, color, color)
    captcha_popup = CaptchaPopup(content, position)
    qtbot.addWidget(content)

    spy_passed = QSignalSpy(captcha_popup.passed)
    spy_failed = QSignalSpy(captcha_popup.failed)

    content.setFiles([1])
    correct_answer = square_labels[str(content.getFiles()[0])]
    content.setSquareButtonStates(correct_answer)
    content.handle_submit()

    # Wait for the signals to be emitted
    QTest.qWait(250)

    assert len(spy_passed) == 1
    assert len(spy_failed) == 0


def test_submit_square_incorrect(qtbot):
    """Test submitting an incorrect answer for the square task"""

    position = QPoint(0, 0)
    color = QColor(0, 0, 0)

    content = CaptchaPopupContent(CaptchaDifficulty.HARD, 0, color, color, color, color, color, color, color)
    captcha_popup = CaptchaPopup(content, position)
    qtbot.addWidget(content)

    spy_passed = QSignalSpy(captcha_popup.passed)
    spy_failed = QSignalSpy(captcha_popup.failed)

    content.setFiles([1])
    incorrect_answer = [[False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False]]
    content.setSquareButtonStates(incorrect_answer)
    content.handle_submit()

    # Wait for the signals to be emitted
    QTest.qWait(250)

    assert len(spy_passed) == 0
    assert len(spy_failed) == 1


def test_submit_audio_correct(qtbot):
    """Test submitting a correct answer for the audio task"""

    position = QPoint(0, 0)
    color = QColor(0, 0, 0)

    content = CaptchaPopupContent(CaptchaDifficulty.HARD, 0, color, color, color, color, color, color, color)
    captcha_popup = CaptchaPopup(content, position)
    qtbot.addWidget(content)

    content.handle_audio()

    spy_passed = QSignalSpy(captcha_popup.passed)
    spy_failed = QSignalSpy(captcha_popup.failed)

    correct_answer = audio_labels[str(content.getFiles()[0])]
    content.setTextfieldContent(correct_answer)
    content.handle_submit()

    # Wait for the signals to be emitted
    QTest.qWait(250)

    assert len(spy_passed) == 1
    assert len(spy_failed) == 0


def test_submit_audio_incorrect(qtbot):
    """Test submitting an incorrect answer for the audio task"""

    position = QPoint(0, 0)
    color = QColor(0, 0, 0)

    content = CaptchaPopupContent(CaptchaDifficulty.HARD, 0, color, color, color, color, color, color, color)
    captcha_popup = CaptchaPopup(content, position)
    qtbot.addWidget(content)

    content.handle_audio()

    spy_passed = QSignalSpy(captcha_popup.passed)
    spy_failed = QSignalSpy(captcha_popup.failed)

    content.setTextfieldContent('')
    content.handle_submit()

    # Wait for the signals to be emitted
    QTest.qWait(250)

    assert len(spy_passed) == 0
    assert len(spy_failed) == 1


def test_paint_event(qtbot):
    """Test the paint event"""

    color = QColor(0, 0, 0)
    color_to_test = QColor(255, 0, 0)

    content = CaptchaPopupContent(CaptchaDifficulty.HARD, 0, color, color, color, color_to_test, color, color, color)
    qtbot.addWidget(content)

    # Simulate paint event and wait for event to be handled
    paint_event = QPaintEvent(QRect(0, 0, 0, 0))
    qt_api.QtWidgets.QApplication.instance().postEvent(content, paint_event)
    QTest.qWait(250)

    assert content.grab().toImage().pixel(200, 50) == color_to_test
