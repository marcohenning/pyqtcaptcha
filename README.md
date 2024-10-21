# PyQt CAPTCHA

[![PyPI](https://img.shields.io/badge/pypi-v1.0.0-blue)](https://pypi.org/project/pyqtcaptcha)
[![Python](https://img.shields.io/badge/python-3.7+-blue)](https://github.com/marcohenning/pyqtcaptcha)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/marcohenning/pyqtcaptcha/blob/master/LICENSE)
[![Coverage](https://img.shields.io/badge/coverage-96%25-neon)](https://github.com/marcohenning/pyqtcaptcha)
[![Build](https://img.shields.io/badge/build-passing-neon)](https://github.com/marcohenning/pyqtcaptcha)

A modern and fully customizable CAPTCHA library for PyQt and PySide.

GIF...

## About

This library was made to bring CAPTCHA support to PyQt desktop applications. While the measure is mostly used in web applications due to their ease of automation, desktop applications can also be automated using programs like AutoHotkey. This CAPTCHA widget is fully customizable from everything related to visuals to the difficulty of the tasks and helps protect your application from spam and abuse through automation.

> **IMPORTANT:** <br>All images have been sourced from public domain video material and are not subject to copyright restrictions.

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

> **IMPORTANT:** <br>Styling of the widget must not be done by setting the stylesheet manually as the widget calculates the stylesheet itself and overrides it. Use the provided methods such as `setBackgroundColor()` instead.

* **Setting the difficulty:**
```python
captcha.setDifficulty(CaptchaDifficulty.HARD)
```

> On easy difficulty the user will have to complete image selection tasks (i.e. "Select all images containing cars"). On hard difficulty the user will have to select image squares (i.e. "Select all squares containing traffic lights"). Medium difficulty alternates between these two options randomly.

* **Checking the state:**
```python
captcha.isPassed()
```

* **Resetting the state:**
```python
captcha.reset()
```

* **Setting the button text:**
```python
captcha.setText('Text')
```

* **Setting the button foreground color:**
```python
captcha.setButtonForegroundColor(QColor('#FFF'))
```

* **Setting the button background color:**
```python
captcha.setButtonBackgroundColor(QColor('#FFF'))
```

* **Setting the button border color:**
```python
captcha.setButtonBorderColor(QColor('#FFF'))
```

* **Setting the button border width:**
```python
captcha.setButtonBorderWidth(1)
```

* **Setting the button border radius:**
```python
captcha.setButtonBorderRadius(5)
```

* **Setting the checkbox color:**
```python
captcha.setCheckboxColor(QColor('#FFF'))
```

* **Setting the checkbox width:**
```python
captcha.setCheckboxWidth(2)
```

> The checkbox width is also used for the width of the checkmark.

* **Setting the checkmark color:**
```python
captcha.setCheckmarkColor(QColor('#FFF'))
```

* **Setting the CAPTCHA popup foreground color:**
```python
captcha.setCaptchaForegroundColor(QColor('#FFF'))
```

> The foreground color (white by default) is used for text elements like the captcha prompt and submit button text as well as for the checkmark on selected images.

* **Setting the CAPTCHA popup background color:**
```python
captcha.setCaptchaBackgroundColor(QColor('#FFF'))
```

> The background color (white by default) is used for the background of the popup window.

* **Setting the CAPTCHA popup border color:**
```python
captcha.setCaptchaBorderColor(QColor('#FFF'))
```

* **Setting the CAPTCHA popup border radius:**
```python
captcha.setCaptchaBorderRadius(10)
```

* **Setting the CAPTCHA popup primary color:**
```python
captcha.setCaptchaPrimaryColor(QColor('#FFF'))
```

> The primary color (green by default) is used for the background of the captcha prompt and the background of the submit button.

* **Setting the CAPTCHA popup primary color (hovered):**
```python
captcha.setCaptchaPrimaryColorHovered(QColor('#FFF'))
```

> The primary hovered color (light-green by default) is used for the hovered background of the submit button.

* **Setting the CAPTCHA popup secondary color:**
```python
captcha.setCaptchaSecondaryColor(QColor('#FFF'))
```

> The secondary color (gray by default) is used for elements like the refresh button, visual button, audio button and play button.

* **Setting the CAPTCHA popup secondary color (hovered):**
```python
captcha.setCaptchaSecondaryColorHovered(QColor('#FFF'))
```

> The secondary hovered color (dark-gray by default) is used as the hover color for elements like the refresh button, visual button, audio button and play button.

* **Connecting methods to the provided events:**
```python
captcha.started.connect(self.some_function)
captcha.aborted.connect(self.some_function)
captcha.passed.connect(self.some_function)
captcha.failed.connect(self.some_function)
```

**<br>All available methods:**

Table...

## Showcase

Video...

## License

This software is licensed under the [MIT license](https://github.com/marcohenning/pyqtcaptcha/blob/master/LICENSE).
