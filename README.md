# PyQt CAPTCHA

[![PyPI](https://img.shields.io/badge/pypi-v1.0.0-blue)](https://pypi.org/project/pyqtcaptcha)
[![Python](https://img.shields.io/badge/python-3.7+-blue)](https://github.com/marcohenning/pyqtcaptcha)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/marcohenning/pyqtcaptcha/blob/master/LICENSE)
[![Coverage](https://img.shields.io/badge/coverage-96%25-neon)](https://github.com/marcohenning/pyqtcaptcha)
[![Build](https://img.shields.io/badge/build-passing-neon)](https://github.com/marcohenning/pyqtcaptcha)

A modern and fully customizable CAPTCHA library for PyQt and PySide.

![main](https://github.com/user-attachments/assets/14af04a6-c953-4038-8121-0c7c91b92f9f)

## About

This library was made to bring CAPTCHA support to PyQt desktop applications. While the measure is mostly used in web applications due to their ease of automation, desktop applications can also be automated using programs like AutoHotkey. This CAPTCHA widget is fully customizable from everything related to visuals to the difficulty of the tasks and helps protect your application from spam and abuse through automation.

> All images have been sourced from public domain video material and are not subject to copyright restrictions.

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
captcha.setButtonForegroundColor(QColor(255, 0, 0))
```

* **Setting the button background color:**
```python
captcha.setButtonBackgroundColor(QColor(0, 255, 0))
```

* **Setting the button border color:**
```python
captcha.setButtonBorderColor(QColor(0, 0, 255))
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
captcha.setCheckboxColor(QColor(255, 255, 0))
```

* **Setting the checkbox width:**
```python
captcha.setCheckboxWidth(2)
```

> The checkbox width is also used for the width of the checkmark.

* **Setting the checkmark color:**
```python
captcha.setCheckmarkColor(QColor(0, 255, 255))
```

* **Setting the CAPTCHA popup foreground color:**
```python
captcha.setCaptchaForegroundColor(QColor(255, 255, 255))
```

> The foreground color (white by default) is used for text elements like the captcha prompt and submit button text as well as for the checkmark on selected images.

* **Setting the CAPTCHA popup background color:**
```python
captcha.setCaptchaBackgroundColor(QColor(255, 0, 255))
```

> The background color (white by default) is used for the background of the popup window.

* **Setting the CAPTCHA popup border color:**
```python
captcha.setCaptchaBorderColor(QColor(100, 255, 0))
```

* **Setting the CAPTCHA popup border radius:**
```python
captcha.setCaptchaBorderRadius(10)
```

* **Setting the CAPTCHA popup primary color:**
```python
captcha.setCaptchaPrimaryColor(QColor(0, 100, 255))
```

> The primary color (green by default) is used for the background of the captcha prompt and the background of the submit button.

* **Setting the CAPTCHA popup primary color (hovered):**
```python
captcha.setCaptchaPrimaryColorHovered(QColor(255, 100, 0))
```

> The primary hovered color (light-green by default) is used for the hovered background of the submit button.

* **Setting the CAPTCHA popup secondary color:**
```python
captcha.setCaptchaSecondaryColor(QColor(255, 255, 100))
```

> The secondary color (gray by default) is used for elements like the refresh button, visual button, audio button and play button.

* **Setting the CAPTCHA popup secondary color (hovered):**
```python
captcha.setCaptchaSecondaryColorHovered(QColor(0, 255, 50))
```

> The secondary hovered color (dark-gray by default) is used as the hover color for elements like the refresh button, visual button, audio button and play button.

* **Connecting methods to the provided events:**
```python
captcha.started.connect(self.some_function)
captcha.aborted.connect(self.some_function)
captcha.passed.connect(self.some_function)
captcha.failed.connect(self.some_function)
```

> The `started` signal is emitted every time the popup window gets opened, while the `aborted` signal is emitted every time the popup window gets closed without submitting an answer. When the submit button is pressed either the `passed` signal or the `failed` signal is emitted depending on the correctness of the answer.

**<br>All available methods:**

| Method                                                 | Description                                     |
|--------------------------------------------------------|-------------------------------------------------|
| `text(self)`                                           | Get the current button text                     |
| `setText(self, text: str)`                             | Set the button text                             |
| `getButtonForegroundColor(self)`                       | Get the current button foreground color         |
| `setButtonForegroundColor(self, color: QColor)`        | Set the button foreground color                 |
| `getButtonBackgroundColor(self)`                       | Get the current button background color         |
| `setButtonBackgroundColor(self, color: QColor)`        | Set the button background color                 |
| `getButtonBorderColor(self)`                           | Get the current button border color             |
| `setButtonBorderColor(self, color: QColor)`            | Set the button border color                     |
| `getButtonBorderWidth(self)`                           | Get the current button border width             |
| `setButtonBorderWidth(self, width: int)`               | Set the button border width                     |
| `getButtonBorderRadius(self)`                          | Get the current button border radius            |
| `setButtonBorderRadius(self, radius: int)`             | Set the button border radius                    |
| `getCheckboxColor(self)`                               | Get the current checkbox color                  |
| `setCheckboxColor(self, color: QColor)`                | Set the checkbox color                          |
| `getCheckboxWidth(self)`                               | Get the current checkbox width                  |
| `setCheckboxWidth(self, width: int)`                   | Set the checkbox width                          |
| `getCheckmarkColor(self)`                              | Get the current checkmark color                 |
| `setCheckmarkColor(self, color: QColor)`               | Set the checkmark color                         |
| `getCaptchaForegroundColor(self)`                      | Get the current captcha foreground color        |
| `setCaptchaForegroundColor(self, color: QColor)`       | Set the captcha foreground color                |
| `getCaptchaBackgroundColor(self)`                      | Get the current captcha background color        |
| `setCaptchaBackgroundColor(self, color: QColor)`       | Set the captcha background color                |
| `getCaptchaBorderColor(self)`                          | Get the current captcha border color            |
| `setCaptchaBorderColor(self, color: QColor)`           | Set the captcha border color                    |
| `getCaptchaBorderRadius(self)`                         | Get the current captcha border radius           |
| `setCaptchaBorderRadius(self, radius: int)`            | Set the captcha border radius                   |
| `getCaptchaPrimaryColor(self)`                         | Get the current captcha primary color           |
| `setCaptchaPrimaryColor(self, color: QColor)`          | Set the captcha primary color                   |
| `getCaptchaPrimaryColorHovered(self)`                  | Get the current captcha primary hovered color   |
| `setCaptchaPrimaryColorHovered(self, color: QColor)`   | Set the captcha primary hovered color           |
| `getCaptchaSecondaryColor(self)`                       | Get the current captcha secondary color         |
| `setCaptchaSecondaryColor(self, color: QColor)`        | Set the captcha secondary color                 |
| `getCaptchaSecondaryColorHovered(self)`                | Get the current captcha secondary hovered color |
| `setCaptchaSecondaryColorHovered(self, color: QColor)` | Set the captcha secondary hovered color         |
| `getDifficulty(self)`                                  | Get the current captcha difficulty              |
| `setDifficulty(self, difficulty: CaptchaDifficulty)`   | Set the captcha difficulty                      |
| `isPassed(self)`                                       | Has the captcha been completed?                 |
| `setPassed(self, passed: bool)`                        | Set the completion status of the captcha        |
| `reset(self)`                                          | Reset the captcha                               |
| `getPopup(self)`                                       | Get the current captcha popup                   |

## Showcase

https://github.com/user-attachments/assets/4a9245ea-3cee-40fd-9457-123a4dc0c58a

## License

This software is licensed under the [MIT license](https://github.com/marcohenning/pyqtcaptcha/blob/master/LICENSE).
