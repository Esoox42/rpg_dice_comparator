from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QLineEdit, QPushButton, QTextEdit, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from dice_statistics import dice_statistics, parse_roll_expression
import numpy as np

class DiceStatisticsUI(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.dice_label = QLabel("Select Dice:")
        layout.addWidget(self.dice_label)

        self.dice_combo = QComboBox(self)
        dice_options = ['1d6', '1d8', '1d10', '1d12', '2d6', '2d8', '2d10', '2d12']
        self.dice_combo.addItems(dice_options)
        layout.addWidget(self.dice_combo)

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

    def compare_outputs(self):
        roll_expression = self.dice_combo.currentText()
        modifier = self.modifier_input.text()
        
        # Ensure the modifier is correctly formatted
        if modifier:
            if not modifier.startswith('+') and not modifier.startswith('-'):
                modifier = '+' + modifier
            roll_expression += modifier

        try:
            mean, var = dice_statistics(roll_expression)
            self.output_text.clear()
            self.output_text.append(f"{roll_expression}: Mean = {mean}, Variance = {var}")
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