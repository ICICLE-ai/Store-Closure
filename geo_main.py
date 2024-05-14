import mesa
import mesa_geo
import pandas as pd
import geopandas
from shapely.geometry import Point
import math
import random

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

class GeoModel(mesa.Model):

    #intialize all agents
    def __init__(self, stores: pd.DataFrame, households: pd.DataFrame):
        super().__init__()
        self.space = mesa_geo.GeoSpace()
        self.schedule = mesa.time.RandomActivation(self)

        # Create store agents and add to model
        for index,row in stores.iterrows():
            agent = Store(index+len(households), self, row["category"],row["latitude"],row["longitude"],row["FSA"])
            self.space.add_agents(agent)

        #Create household agents and add to model
        for index,row in households.iterrows():
            if row["category"] == "ERHC":
                agent = Household(index,self, "ERHC",row["latitude"],row["longitude"],0,ERHCMAX,ERHCFARTHERPROB,CLOSERPROB)
                self.schedule.add(agent)
                self.space.add_agents(agent)
            if row["category"] == "ERLC":
                agent = Household(index,self, "ERLC",row["latitude"],row["longitude"],0,ERLCMAX,ERLCFARTHERPROB,CLOSERPROB)
                self.schedule.add(agent)
                self.space.add_agents(agent)
            if row["category"] == "LRHC":
                agent = Household(index,self, "LRHC",row["latitude"],row["longitude"],0,LRHCMAX,LRHCFARTHERPROB,CLOSERPROB)
                self.schedule.add(agent)
                self.space.add_agents(agent)
            if row["category"] == "LRLC":
                agent = Household(index,self, "LRLC",row["latitude"],row["longitude"],0,LRLCMAX,LRLCFARTHERPROB,CLOSERPROB)
                self.schedule.add(agent)
                self.space.add_agents(agent)
  
    #run one step of model
    def step(self):
      self.schedule.step()

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

    def __init__(self: "Store",  model, store_id: int, category: str, lat: float, lon: float, fsa: int) -> None:
        """Initialize food store."""
        super().__init__(store_id,model,Point(lat,lon),"epsg:3857") # epsg:3857 is the mercator projection
        self.category = str(category)
        self.fsa = int(fsa)

class Household(mesa_geo.GeoAgent):
    """Base algorithm for each agents' behavior.

    Attributes
    ----------
        - house_id (int): Unique id.
        - household_type (string): ERHC, ERLC, LRHC, or LRLC.
        - lat (float): latitude of agent.
        - lon (float): longitude of agent.
        - mfai (int): food availability.

    """

    def __init__(self, house_id,model,  household_type, lat, lon, mfai, mfai_max: int, farther_prob: float, closer_prob: float):
        """Initialize agent's attributes."""
        super().__init__(house_id,model,Point(lat,lon),"epsg:2022")
        self.household_type = str(household_type)
        self.mfai = int(mfai)
        self.mfai_max = mfai_max
        self.farther_prob = farther_prob
        self.closer_prob = closer_prob

    def step(self: "Household") -> None:
        """Define agent behavior at each step.

        (1) Finds a list of neighboring supermarket agents (SPM/CSPM)
        (2) Chooses one from the list based on market distance and pre-defined agent probabilities
        (3) Calculates food availability based on chosen market.
        """
        #(1) find all stores within SEARCHRADIUS
        #TODO using geo-mesa
        closest_stores = model.space.get_neighbors_within_distance(self,SEARCHRADIUS)
        #init variables to easier names
        mfai_max = self.mfai_max
        farther_prob = self.farther_prob
        closer_prob = self.closer_prob
        """
        if(spm_choice[1]>cspm_choice[1]):
            #if farther, choose SPM with fartherprob
            chosen = random.choices([spm_choice[0],cspm_choice[0]], weights=[farther_prob,1-farther_prob])[0]
        else:
            #if closer, choose SPM with closerprob
            chosen = random.choices([spm_choice[0],cspm_choice[0]], weights=[closer_prob,1-closer_prob])[0]
        """
        #(3) calculate mfai like self.mfai = chosenMarket.fsa / mfai_max
        #food_from_visit =  int ((chosen.fsa / mfai_max)*100) #increment household's mfai by store's score
        #self.mfai += food_from_visit
        #TODO implement behavioral rules from slide 10 of ABM literature presentation: 0.8 for LC, 0.8 for LR, movement speeds?
            # foodFromVisit =  chosen.fsa * hasNoCar*0.8 *hasLowResource*0.8  #increment household's mfai by store's score
            # self.mfai += int ((foodFromVisit / mfai_max)*100)

#number of steps
num_steps = 5
#intialize model with stores and household data in a pandas df
model = GeoModel(stores,households)
#Run model for given number of iterations
for i in range(num_steps):
    model.step()