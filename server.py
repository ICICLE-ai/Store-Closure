from data import stores, households #imports two pandas dataframes for household data and store data
from geo_model import GeoModel
from custom_map_visualization import MapModule
from mesa.visualization import ModularServer
from agent_visualization import agent_portrayal


model_params = {
    "stores": stores,
    "households": households
}

#Create Map visualization of Stores and households
map_vis = MapModule(agent_portrayal)

#Start server on port 8080
server = ModularServer(
    GeoModel,
    [map_vis],
    "Store Closure Agent-Based Model",
    model_params,
)
print("running")
server.launch(8080)