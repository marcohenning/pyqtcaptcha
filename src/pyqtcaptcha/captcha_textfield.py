from qtpy.QtCore import Signal
from qtpy.QtWidgets import QWidget, QLineEdit


class CaptchaTextField(QLineEdit):

    focus_out = Signal()

    def __init__(self, parent: QWidget = None):
        super(CaptchaTextField, self).__init__(parent)

    def focusOutEvent(self, event) -> None:
        super().focusOutEvent(event)
        self.focus_out.emit()
