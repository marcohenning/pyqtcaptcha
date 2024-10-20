from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QColor
from src.pyqtcaptcha.captcha_popup import CaptchaPopup
from src.pyqtcaptcha.captcha_popup_content import CaptchaPopupContent
from src.pyqtcaptcha.captcha_enums import *


def test_initial_values(qtbot):
    """Test initial values after instantiating"""

    position = QPoint(0, 0)
    color = QColor(0, 0, 0)
    content = CaptchaPopupContent(CaptchaDifficulty.HARD, 0, color, color, color, color, color, color, color)

    captcha_popup = CaptchaPopup(content, position)
    qtbot.addWidget(captcha_popup)

    assert captcha_popup.getContent() == content
    assert captcha_popup.getPosition() == position


def test_set_content(qtbot):
    """Test setting the content"""

    position = QPoint(0, 0)
    color = QColor(0, 0, 0)
    content = CaptchaPopupContent(CaptchaDifficulty.HARD, 0, color, color, color, color, color, color, color)

    captcha_popup = CaptchaPopup(content, position)
    qtbot.addWidget(captcha_popup)

    content_new = CaptchaPopupContent(CaptchaDifficulty.HARD, 0, color, color, color, color, color, color, color)
    captcha_popup.setContent(content_new)

    assert captcha_popup.getContent() == content_new


def test_set_position(qtbot):
    """Test setting the position"""

    position = QPoint(0, 0)
    color = QColor(0, 0, 0)
    content = CaptchaPopupContent(CaptchaDifficulty.HARD, 0, color, color, color, color, color, color, color)

    captcha_popup = CaptchaPopup(content, position)
    qtbot.addWidget(captcha_popup)

    position_new = QPoint(1, 1)
    captcha_popup.setPosition(position_new)

    assert captcha_popup.getPosition() == position_new
