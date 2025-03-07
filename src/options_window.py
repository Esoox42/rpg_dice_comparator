from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QPushButton

class OptionsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Options")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.samples_label = QLabel("Number of Samples:")
        layout.addWidget(self.samples_label)

        self.samples_spinbox = QSpinBox(self)
        self.samples_spinbox.setRange(100, 1000000)  # Set a reasonable range for the number of samples
        self.samples_spinbox.setValue(10000)  # Default value
        layout.addWidget(self.samples_spinbox)

        self.apply_button = QPushButton("Apply", self)
        self.apply_button.clicked.connect(self.apply_changes)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)

    def apply_changes(self):
        self.accept()  # Close the dialog and indicate success