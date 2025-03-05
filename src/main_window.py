from PyQt5.QtWidgets import QWidget, QHBoxLayout
from ui import DiceStatisticsUI

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()

        self.left_ui = DiceStatisticsUI()
        self.right_ui = DiceStatisticsUI()

        layout.addWidget(self.left_ui)
        layout.addWidget(self.right_ui)

        self.setLayout(layout)
        self.setWindowTitle("Dice Statistics Comparison")