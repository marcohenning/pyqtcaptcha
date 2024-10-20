from qtpy.QtCore import Signal
from qtpy.QtWidgets import QWidget, QLineEdit


class CaptchaTextField(QLineEdit):

    # Signal to be emitted when losing focus
    focus_out = Signal()

    def __init__(self, parent: QWidget = None):
        """Create a new CaptchaTextField instance

        :param parent: the parent widget
        """

        super(CaptchaTextField, self).__init__(parent)

    def focusOutEvent(self, event) -> None:
        """Gets called every time the widget loses focus

        :param event: the event sent by PyQt
        """

        super().focusOutEvent(event)
        self.focus_out.emit()
