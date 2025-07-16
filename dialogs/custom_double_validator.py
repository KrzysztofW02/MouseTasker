from PyQt5.QtGui import QDoubleValidator, QValidator
from PyQt5.QtCore import QLocale
from typing import Tuple

class CustomDoubleValidator(QDoubleValidator):
    """Double validator enforcing English locale and forbidding scientific notation or comma separators."""

    def __init__(self, *args) -> None:
        """Initialize with English locale for decimal point."""
        super().__init__(*args)
        self.setLocale(QLocale(QLocale.English))

    def validate(self, string: str, pos: int) -> Tuple[QValidator.State, str, int]:
        """Reject input containing 'e' or ','; otherwise defer to base implementation."""
        if 'e' in string.lower() or ',' in string:
            return QValidator.Invalid, string, pos
        return super().validate(string, pos)