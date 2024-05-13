import mesa
import mesa_geo
import pandas as pd
import geopandas
from shapely.geometry import Point
from constants import (
    CLOSERPROB,
    ERHCFARTHERPROB,
    ERHCMAX,
    ERLCFARTHERPROB,
    ERLCMAX,
    LRHCFARTHERPROB,
    LRHCMAX,
    LRLCFARTHERPROB,
    LRLCMAX,
    SEARCHRADIUS,
)

csv_stores_file_path = "data/marketdata.csv"
csv_households_file_path = "data/homedata.csv"

households = pd.read_csv(csv_households_file_path)
stores = pd.read_csv(csv_stores_file_path)


#number of steps
num_steps = 5
#intialize and run model
model = GeoModel(width, height, len(households), len(stores))
for i in range(num_steps):
    model.step()


class GeoModel(mesa.Model):
    def __init__(self):
        super().__init__()
        self.space = mesa_geo.GeoSpace()

         # Create agents
        for row,index in stores.iterrows():
            agent = Store(row[])
            self.schedule.add(agent)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))

        self.space.add_agents(agents)

"""Module containing SPM and CSPM food store classes."""

class Store(mesa_geo.GeoAgent):
    """Class for SPM or CSPM.

    Attributes
    ----------
        - store_id (int): unique id
        - category (string): SPM or CSPM
        - lat (float): latitude of agent
        - lon (float): longitude of agent
        - fsa (int): Food Store Audit (index indicating the percentage of 87 USDA TFP items available at the store)

    """

    def __init__(self: "Store", store_id: int, category: str, lat: float, lon: float, fsa: int) -> None:
        """Initialize food store."""
        super().__init__(self, store_id,model,Point(lat,long),"epsg:3857") # epsg:3857 is the mercator projection
        self.category = str(category)
        self.fsa = int(fsa)