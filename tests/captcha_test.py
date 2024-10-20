import math
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QColor, QPaintEvent
from PyQt6.QtTest import QTest
from pytestqt.qt_compat import qt_api
from src.pyqtcaptcha.captcha import Captcha
from src.pyqtcaptcha.captcha_enums import *
from src.pyqtcaptcha.constants import *


def test_initial_values(qtbot):
    """Test initial values after instantiating"""

    captcha = Captcha()
    qtbot.addWidget(captcha)

    assert captcha.text() == 'I\'m not a robot'
    assert captcha.size() == CAPTCHA_BUTTON_SIZE
    assert not captcha.isPassed()
    assert captcha.getPopup() is None
    assert captcha.getButtonForegroundColor() == QColor(0, 0, 0)
    assert captcha.getButtonBackgroundColor() == QColor(255, 255, 255)
    assert captcha.getButtonBorderColor() == QColor(125, 125, 125)
    assert captcha.getButtonBorderWidth() == 1
    assert captcha.getButtonBorderRadius() == 4
    assert captcha.getCheckboxColor() == QColor(125, 125, 125)
    assert captcha.getCheckboxWidth() == 2
    assert captcha.getCheckmarkColor() == CAPTCHA_BUTTON_CHECKMARK_COLOR

    assert captcha.getDifficulty() == CaptchaDifficulty.MEDIUM
    assert captcha.getCaptchaBorderRadius() == 10
    assert captcha.getCaptchaForegroundColor() == CAPTCHA_POPUP_FOREGROUND_COLOR
    assert captcha.getCaptchaBackgroundColor() == CAPTCHA_POPUP_BACKGROUND_COLOR
    assert captcha.getCaptchaBorderColor() == CAPTCHA_POPUP_BORDER_COLOR
    assert captcha.getCaptchaPrimaryColor() == CAPTCHA_POPUP_PRIMARY_COLOR
    assert captcha.getCaptchaPrimaryColorHovered() == CAPTCHA_POPUP_PRIMARY_COLOR_HOVER
    assert captcha.getCaptchaSecondaryColor() == CAPTCHA_POPUP_SECONDARY_COLOR
    assert captcha.getCaptchaSecondaryColorHovered() == CAPTCHA_POPUP_SECONDARY_COLOR_HOVER


def test_set_text(qtbot):
    """Test setting the button text"""

    captcha = Captcha()
    qtbot.addWidget(captcha)

    text = 'test'
    captcha.setText(text)
    assert captcha.text() == text


def test_set_button_foreground_color(qtbot):
    """Test setting the button foreground color"""

    captcha = Captcha()
    qtbot.addWidget(captcha)

    color = QColor(255, 0, 0)
    captcha.setButtonForegroundColor(color)
    assert captcha.getButtonForegroundColor() == color


def test_set_button_background_color(qtbot):
    """Test setting the button background color"""

    captcha = Captcha()
    qtbot.addWidget(captcha)

    color = QColor(255, 0, 0)
    captcha.setButtonBackgroundColor(color)
    assert captcha.getButtonBackgroundColor() == color


def test_set_button_border_color(qtbot):
    """Test setting the button border color"""

    captcha = Captcha()
    qtbot.addWidget(captcha)

    color = QColor(255, 0, 0)
    captcha.setButtonBorderColor(color)
    assert captcha.getButtonBorderColor() == color


def test_set_button_border_width(qtbot):
    """Test setting the button border width"""

    captcha = Captcha()
    qtbot.addWidget(captcha)

    captcha.setButtonBorderWidth(10)
    assert captcha.getButtonBorderWidth() == 10


def test_set_button_border_radius(qtbot):
    """Test setting the button border radius"""

    captcha = Captcha()
    qtbot.addWidget(captcha)

    captcha.setButtonBorderRadius(10)
    assert captcha.getButtonBorderRadius() == 10


def test_set_checkbox_color(qtbot):
    """Test setting the checkbox color"""

    captcha = Captcha()
    qtbot.addWidget(captcha)

    color = QColor(255, 0, 0)
    captcha.setCheckboxColor(color)
    assert captcha.getCheckboxColor() == color


def test_set_checkbox_width(qtbot):
    """Test setting the checkbox width"""

    captcha = Captcha()
    qtbot.addWidget(captcha)

    captcha.setCheckboxWidth(10)
    assert captcha.getCheckboxWidth() == 10


def test_set_checkmark_color(qtbot):
    """Test setting the checkmark color"""

    captcha = Captcha()
    qtbot.addWidget(captcha)

    color = QColor(255, 0, 0)
    captcha.setCheckmarkColor(color)
    assert captcha.getCheckmarkColor() == color


