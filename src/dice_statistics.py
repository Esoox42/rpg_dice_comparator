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
        # E[max(X1,X2)] = Σk[(k/N)^2 - (k-1/N)^2] = Σk((2k-1)/N^2)
        expectation_without_mod = sum(k * ((k / num_sides)**2 - ((k - 1) / num_sides)**2) for k in range(1, num_sides + 1))
        expectation = expectation_without_mod + modifier
        
        # Variance for advantage roll
        # Var[max(X1,X2)] = Σk^2[(k/N)^2 - (k-1/N)^2] = Σk^2((2k-1)/N^2)
        mean_square = sum((k**2) * ((2*k - 1) / (num_sides)**2) for k in range(1, num_sides + 1))
        variance = mean_square - expectation_without_mod**2 # Modifiers do not affect variance
    elif disadvantage:
        if num_dice != 1:
            raise ValueError("Disadvantage roll can only be performed with 1 dice.")
        
        # Expectation (Mean) for disadvantage roll
        # E[max(X1,X2)] = Σk[(N-k+1/N)^2 - (N-k/N)^2] = Σk((2(N-k)+1/N^2) #doubt
        expectation_without_mod = sum(k *  (((num_sides - k + 1) / num_sides)**2 - ((num_sides - k) / num_sides)**2) for k in range(1, num_sides + 1))
        expectation = expectation_without_mod + modifier

        # Variance for disadvantage roll
        # Var[max(X1,X2)] = Σk^2[(N-k+1/N)^2 - (N-k/N)^2] = Σk^2((2(N-k)+1/N^2)
        mean_square = sum((k**2) * (((num_sides - k + 1) / num_sides)**2 - ((num_sides - k) / num_sides)**2) for k in range(1, num_sides + 1))
        variance = mean_square - expectation_without_mod**2 # Modifiers do not affect variance
    else:
        # Expectation (Mean) formula: E[X] = (n * (s + 1)) / 2 + modifier
        expectation = num_dice * (num_sides + 1) / 2 + modifier
        
        # Variance formula: Var(X) = n * (s^2 - 1) / 12 (modifiers do not affect variance)
        variance = num_dice * (num_sides**2 - 1) / 12
    
    # Minimum and maximum values
    min_value = num_dice + modifier
    max_value = num_dice * num_sides + modifier
    
    return expectation, variance, min_value, max_value