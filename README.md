# PyQt CAPTCHA

Shields...

A modern and fully customizable CAPTCHA library for PyQt and PySide.

GIF...

## About

This library was made to bring CAPTCHA support to PyQt desktop applications. While the measure is mostly used in web applications due to their ease of automation, desktop applications can also be automated using programs like AutoHotkey. The CAPTCHA is fully customizable from everything related to visuals to the difficulty of the tasks and helps protect your application from spam and abuse.

## Installation

```
pip install pyqtcaptcha
```

## Example

```python
from PyQt6.QtWidgets import QMainWindow
from pyqtcaptcha import Captcha, CaptchaDifficulty


class Window(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)

        self.captcha = Captcha(self)
        self.captcha.setDifficulty(CaptchaDifficulty.HARD)
        self.captcha.setFixedSize(130, 40)
```

## Documentation

## License

This software is licensed under the [MIT license](https://github.com/marcohenning/pyqtcaptcha/blob/master/LICENSE).
