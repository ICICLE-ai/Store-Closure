#file for agent based model algorithm for households
import math
import random
from constants import SEARCHRADIUS, ERHCMAX, ERLCMAX, LRHCMAX, LRLCMAX, ERHCFARTHERPROB, ERLCFARTHERPROB, LRHCFARTHERPROB, LRLCFARTHERPROB, CLOSERPROB
#from stores import store 
#TODO: get access to list of stores

class BaseAgent:
    """
    This class represents the base algorithm for each agents' behavior
    Attributes: 
        - id (int): Unique id
        - household_type (string): ERHC, ERLC, LRHC, or LRLC
        - lat (float): latitude of agent
        - lon (float): longitude of agent
        - mfai (int): food availability
    """
    def __init__(self, id, household_type, lat, lon, mfai):
        """
        Initializes agent's attributes
        """
        self.id = id
        self.household_type = household_type
        self.lat = lat
        self.lon = lon
        self.mfai = mfai

    def calculate_distance(self, otherLat, otherLon):
        """
        Calculates euclidean distance from self to other point
        """
        return math.sqrt((self.lat - otherLat)^2 + (self.lon - otherLon)^2)
    
    def find_closest_stores(self, stores, search_radius):
        """
        Find the closest stores to home within search_radius
        """
        closest_spms = []
        closest_cspms = []
        for store in stores:
            distance = self.calculate_distance(store.lat, store.lon)
            if distance <= search_radius:
                if store.category == "SPM":
                    closest_spms.append((store, distance))
                elif store.category == "CSPM":
                    closest_cspms.append((store, distance))
                else:
                    print("store",id,"does not have category!") #error case
        #sort the lists by distance
        closest_spms = sorted(closest_spms, key=lambda x: x[1])    
        closest_cspms = sorted(closest_cspms, key=lambda x: x[1])
        return closest_spms,closest_cspms

    def step(self, mfaiMax, fartherProb, closerProb):
        """
        Defines agent behavior at each step
        (1) Finds a list of neighboring supermarket agents (SPM/CSPM)
        (2) Chooses one from the list based on market distance and pre-defined agent probabilities
        (3) Calculates food availability based on chosen market
        """
        #(1) find all stores within SEARCHRADIUS
        storeList = [] #TODO: write method to init list of stores
        nearestSPMs, nearestCSPMs = self.find_closest_stores(storeList, SEARCHRADIUS)

        #(2) choose one from list based on probs
        SPMChoice = nearestSPMs[0]  #tuple of store and distance, closest one
        CSPMChoice = nearestCSPMs[0]  #tuple of store and distance, closest one
        if(SPMChoice[1]>CSPMChoice):
            #if farther, choose SPM with fartherprob
            chosen = random.choices([SPMChoice,CSPMChoice], weights=[fartherProb,1-fartherProb])[0]
        else:
            #if closer, choose SPM with closerprob
            chosen = random.choices([SPMChoice,CSPMChoice], weights=[closerProb,1-closerProb])[0]
        #(3) calculate mfai like self.mfai = chosenMarket.fsa / mfaiMax
        self.mfai += chosen.fsa / mfaiMax #increment household's mfai by store's fsa score


class ERHC(BaseAgent):
    def __init__(self, id, lat, lon, mfai):
        super().__init__(id, household_type="ERHC", lat=lat, lon=lon, mfai=mfai)
    def step(self):
         super().step(mfaiMax=ERHCMAX, fartherProb=ERHCFARTHERPROB, closerProb=CLOSERPROB)

class ERLC(BaseAgent):
    def __init__(self, id, lat, lon, mfai):
        super().__init__(id, household_type="ERLC", lat=lat, lon=lon, mfai=mfai)
    def step(self):
         super().step(mfaiMax=ERLCMAX, fartherProb=ERLCFARTHERPROB, closerProb=CLOSERPROB)

class LRHC(BaseAgent):
    def __init__(self, id, lat, lon, mfai):
        super().__init__(id, household_type="LRHC", lat=lat, lon=lon, mfai=mfai)
    def step(self):
         super().step(mfaiMax=LRHCMAX, fartherProb=LRHCFARTHERPROB, closerProb=CLOSERPROB)

class LRLC(BaseAgent):
    def __init__(self, id, lat, lon, mfai):
        super().__init__(id, household_type="LRLC", lat=lat, lon=lon, mfai=mfai)
    def step(self):
         super().step(mfaiMax=LRLCMAX, fartherProb=LRLCFARTHERPROB, closerProb=CLOSERPROB)
              