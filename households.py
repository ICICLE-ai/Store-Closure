#file for agent based model algorithm for households
from constants import SEARCHRADIUS, ERHCMAX, ERLCMAX, LRHCMAX, LRLCMAX, ERHCFARTHERPROB, ERLCFARTHERPROB, LRHCFARTHERPROB, LRLCFARTHERPROB, CLOSERPROB

class BaseAgent:
    """
    This class represents the base algorithm for each agents' behavior
    Attributes: 
        - id (int): Unique id
        - household_type (string): ERHC, ERLC, LRHC, or LRLC
        - x (float): latitude of agent
        - y (float): longitude of agent
        - mfai (int): food availability
    """
    def __init__(self, id, household_type, x, y, mfai):
        self.id = id
        self.household_type = household_type
        self.x = x
        self.y = y
        self.mfai = mfai

    def step(self, mfaiMax, fartherProb, closerProb):
         """
        Defines agent behavior at each step
        (1) Finds a list of neighboring supermarket agents (SPM/CSPM)
        (2) Chooses one from the list based on market distance and pre-defined agent probabilities
        (3) Calculates food availability based on chosen market
        """
        #find all stores in SEARCHRADIUS

        #choose one from list based on probs

        #calculate mfai like self.mfai = chosenMarket.fsa / mfaiMax

        

class ERHC(BaseAgent):
    def __init__(self, id, x, y, mfai):
        super().__init__(id, household_type="ERHC", x=x, y=y, mfai=mfai)
    def step(self):
         super().step(mfaiMax=ERHCMAX, fartherProb=ERHCFARTHERPROB, closerProb=CLOSERPROB)
        