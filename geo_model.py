from mesa import Model
from mesa.time import RandomActivation
from mesa_geo import GeoSpace
import pandas as pd
from store import Store
from household import Household

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

class GeoModel(Model):

    #intialize all agents
    def __init__(self, stores: pd.DataFrame, households: pd.DataFrame):
        super().__init__()
        self.space = GeoSpace(warn_crs_conversion=False)
        self.schedule = RandomActivation(self)

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