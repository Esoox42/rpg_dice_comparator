from PyQt5.QtWidgets import QSpinBox

class CustomSpinBox(QSpinBox):
    def textFromValue(self, value):
        if value > 0:
            return f'+{value}'
        return str(value)