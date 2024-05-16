from data import stores, households #imports two pandas dataframes for household data and store data
from geo_model import GeoModel
from mesa_geo.visualization import MapModule
from mesa.visualization import ModularServer
from household import Household

model_params = {
    "stores": stores,
    "households": households
}

def agent_portrayal(agent):
    """
    Defines color for agent visualization. If agent is a houshold, it is colored blue, if it is a store then red.

    Args:
        - agent: household or store to be colored red or blue.
    """
    portrayal = dict()
    if(type(agent)==Household):
        portrayal["color"] = "Blue"
    else:
        portrayal["color"] = "Red"
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