from data import stores, households #imports two pandas dataframes for household data and store data
from geo_model import GeoModel
from abm_map import MapModule
from mesa.visualization import ModularServer
from household import Household
from store import Store
import matplotlib.pyplot as plt
import numpy as np

model_params = {
    "stores": stores,
    "households": households
}

# Function to interpolate colors
def get_color(value, cmap_name='RdYlGn', vmin=1, vmax=100):
    norm = plt.Normalize(vmin, vmax)
    cmap = plt.get_cmap(cmap_name)
    rgba = cmap(norm(value))
    return rgba

# Function to convert RGBA to a color name
def rgba_to_color_name(rgba):
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

# Main function to map number to color word
def number_to_color_word(value):
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

#Create Map visualization of Stores and households
map_vis = MapModule(agent_portrayal)

#Start server on port 8080
server = ModularServer(
    GeoModel,
    [map_vis],
    "ABM",
    model_params,
)
print("running")
server.launch(8080)