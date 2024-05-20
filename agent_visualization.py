import matplotlib.pyplot as plt
import numpy as np
from household import Household
from store import Store

def number_to_color_word(value):
    """
    helper function for agent_portrayal. Assigns a name to a value on a red-yellow-green scale.

    Args:
        - value: the value that is to be parsed into hex color.
    """
    # Normalize value to a range of 0 to 1
    normalized = (value - 1) / 99
    
    # Calculate the red, green, and blue components
    if normalized < 0.5:
        # Interpolate between red (255, 0, 0) and yellow (255, 255, 0)
        red = 255
        green = int(255 * (normalized * 2))
        blue = 0
    else:
        # Interpolate between yellow (255, 255, 0) and green (0, 255, 0)
        red = int(255 * (2 - 2 * normalized))
        green = 255
        blue = 0
    
    gray = 128
    desaturation_factor = 0.25
    red = int(red * (1 - desaturation_factor) + gray * desaturation_factor)
    green = int(green * (1 - desaturation_factor) + gray * desaturation_factor)
    blue = int(blue * (1 - desaturation_factor) + gray * desaturation_factor)

    # Convert RGB to hexadecimal
    hex_color = f"#{red:02x}{green:02x}{blue:02x}"
    
    return hex_color

def agent_portrayal(agent):
    """
    Defines attributes for agent visualization. If agent is a houshold, it is colored blue, if it is a store then red.

    Args:
        - agent: household or store to be colored red or blue.
    """
    portrayal = dict()
    if isinstance(agent,Household):
        portrayal["color"] = number_to_color_word(agent.mfai)

        portrayal["description"] = ["Household","mfai score: " + str(agent.mfai)]
    if isinstance(agent,Store):
        portrayal["color"] = "Blue"
        portrayal["description"] = ["Store"]
    return portrayal