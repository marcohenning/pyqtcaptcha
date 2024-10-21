from PyQt6.QtGui import QFocusEvent
from PyQt6.QtTest import QTest, QSignalSpy
from pytestqt.qt_compat import qt_api
from src.pyqtcaptcha.captcha_textfield import CaptchaTextField


def test_signal_emitted(qtbot):
    """Test focus_out signal being emitted when losing focus"""

    textfield = CaptchaTextField()
    qtbot.addWidget(textfield)

    spy = QSignalSpy(textfield.focus_out)
    assert len(spy) == 0

    # Simulate focus out event
    focus_event_out = QFocusEvent(QFocusEvent.Type.FocusOut)
    qt_api.QtWidgets.QApplication.instance().postEvent(textfield, focus_event_out)

    # Wait for signal to be emitted
    QTest.qWait(250)

    assert len(spy) == 1
