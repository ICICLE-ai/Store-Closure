from household import Household
from store import Store

def number_to_color_word(value):
    return f"#{200:02x}{0:02x}{0:02x}"
    """
    helper function for agent_portrayal. Assigns a name to a value on a red-yellow-green scale.

    Args:
        - value: the value that is to be parsed into hex color.
    """
    #used to change how dark the color is
    top_range = 175

    # Normalize value to a range of 0 to 1
    normalized = (value - 50) / 50

    # If value is too low just return red
    if normalized < 0:
        red = top_range
        green = 0
        blue = 0
    # Calculate the red, green, and blue components
    elif normalized < 0.5:
        # Interpolate between red (255, 0, 0) and yellow (255, 255, 0)
        red = top_range
        green = int(top_range * (normalized * 2))
        blue = 0
    else:
        # Interpolate between yellow (255, 255, 0) and green (0, 255, 0)
        red = int(top_range * (2 - 2 * normalized))
        green = top_range
        blue = 0
    
    #gray = 128
    #desaturation_factor = 0.25
    #red = int(red * (1 - desaturation_factor) + gray * desaturation_factor)
    #green = int(green * (1 - desaturation_factor) + gray * desaturation_factor)
    #blue = int(blue * (1 - desaturation_factor) + gray * desaturation_factor)

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
        portrayal["color"] = "Red" #number_to_color_word(agent.income)

        portrayal["description"] = ["Household","income: " + str(agent.income)]
    if isinstance(agent,Store):
        portrayal["color"] = "Blue"
        portrayal["description"] = ["Category: " + str(agent.category),"FSA Score: " + str(agent.fsa)]
    return portrayal