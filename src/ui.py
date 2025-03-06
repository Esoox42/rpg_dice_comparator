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

        # Create a horizontal layout for advantage and disadvantage buttons
        adv_disadv_layout = QHBoxLayout()

        self.advantage_button = QPushButton("Roll with Advantage", self)
        self.advantage_button.setCheckable(True)
        self.advantage_button.clicked.connect(self.toggle_advantage)
        adv_disadv_layout.addWidget(self.advantage_button)

        self.disadvantage_button = QPushButton("Roll with Disadvantage", self)
        self.disadvantage_button.setCheckable(True)
        self.disadvantage_button.clicked.connect(self.toggle_disadvantage)
        adv_disadv_layout.addWidget(self.disadvantage_button)

        layout.addLayout(adv_disadv_layout)

        self.compare_button = QPushButton("Run simulation", self)
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
        self.advantage = False
        self.disadvantage = False

    def select_dice(self):
        sender = self.sender()
        if self.selected_button:
            self.selected_button.setStyleSheet("")  # Reset the style of the previously selected button
        self.selected_button = sender
        self.selected_button.setStyleSheet("background-color: lightblue;")  # Highlight the selected button
        self.selected_dice = self.dice_buttons[sender]

    def toggle_advantage(self):
        self.advantage = self.advantage_button.isChecked()
        self.disadvantage = False
        self.disadvantage_button.setChecked(False)
        if self.advantage:
            self.num_dice_spinbox.setValue(1)
            self.num_dice_spinbox.setEnabled(False)
        else:
            self.num_dice_spinbox.setEnabled(True)

    def toggle_disadvantage(self):
        self.disadvantage = self.disadvantage_button.isChecked()
        self.advantage = False
        self.advantage_button.setChecked(False)
        if self.disadvantage:
            self.num_dice_spinbox.setValue(1)
            self.num_dice_spinbox.setEnabled(False)
        else:
            self.num_dice_spinbox.setEnabled(True)

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
            mean, var, min_value, max_value = dice_statistics(roll_expression, advantage=self.advantage, disadvantage=self.disadvantage)
            self.output_text.clear()
            self.output_text.append(f"{roll_expression}{' with Advantage' if self.advantage else ''}{' with Disadvantage' if self.disadvantage else ''}: Mean = {mean}\n Variance = {var}\n Min = {min_value}\n Max = {max_value}")
            self.plot_histogram(roll_expression, advantage=self.advantage, disadvantage=self.disadvantage)
        except ValueError as e:
            self.output_text.clear()
            self.output_text.append(str(e))

    def plot_histogram(self, roll_expression: str, num_samples: int = 10000, advantage: bool = False, disadvantage: bool = False):
        """Generate and display a histogram of the roll results."""
        num_dice, num_sides, modifier = parse_roll_expression(roll_expression)
        
        if advantage:
            rolls = [max(np.random.randint(1, num_sides + 1), np.random.randint(1, num_sides + 1)) + modifier for _ in range(num_samples)]
        elif disadvantage:
            rolls = [min(np.random.randint(1, num_sides + 1), np.random.randint(1, num_sides + 1)) + modifier for _ in range(num_samples)]
        else:
            rolls = [sum(np.random.randint(1, num_sides + 1, num_dice)) + modifier for _ in range(num_samples)]
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.hist(rolls, bins=range(min(rolls), max(rolls) + 2), edgecolor='black', alpha=0.75)
        ax.set_xlabel("Roll Result")
        ax.set_ylabel("Frequency")
        ax.set_title(f"Histogram of {roll_expression} Rolls")
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        self.canvas.draw()