from PyQt6.QtCore import QRect, QPoint
from PyQt6.QtGui import QColor, QPaintEvent, QMouseEvent
from PyQt6.QtTest import QTest
from pytestqt.qt_compat import qt_api
from src.pyqtcaptcha.captcha_icon_button import CaptchaIconButton


def test_initial_values(qtbot):
    """Test initial values after instantiating"""

    icon_button = CaptchaIconButton()
    qtbot.addWidget(icon_button)

    assert icon_button.getIcon() is None
    assert icon_button.getIconHover() is None
    assert not icon_button.isHovered()
    assert icon_button.getColor() == QColor()
    assert icon_button.getHoveredColor() == QColor()


def test_hover(qtbot):
    icon_button = CaptchaIconButton()
    qtbot.addWidget(icon_button)
    icon_button.show()

    # Simulate mouse entering the widget
    QTest.mouseMove(icon_button, icon_button.rect().center())
    QTest.qWait(250)
    assert icon_button.isHovered()

    # Simulate mouse leaving the widget
    QTest.mouseMove(icon_button, QPoint(10000, 10000))
    QTest.qWait(250)
    assert not icon_button.isHovered()
