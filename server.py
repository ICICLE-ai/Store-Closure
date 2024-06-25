from geo_model import GeoModel
from custom_map_visualization import MapModule
from mesa.visualization import ModularServer, Slider, ChartModule
from agent_visualization import agent_portrayal
import pandas as pd

stores = pd.read_csv("data/stores.csv")
households = pd.read_csv("data/households.csv")

model_params = {
    "stores": stores,
    "households": households,
}

#Create Map visualization of Stores and households
map_vis = MapModule(agent_portrayal)

"""
Create chart to track mfai score
chart = ChartModule(
    [{"Label": "Average mfai", "Color": "Black"}],
    data_collector_name='datacollector'
)
"""

#Start server on port 8080
server = ModularServer(
    GeoModel,
    [map_vis],
    "Store Closure Agent-Based Model",
    model_params,
)
print("running")
server.launch(8080)