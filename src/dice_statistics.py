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

def dice_statistics(roll_expression: str, advantage: bool = False, disadvantage: bool = False):
    """
    Compute the expectation (mean), variance, minimum, and maximum of a dice roll expression.
    Example inputs: '1d8', '2d4+3'
    """
    num_dice, num_sides, modifier = parse_roll_expression(roll_expression)
    
    if advantage:
        if num_dice != 1:
            raise ValueError("Advantage roll can only be performed with 1 dice.")
        
        # Expectation (Mean) for advantage roll
        expectation = sum(k * ((k / num_sides)**2 - ((k - 1) / num_sides)**2) for k in range(1, num_sides + 1)) + modifier
        
        # Variance for advantage roll
        mean_square = sum((k**2) * ((k / num_sides)**2 - ((k - 1) / num_sides)**2) for k in range(1, num_sides + 1))
        variance = mean_square - expectation**2
    elif disadvantage:
        if num_dice != 1:
            raise ValueError("Disadvantage roll can only be performed with 1 dice.")
        
        # Expectation (Mean) for disadvantage roll
        expectation = sum(k * ((num_sides - k + 1) / num_sides)**2 - ((num_sides - k) / num_sides)**2 for k in range(1, num_sides + 1)) + modifier
        
        # Variance for disadvantage roll
        mean_square = sum((k**2) * ((num_sides - k + 1) / num_sides)**2 - ((num_sides - k) / num_sides)**2 for k in range(1, num_sides + 1))
        variance = mean_square - expectation**2
    else:
        # Expectation (Mean) formula: E[X] = (n * (s + 1)) / 2 + modifier
        expectation = num_dice * (num_sides + 1) / 2 + modifier
        
        # Variance formula: Var(X) = n * (s^2 - 1) / 12 (modifiers do not affect variance)
        variance = num_dice * (num_sides**2 - 1) / 12
    
    # Minimum and maximum values
    min_value = num_dice + modifier
    max_value = num_dice * num_sides + modifier
    
    return expectation, variance, min_value, max_value