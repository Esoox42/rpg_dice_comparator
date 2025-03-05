import numpy as np
import matplotlib.pyplot as plt
import re

def parse_roll_expression(roll_expression: str):
    """Parse a dice roll expression like '2d4+3' into components."""
    match = re.fullmatch(r"(\d+)d(\d+)([+-]\d+)?", roll_expression.lower())
    if not match:
        raise ValueError("Invalid roll expression. Use format like '2d4+3'/'1d6+4'.")
    
    num_dice = int(match.group(1))
    num_sides = int(match.group(2))
    modifier = int(match.group(3)) if match.group(3) else 0
    
    return num_dice, num_sides, modifier

def dice_statistics(roll_expression: str):
    """
    Compute the expectation (mean) and variance of a dice roll expression.
    Example inputs: '1d8', '2d4+3'
    """
    num_dice, num_sides, modifier = parse_roll_expression(roll_expression)
    
    # Expectation (Mean) formula: E[X] = (n * (s + 1)) / 2 + modifier
    expectation = num_dice * (num_sides + 1) / 2 + modifier
    
    # Variance formula: Var(X) = n * (s^2 - 1) / 12 (modifiers do not affect variance)
    variance = num_dice * (num_sides**2 - 1) / 12
    
    return expectation, variance

#def plot_histogram(roll_expression: str, num_samples: int = 10000):
#    """Generate and display a histogram of the roll results."""
#    num_dice, num_sides, modifier = parse_roll_expression(roll_expression)
#    
#    rolls = [sum(np.random.randint(1, num_sides + 1, num_dice)) + modifier for _ in range(num_samples)]
#   
#   plt.hist(rolls, bins=range(min(rolls), max(rolls) + 2), edgecolor='black', alpha=0.75)
#   plt.xlabel("Roll Result")
#   plt.ylabel("Frequency")
#   plt.title(f"Histogram of {roll_expression} Rolls")
#   plt.grid(axis='y', linestyle='--', alpha=0.7)
#   plt.show()