def test_set_captcha_foreground_color(qtbot):
    """Test setting the captcha foreground color"""

    captcha = Captcha()
    qtbot.addWidget(captcha)

    color = QColor(255, 0, 0)
    captcha.setCaptchaForegroundColor(color)
    assert captcha.getCaptchaForegroundColor() == color


def test_set_captcha_background_color(qtbot):
    """Test setting the captcha background color"""

    captcha = Captcha()
    qtbot.addWidget(captcha)

    color = QColor(255, 0, 0)
    captcha.setCaptchaBackgroundColor(color)
    assert captcha.getCaptchaBackgroundColor() == color


def test_set_captcha_border_color(qtbot):
    """Test setting the captcha border color"""

    captcha = Captcha()
    qtbot.addWidget(captcha)

    color = QColor(255, 0, 0)
    captcha.setCaptchaBorderColor(color)
    assert captcha.getCaptchaBorderColor() == color


def test_set_captcha_border_radius(qtbot):
    """Test setting the captcha border radius"""

    captcha = Captcha()
    qtbot.addWidget(captcha)

    captcha.setCaptchaBorderRadius(20)
    assert captcha.getCaptchaBorderRadius() == 20


def test_set_captcha_primary_color(qtbot):
    """Test setting the captcha primary color"""

    captcha = Captcha()
    qtbot.addWidget(captcha)

    color = QColor(255, 0, 0)
    captcha.setCaptchaPrimaryColor(color)
    assert captcha.getCaptchaPrimaryColor() == color


def test_set_captcha_primary_color_hovered(qtbot):
    """Test setting the captcha hovered primary color"""

    captcha = Captcha()
    qtbot.addWidget(captcha)

    color = QColor(255, 0, 0)
    captcha.setCaptchaPrimaryColorHovered(color)
    assert captcha.getCaptchaPrimaryColorHovered() == color


def test_set_captcha_secondary_color(qtbot):
    """Test setting the captcha secondary color"""

    captcha = Captcha()
    qtbot.addWidget(captcha)

    color = QColor(255, 0, 0)
    captcha.setCaptchaSecondaryColor(color)
    assert captcha.getCaptchaSecondaryColor() == color


def test_set_captcha_secondary_color_hovered(qtbot):
    """Test setting the captcha hovered secondary color"""

    captcha = Captcha()
    qtbot.addWidget(captcha)

    color = QColor(255, 0, 0)
    captcha.setCaptchaSecondaryColorHovered(color)
    assert captcha.getCaptchaSecondaryColorHovered() == color


def test_set_captcha_difficulty(qtbot):
    """Test setting the captcha difficulty"""

    captcha = Captcha()
    qtbot.addWidget(captcha)

    difficulty = CaptchaDifficulty.HARD
    captcha.setDifficulty(difficulty)
    assert captcha.getDifficulty() == difficulty


def test_set_passed(qtbot):
    """Test setting the passed flag"""

    captcha = Captcha()
    qtbot.addWidget(captcha)

    captcha.setPassed(True)
    assert captcha.isPassed()


def test_reset(qtbot):
    """Test resetting the captcha"""

    captcha = Captcha()
    qtbot.addWidget(captcha)

    captcha.setPassed(True)
    captcha.reset()
    assert not captcha.isPassed()


def test_press_captcha_button(qtbot):
    """Test pressing the captcha button"""

    captcha = Captcha()
    qtbot.addWidget(captcha)
    captcha.show()

    QTest.mouseMove(captcha, captcha.rect().center())
    QTest.qWait(250)
    QTest.mouseClick(captcha, Qt.MouseButton.LeftButton)

    assert captcha.getPopup() is not None


def test_paint_event(qtbot):
    """Test the paint event"""

    captcha = Captcha()
    captcha.setPassed(True)
    qtbot.addWidget(captcha)

    paint_event = QPaintEvent(QRect(0, 0, 0, 0))
    qt_api.QtWidgets.QApplication.instance().postEvent(captcha, paint_event)
    QTest.qWait(250)

    actual_height = captcha.height() - captcha.getButtonBorderWidth() * 2
    dimension = int(actual_height * 0.66)
    buffer = captcha.getButtonBorderWidth() + math.ceil((actual_height - dimension) / 2)
    x_start_1 = buffer + int(dimension * 0.1)
    y_start_1 = math.ceil(buffer + dimension / 2)

    assert captcha.grab().toImage().pixel(x_start_1, y_start_1) == CAPTCHA_BUTTON_CHECKMARK_COLOR
