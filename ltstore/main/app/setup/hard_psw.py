
import re


class PswException(Exception):
    def __init__(self, psw):
        self._psw = psw

    def __str__(self):
        return f"Ошибка при проверке пароля"


class ValidatePsw(PswException):
    def __init__(self, psw):
        self._psw = psw
        self._cond1 = re.compile(r'''[A-Z]''')
        self._cond2 = re.compile(r'[a-z]')
        self._cond3 = re.compile(r'[0-9]')

    def check_psw(self):
        return self._cond1.search(str(self._psw)) and self._cond2.search(str(self._psw)) and self._cond3.search(str(self._psw))
