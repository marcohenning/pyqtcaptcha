from enum import Enum


class CaptchaType(Enum):
    VISUAL = 1
    AUDIO = 2

class CaptchaTask(Enum):
    IMAGE = 1
    SQUARE = 2
    AUDIO = 3

class CaptchaDifficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3
