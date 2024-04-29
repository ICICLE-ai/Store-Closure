#file for agent based model algorithm for households
import math
import random
from constants import SEARCHRADIUS, ERHCMAX, ERLCMAX, LRHCMAX, LRLCMAX, ERHCFARTHERPROB, ERLCFARTHERPROB, LRHCFARTHERPROB, LRLCFARTHERPROB, CLOSERPROB

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
        self.id = int(id)
        self.household_type = str(household_type)
        self.lat = float(lat)
        self.lon = float(lon)
        self.mfai = int(mfai)

    def calculate_distance(self, otherLat, otherLon):
        """
        Calculates euclidean distance from self to other point
        """
        return math.sqrt((self.lat - otherLat)**2 + (self.lon - otherLon)**2)
    
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

    def step(self, mfaiMax, fartherProb, closerProb, storeList):
        """
        Defines agent behavior at each step
        (1) Finds a list of neighboring supermarket agents (SPM/CSPM)
        (2) Chooses one from the list based on market distance and pre-defined agent probabilities
        (3) Calculates food availability based on chosen market
        """
        #(1) find all stores within SEARCHRADIUS
        nearestSPMs, nearestCSPMs = self.find_closest_stores(storeList, SEARCHRADIUS)

        #(2) choose one from list based on probs
        SPMChoice = nearestSPMs[0]  #tuple of store and distance, closest SPM
        CSPMChoice = nearestCSPMs[0]  #tuple of store and distance, closest CSPM
        if(SPMChoice[1]>CSPMChoice[1]):
            #if farther, choose SPM with fartherprob
            chosen = random.choices([SPMChoice[0],CSPMChoice[0]], weights=[fartherProb,1-fartherProb])[0]
        else:
            #if closer, choose SPM with closerprob
            chosen = random.choices([SPMChoice[0],CSPMChoice[0]], weights=[closerProb,1-closerProb])[0]
        #(3) calculate mfai like self.mfai = chosenMarket.fsa / mfaiMax
        foodFromVisit =  int ((chosen.fsa / mfaiMax)*100) #increment household's mfai by store's score
        self.mfai += foodFromVisit
        #TODO implement behavioral rules from slide 10 of ABM literature presentation: 0.8 for LC, 0.8 for LR, movement speeds?
            # foodFromVisit =  chosen.fsa * hasNoCar*0.8 *hasLowResource*0.8  #increment household's mfai by store's score
            # self.mfai += int ((foodFromVisit / mfaiMax)*100)

#below are classes for ERHC, ERLC, LRHC, LRLC that are subclasses of BaseAgent 
class ERHC(BaseAgent):
    def __init__(self, id, household_type, lat, lon, mfai):
        super().__init__(id, household_type, lat=lat, lon=lon, mfai=mfai)
    def step(self,storeList):
        """Step function for ERHC, uses specific constants for mfaiMax and fartherProbability"""
        super().step(mfaiMax=ERHCMAX, fartherProb=ERHCFARTHERPROB, closerProb=CLOSERPROB, storeList=storeList)

class ERLC(BaseAgent):
    def __init__(self, id, household_type, lat, lon, mfai):
        super().__init__(id, household_type=household_type, lat=lat, lon=lon, mfai=mfai)
    def step(self,storeList):
        """Step function for ERLC, uses specific constants for mfaiMax and fartherProbability"""
        super().step(mfaiMax=ERLCMAX, fartherProb=ERLCFARTHERPROB, closerProb=CLOSERPROB, storeList=storeList)

class LRHC(BaseAgent):
    def __init__(self, id, household_type, lat, lon, mfai):
        super().__init__(id, household_type=household_type, lat=lat, lon=lon, mfai=mfai)
    def step(self,storeList):
        """Step function for LRHC, uses specific constants for mfaiMax and fartherProbability"""
        super().step(mfaiMax=LRHCMAX, fartherProb=LRHCFARTHERPROB, closerProb=CLOSERPROB, storeList=storeList)

class LRLC(BaseAgent):
    def __init__(self, id, household_type, lat, lon, mfai):
        super().__init__(id, household_type=household_type, lat=lat, lon=lon, mfai=mfai)
    def step(self,storeList):
        """Step function for LRLC, uses specific constants for mfaiMax and fartherProbability"""
        super().step(mfaiMax=LRLCMAX, fartherProb=LRLCFARTHERPROB, closerProb=CLOSERPROB, storeList=storeList)
              