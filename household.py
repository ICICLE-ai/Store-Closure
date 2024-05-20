from mesa_geo import GeoAgent
from shapely.geometry import Polygon
from shapely.ops import transform
import pyproj
from store import Store
import random
from constants import (
    SEARCHRADIUS # How far the household looks for store candidates
)


class Household(GeoAgent):

    """
    Represents one Household. Extends the mesa_geo GeoAgent class. The step function
    defines the behavior of a single household on each step through the model.
    """

    def __init__(self, house_id: int, model: "GeoModel", lat: float, lon: float, farther_prob: float, closer_prob: float, trips_per_month: int, max_carry_percent: float, crs: str):
        """
        Initialize the Household Agent.

        Args:
            - house_id (int): Unique id.
            - model (GeoModel): model from mesa that places Households on a GeoSpace
            - lat (float): latitude of agent.
            - lon (float): longitude of agent.
            - farther_prob (float): probabilty that the agent goes to the supermarket if it is farther than the convenience store
            - closer_prob (float): proability that the agent goes to the supermarket if it is closer than the convenience store
            - trips_per_month: Number of times the agent goes to the store every month
            - max_carry_percent: Percent of food that an agent can bring home from the store. This percentage is lower if the
                agent does not have a car because of the physical strain of carrying groceries. the amount of food an agent
                can carry home per trip is calculated as: food per trip = (Stores FSA score) * (max_carry_percent)
        """

        #Transform shapely coordinates to mercator projection coords
        polygon = Polygon(((lat+0.00008, lon+0.0001),(lat-0.00008, lon+0.0001),(lat-0.00008, lon-0.0001),(lat+0.00008, lon-0.0001)))
        project = pyproj.Transformer.from_proj(
            pyproj.Proj('epsg:4326'), # source coordinate system
            pyproj.Proj('epsg:3857')) # destination coordinate system
        polygon = transform(project.transform, polygon)  # apply projection

        super().__init__(house_id,model,polygon,crs)
        self.mfai = 100
        self.mfai_max = 100 * trips_per_month * max_carry_percent # Maximum food that an agent could obtain per month if they went to a store with a perfect FSA score
                # every visit. calculated as: mfai_max = (perfect FSA score of 100) * (max_carry_percent) * (trips_per_month)
        self.farther_prob = farther_prob
        self.closer_prob = closer_prob
        self.model = model
        self.trips_per_month = trips_per_month
        self.max_carry_percent = max_carry_percent

    def step(self) -> None:
        """
        Defines the behavior of a single household on each step through the model.

        Currently does:
        (1) Finds closest SPM and Closest CSPM
        (2) Randomly (weighted by closer_prob or farther_prob chooses either the cspm or the spm to go to.
        (3) Calculates mfai based on chosen store's fsa score
        
        """
        #(1) find all agents within SEARCHRADIUS
        closest_agents = self.model.space.get_neighbors_within_distance(self,SEARCHRADIUS)

        #Find all Stores within SEARCHRADIUS, and get closest store.
        closest_cspm = None
        cspm_distance = SEARCHRADIUS
        closest_spm = None
        spm_distance = SEARCHRADIUS
        #Get closest cspm and closest spm
        for agent in closest_agents:
            if (isinstance(agent,Store)):
                if (agent.category == "SPM"):
                    distance = self.model.space.distance(self,agent)
                    if distance < spm_distance:
                        spm_distance = distance
                        closest_spm = agent
                if (agent.category == "CSPM"):
                    distance = self.model.space.distance(self,agent)
                    if distance < cspm_distance:
                        cspm_distance = distance
                        closest_cspm = agent

        #Randomly (with weighted by closer prob or farther prob) choose to go to cspm or spm
        chosen_store = None
        if(spm_distance>cspm_distance):
            #if farther, choose SPM with fartherprob
            chosen_store = random.choices([closest_spm,closest_cspm], weights=[self.farther_prob,1-self.farther_prob])[0]
        else:
            #if closer, choose SPM with closerprob
            chosen_store = random.choices([closest_spm,closest_cspm], weights=[self.closer_prob,1-self.closer_prob])[0]
        
        # calculate mfai score:
        # code returns a moving average, however mfai per month is calculated like:
        # FOR EACH VISIT: (number of visits per month given by trips_per_month)
        # Sum of Food per month += ((Store's FSA score) * (Percent that the agent can carry))
        # AT END OF MONTH
        # mfai = ((Sum of Food per month) / (Maximum MFAI)) * 100
        food_on_this_visit = ((chosen_store.fsa*self.max_carry_percent) / self.mfai_max) * 100
        self.mfai = (self.mfai - self.mfai/self.trips_per_month) + food_on_this_visit

    """
    ALAN's OLD STEP FUNCTION - ONLY FOR REFERENCE:

    Define agent behavior at each step.

        (1) Finds a list of neighboring supermarket agents (SPM/CSPM)
        (2) Chooses one from the list based on market distance and pre-defined agent probabilities
        (3) Calculates food availability based on chosen market.

        #(2) choose one from list based on probs
        spm_choice = nearest_spms[0]  #tuple of store and distance, closest SPM
        cspm_choice = nearest_cspms[0]  #tuple of store and distance, closest CSPM
        if(spm_choice[1]>cspm_choice[1]):
            #if farther, choose SPM with fartherprob
            chosen = random.choices([spm_choice[0],cspm_choice[0]], weights=[farther_prob,1-farther_prob])[0]
        else:
            #if closer, choose SPM with closerprob
            chosen = random.choices([spm_choice[0],cspm_choice[0]], weights=[closer_prob,1-closer_prob])[0]
        #(3) calculate mfai like self.mfai = chosenMarket.fsa / mfai_max
        food_from_visit =  int ((chosen.fsa / mfai_max)*100) #increment household's mfai by store's score
        self.mfai += food_from_visit
        #TODO implement behavioral rules from slide 10 of ABM literature presentation: 0.8 for LC, 0.8 for LR, movement speeds?
            # foodFromVisit =  chosen.fsa * hasNoCar*0.8 *hasLowResource*0.8  #increment household's mfai by store's score
            # self.mfai += int ((foodFromVisit / mfai_max)*100)

    """