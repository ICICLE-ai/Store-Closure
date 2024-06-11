from data import stores, households #imports two pandas dataframes for household data and store data
from geo_model import GeoModel
from custom_map_visualization import MapModule
from mesa.visualization import ModularServer, Slider, ChartModule
from agent_visualization import agent_portrayal

from constants import (
    CLOSERPROB,
    ERHCFARTHERPROB,
    ERLCFARTHERPROB,
    LRHCFARTHERPROB,
    LRLCFARTHERPROB,
    ERHCTRIPSPERMONTH,
    ERLCTRIPSPERMONTH,
    LRHCTRIPSPERMONTH,
    LRLCTRIPSPERMONTH,
    ERHCCARRYPERCENT,
    ERLCCARRYPERCENT,
    LRHCCARRYPERCENT,
    LRLCCARRYPERCENT,
    SEARCHRADIUS
) #Constant variables from the constants.py file

model_params = {
    "stores": stores,
    "households": households,
    "CLOSERPROB": Slider("Probability that ANY agent goes to SPM if CLOSER than CSPM", CLOSERPROB, 0, 1, 0.01),
    "ERHCFARTHERPROB": Slider("Probability that ERHC agent goes to SPM if FARTHER than CSPM", ERHCFARTHERPROB, 0, 1, 0.01),
    "ERLCFARTHERPROB": Slider("Probability that ERLC agent goes to SPM if FARTHER than CSPM", ERLCFARTHERPROB, 0, 1, 0.01),
    "LRHCFARTHERPROB": Slider("Probability that LRHC agent goes to SPM if FARTHER than CSPM", LRHCFARTHERPROB, 0, 1, 0.01),
    "LRLCFARTHERPROB": Slider("Probability that LRLC agent goes to SPM if FARTHER than CSPM", LRLCFARTHERPROB, 0, 1, 0.01),
    "ERHCTRIPSPERMONTH": ERHCTRIPSPERMONTH,
    "ERLCTRIPSPERMONTH": ERLCTRIPSPERMONTH,
    "LRHCTRIPSPERMONTH": LRHCTRIPSPERMONTH,
    "LRLCTRIPSPERMONTH": LRLCTRIPSPERMONTH,
    "ERHCCARRYPERCENT": Slider("% of needed food that ERHC agent can carry home", ERHCCARRYPERCENT, 0, 1, 0.01),
    "ERLCCARRYPERCENT": Slider("% of needed food that ERLC agent can carry home", ERLCCARRYPERCENT, 0, 1, 0.01),
    "LRHCCARRYPERCENT": Slider("% of needed food that LRHC agent can carry home", LRHCCARRYPERCENT, 0, 1, 0.01),
    "LRLCCARRYPERCENT": Slider("% of needed food that LRLC agent can carry home", LRLCCARRYPERCENT, 0, 1, 0.01),
    "SEARCHRADIUS": SEARCHRADIUS
}

#Create Map visualization of Stores and households
map_vis = MapModule(agent_portrayal)

#Create chart to track mfai score
chart = ChartModule(
    [{"Label": "Average mfai", "Color": "Black"}],
    data_collector_name='datacollector'
)

#Start server on port 8080
server = ModularServer(
    GeoModel,
    [map_vis, chart],
    "Store Closure Agent-Based Model",
    model_params,
)
print("running")
server.launch(8080)