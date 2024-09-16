from qtpy.QtWidgets import QWidget, QPushButton


class Captcha(QPushButton):

    def __init__(self, parent: QWidget = None):
        super(Captcha, self).__init__(parent)
