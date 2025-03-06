# Dice Statistics Comparison UI

This project provides a graphical user interface (GUI) to compare the statistics of different dice rolls. The application allows users to select the number of dice, the type of dice, and a modifier, and then displays the mean, variance, minimum, and maximum values of the roll. Additionally, it generates a histogram of the roll results.

## Features

- Select the number of dice to roll.
- Choose from different types of dice (d4, d6, d8, d10, d12, d20).
- Add a modifier to the roll.
- Display the mean, variance, minimum, and maximum values of the roll.
- Generate and display a histogram of the roll results.
- Compare two different dice rolls side by side.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Esoox42/rpg_dice_comparator.git
    cd rpg_dice_comparator
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Navigate to the [src](http://_vscodecontentref_/1) directory:
    ```sh
    cd src
    ```

2. Run the application:
    ```sh
    python main.py
    ```

3. The application window will open, allowing you to select the number of dice, the type of dice, and a modifier for two different dice rolls. The results will be displayed side by side for comparison.

## Directory Structure
dice_statistics_ui
├── src
│   ├── main.py            # Entry point for the application
│   ├── ui.py              # User interface logic
│   ├── dice_statistics.py # Dice statistics functionalities
│   ├── main_window.py     # Manage double UI instance
│   └── assets
│       ├── icons          # Dice icons
│       └── styles.css     # CSS styles for the UI
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation