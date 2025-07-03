from PyQt5.QtGui import QDoubleValidator, QValidator
from PyQt5.QtCore import QLocale

class CustomDoubleValidator(QDoubleValidator):
    def __init__(self, *args):
        super().__init__(*args)
        self.setLocale(QLocale(QLocale.English))

    def validate(self, string, pos):
        if 'e' in string.lower() or ',' in string:
            return (QValidator.Invalid, string, pos)
        return super().validate(string, pos)