from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QColor, QPaintEvent, QPixmap
from PyQt6.QtTest import QTest
from pytestqt.qt_compat import qt_api
from src.pyqtcaptcha.captcha_image_button import CaptchaImageButton


def test_initial_values(qtbot):
    """Test initial values after instantiating"""

    color = QColor(0, 0, 0)
    image_button = CaptchaImageButton(color, color)
    qtbot.addWidget(image_button)

    assert not image_button.isSelected()
    assert image_button.getImage() is None


def test_mouse_event(qtbot):
    color = QColor(0, 0, 0)
    image_button = CaptchaImageButton(color, color)
    image_button.setImage(QPixmap())
    qtbot.addWidget(image_button)
    image_button.show()

    assert not image_button.isSelected()

    QTest.mouseMove(image_button, image_button.rect().center())
    QTest.qWait(250)
    QTest.mousePress(image_button, Qt.MouseButton.LeftButton)
    QTest.qWait(250)

    paint_event = QPaintEvent(QRect(0, 0, 0, 0))
    qt_api.QtWidgets.QApplication.instance().postEvent(image_button, paint_event)
    QTest.qWait(250)

    assert image_button.isSelected()

    QTest.mousePress(image_button, Qt.MouseButton.LeftButton)
    QTest.qWait(250)

    paint_event = QPaintEvent(QRect(0, 0, 0, 0))
    qt_api.QtWidgets.QApplication.instance().postEvent(image_button, paint_event)
    QTest.qWait(250)

    assert not image_button.isSelected()
