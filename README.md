# Dice Statistics UI

This project provides a user interface for selecting dice and modifiers to compute and compare dice statistics. It leverages existing functionality for calculating the mean and variance of dice rolls and visualizes the results through a user-friendly interface.

## Project Structure

```
dice_statistics_ui
├── src
│   ├── main.py          # Entry point for the application
│   ├── ui.py            # User interface logic
│   ├── dice_statistics.py # Dice statistics functionality
│   └── assets
│       └── styles.css   # CSS styles for the UI
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd dice_statistics_ui
   ```

2. **Install dependencies**:
   Create a virtual environment and install the required packages listed in `requirements.txt`:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

## Usage Guidelines

1. Run the application:
   ```
   python src/main.py
   ```

2. Use the user interface to:
   - Select the type of dice (e.g.: 1d6, 2d20).
   - Input any modifiers (e.g.: +3, -1).
   - Compare the outputs based on your selections.

## Application Functionality

- The application allows users to easily select different dice configurations and modifiers.
- It computes the mean and variance of the selected dice rolls.
- Users can visualize the results through histograms generated from the roll statistics.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.