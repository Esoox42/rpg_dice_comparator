from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QSpinBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from dice_statistics import dice_statistics, parse_roll_expression
import numpy as np
import os

class DiceStatisticsUI(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.dice_label = QLabel("Select Number of Dice:")
        layout.addWidget(self.dice_label)

        self.num_dice_spinbox = QSpinBox(self)
        self.num_dice_spinbox.setRange(1, 100)
        self.num_dice_spinbox.setValue(1)
        layout.addWidget(self.num_dice_spinbox)

        self.dice_label = QLabel("Select Dice:")
        layout.addWidget(self.dice_label)

        dice_layout = QHBoxLayout()
        self.dice_buttons = {}
        dice_options = ['d4', 'd6', 'd8', 'd10', 'd12', 'd20']
        for dice in dice_options:
            button_layout = QVBoxLayout()
            button = QPushButton()
            icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icons', f'{dice}.png')
            button.setIcon(QIcon(icon_path))
            button.setIconSize(button.sizeHint())
            button.clicked.connect(self.select_dice)
            button_layout.addWidget(button)

            label = QLabel(dice)
            label.setAlignment(Qt.AlignCenter)
            button_layout.addWidget(label)

            dice_layout.addLayout(button_layout)
            self.dice_buttons[button] = dice

        layout.addLayout(dice_layout)

        self.modifier_label = QLabel("Enter Modifier:")
        layout.addWidget(self.modifier_label)

        self.modifier_input = QLineEdit(self)
        self.modifier_input.setText("0")
        layout.addWidget(self.modifier_input)

        self.compare_button = QPushButton("Compare Outputs", self)
        self.compare_button.clicked.connect(self.compare_outputs)
        layout.addWidget(self.compare_button)

        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)
        self.setWindowTitle("Dice Statistics Comparison")

        self.selected_dice = None
        self.selected_button = None

    def select_dice(self):
        sender = self.sender()
        if self.selected_button:
            self.selected_button.setStyleSheet("")  # Reset the style of the previously selected button
        self.selected_button = sender
        self.selected_button.setStyleSheet("background-color: lightblue;")  # Highlight the selected button
        self.selected_dice = self.dice_buttons[sender]

    def compare_outputs(self):
        if not self.selected_dice:
            self.output_text.clear()
            self.output_text.append("Please select a dice.")
            return

        num_dice = self.num_dice_spinbox.value()
        roll_expression = f'{num_dice}{self.selected_dice}'
        modifier = self.modifier_input.text()
        
        # Ensure the modifier is correctly formatted
        if modifier:
            if not modifier.startswith('+') and not modifier.startswith('-'):
                modifier = '+' + modifier
            roll_expression += modifier

        try:
            mean, var, min_value, max_value = dice_statistics(roll_expression)
            self.output_text.clear()
            self.output_text.append(f"{roll_expression}: \nMean = {mean} \nVariance = {var} \nMin = {min_value} \nMax = {max_value}")
            self.plot_histogram(roll_expression)
        except ValueError as e:
            self.output_text.clear()
            self.output_text.append(str(e))

    def plot_histogram(self, roll_expression: str, num_samples: int = 10000):
        """Generate and display a histogram of the roll results."""
        num_dice, num_sides, modifier = parse_roll_expression(roll_expression)
        
        rolls = [sum(np.random.randint(1, num_sides + 1, num_dice)) + modifier for _ in range(num_samples)]
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.hist(rolls, bins=range(min(rolls), max(rolls) + 2), edgecolor='black', alpha=0.75)
        ax.set_xlabel("Roll Result")
        ax.set_ylabel("Frequency")
        ax.set_title(f"Histogram of {roll_expression} Rolls")
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        self.canvas.draw()