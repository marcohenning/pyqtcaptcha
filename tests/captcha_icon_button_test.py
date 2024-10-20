from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QColor
from PyQt6.QtTest import QTest
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
    """Test hovering over the widget"""

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
