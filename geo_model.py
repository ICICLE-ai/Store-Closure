from mesa import Model #Base class for GeoModel
from mesa.time import RandomActivation #Used to specify that agents are run randomly within each step
from mesa_geo import GeoSpace #GeoSpace that houses agents
import pandas as pd
from store import Store # Store agent class
from household import Household # Household agent class

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
) #Constant variables from the constants.py file

class GeoModel(Model):

    """
    Geographical model that extends the mesa Model base class. This class initializes the store and household agents
    and then places the agents in the mesa_geo GeoSpace, which allows the Household agents to calculate distances between
    between themselves and Store Agents.
    """

    def __init__(self, stores: pd.DataFrame, households: pd.DataFrame):
        """
        Initialize the Model, intialize all agents and, add all agents to GeoSpace and Model.

        Args:
            - stores: dataframe containing data for store agents
            - households: dataframe containing data for household agents
        """
        super().__init__()
        self.space = GeoSpace(warn_crs_conversion=False) # Create new GeoSpace to contain agents
        self.schedule = RandomActivation(self) # Specify that agents should be activated randomly during each step

        # Initialize all store agents and add them to the GeoSpace
        for index,row in stores.iterrows():
            agent = Store(index+len(households), self, row["category"],row["latitude"],row["longitude"],row["FSA"],self.space.crs)
            self.space.add_agents(agent)

        # Initialize all household agents and add them to the scheduler and the Geospace
        for index,row in households.iterrows():
            if row["category"] == "ERHC":
                agent = Household(index,self, "ERHC",row["latitude"],row["longitude"],0,ERHCMAX,ERHCFARTHERPROB,CLOSERPROB,self.space.crs)
                self.schedule.add(agent)
                self.space.add_agents(agent)
            if row["category"] == "ERLC":
                agent = Household(index,self, "ERLC",row["latitude"],row["longitude"],0,ERLCMAX,ERLCFARTHERPROB,CLOSERPROB,self.space.crs)
                self.schedule.add(agent)
                self.space.add_agents(agent)
            if row["category"] == "LRHC":
                agent = Household(index,self, "LRHC",row["latitude"],row["longitude"],0,LRHCMAX,LRHCFARTHERPROB,CLOSERPROB,self.space.crs)
                self.schedule.add(agent)
                self.space.add_agents(agent)
            if row["category"] == "LRLC":
                agent = Household(index,self, "LRLC",row["latitude"],row["longitude"],0,LRLCMAX,LRLCFARTHERPROB,CLOSERPROB,self.space.crs)
                self.schedule.add(agent)
                self.space.add_agents(agent)
  
    def step(self) -> None:

        """
        Step function. Runs one step of the GeoModel.
        """
        self.schedule.step()