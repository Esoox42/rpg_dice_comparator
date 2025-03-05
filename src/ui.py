from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QLineEdit, QPushButton, QTextEdit, QVBoxLayout
from dice_statistics import dice_statistics, plot_histogram

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
            plot_histogram(roll_expression)
        except ValueError as e:
            self.output_text.clear()
            self.output_text.append(str(e))