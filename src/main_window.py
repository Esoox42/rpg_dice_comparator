from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QDialog
from PyQt5.QtGui import QIcon
from ui import DiceStatisticsUI
from options_window import OptionsWindow
import os

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.num_samples = 10000  # Default number of samples
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.left_ui = DiceStatisticsUI()
        self.right_ui = DiceStatisticsUI()

        ui_layout = QHBoxLayout()
        ui_layout.addWidget(self.left_ui)
        ui_layout.addWidget(self.right_ui)

        layout.addLayout(ui_layout)

        # Create a horizontal layout for the options button
        options_layout = QHBoxLayout()
        options_layout.addStretch()  # Add a spacer to push the button to the right

        self.options_button = QPushButton("Options", self)
        self.options_button.setFixedWidth(100)  # Set a fixed width for the button
        self.options_button.clicked.connect(self.open_options)
        options_layout.addWidget(self.options_button)

        layout.addLayout(options_layout)

        self.setLayout(layout)
        self.setWindowTitle("Dice Statistics Comparison")

        # Set the window icon
        icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icons', 'd20.png')
        self.setWindowIcon(QIcon(icon_path))

    def open_options(self):
        options_window = OptionsWindow(self)
        options_window.samples_spinbox.setValue(self.num_samples)
        if options_window.exec_() == QDialog.Accepted:
            self.num_samples = options_window.samples_spinbox.value()
            self.left_ui.num_samples = self.num_samples
            self.right_ui.num_samples = self.num_samples