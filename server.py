from data import stores, households #imports two pandas dataframes for household data and store data
from geo_model import GeoModel
from abm_map import MapModule
from mesa.visualization import ModularServer
from household import Household
from store import Store

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
    if isinstance(agent,Household):
        portrayal["color"] = "Green"
        portrayal["description"] = ["HouseHold"]
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