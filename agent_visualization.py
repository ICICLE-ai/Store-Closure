import matplotlib.pyplot as plt
import numpy as np
from household import Household
from store import Store

def get_color(value, cmap_name='RdYlGn', vmin=1, vmax=100):
    """
    helper function for number_to_color_word(). Assigns a color to a value on a red-yellow-green scale.

    Args:
        - value: value that is assigned a color based on the color scale
        - cmap_name: the color map that you want the value to be fitted to
        - vmin: min value of "value" arg
        - vmax: max value of "value" arg
    """
    norm = plt.Normalize(vmin, vmax)
    cmap = plt.get_cmap(cmap_name)
    rgba = cmap(norm(value))
    return rgba

def rgba_to_color_name(rgba):
    """
    helper function for number_to_color_word(). Assigns a name to a color on a red-yellow-green scale.

    Args:
        - rgba: the rgba value of the color that is to be parsed into a word
    """
    r, g, b, _ = rgba
    if r > 0.5 and g < 0.5:
        return "Red"
    elif r < 0.5 and g > 0.5:
        return "Green"
    elif r < 0.5 and g > 0.4 and g < 0.6:
        return "Light Green"
    elif r < 0.5 and g > 0.6:
        return "Yellow Green"
    else:
        return "Yellow"  # Simplified; adjust as needed for more accuracy

def number_to_color_word(value):
    """
    Assigns a name to a value on a red-yellow-green scale.

    Args:
        - value: the value that is to be parsed into a color word.
    """
    rgba = get_color(value)
    color_word = rgba_to_color_name(rgba)
    return color_word

def agent_portrayal(agent):
    """
    Defines color for agent visualization. If agent is a houshold, it is colored blue, if it is a store then red.

    Args:
        - agent: household or store to be colored red or blue.
    """
    portrayal = dict()
    if isinstance(agent,Household):
        portrayal["color"] = number_to_color_word(agent.mfai)
        portrayal["description"] = ["Household"]
    if isinstance(agent,Store):
        portrayal["color"] = "Blue"
        portrayal["description"] = ["Store"]
    return portrayal