from mesa_geo import GeoAgent
from shapely.geometry import Polygon
from shapely.ops import transform
import pyproj
from store import Store
from constants import (
    SEARCHRADIUS # How far the household looks for store candidates
)


class Household(GeoAgent):

    """
    Represents one Household. Extends the mesa_geo GeoAgent class. The step function
    defines the behavior of a single household on each step through the model.
    """

    def __init__(self, house_id: int, model: "GeoModel", household_type: str, lat: float, lon: float, mfai: int, mfai_max: int, farther_prob: float, closer_prob: float,crs: str, trips_per_month: int):
        """
        Initialize the Household Agent.

        Args:
            - house_id (int): Unique id.
            - model (GeoModel): model from mesa that places Households on a GeoSpace
            - household_type (string): ERHC, ERLC, LRHC, or LRLC.
            - lat (float): latitude of agent.
            - lon (float): longitude of agent.
            - mfai (int): food availability.
        """

        #Transform shapely coordinates to mercator projection coords
        polygon = Polygon(((lat+0.00008, lon+0.0001),(lat-0.00008, lon+0.0001),(lat-0.00008, lon-0.0001),(lat+0.00008, lon-0.0001)))
        project = pyproj.Transformer.from_proj(
            pyproj.Proj('epsg:4326'), # source coordinate system
            pyproj.Proj('epsg:3857')) # destination coordinate system
        polygon = transform(project.transform, polygon)  # apply projection

        super().__init__(house_id,model,polygon,crs)
        self.household_type = household_type
        self.mfai = mfai
        self.mfai_max = mfai_max
        self.farther_prob = farther_prob
        self.closer_prob = closer_prob
        self.model = model
        self.trips_per_month = trips_per_month

    def step(self) -> None:
        """
        Defines the behavior of a single household on each step through the model.

        Currently does:
        (1) Finds a list of neighboring agents
        
        """
        #(1) find all agents within SEARCHRADIUS
        closest_agents = self.model.space.get_neighbors_within_distance(self,SEARCHRADIUS)

        #Find all Stores within SEARCHRADIUS, and get closest store.
        closest_store = None
        closest_stores = list()
        #Get list of all closest stores
        for agent in closest_agents:
            if (isinstance(agent,Store)):
                closest_stores.append([agent,self.model.space.distance(self,agent)])
        maxi = 0
        #Get closest store
        for item in closest_stores:
            if item[1] > maxi:
                maxi = item[1]
                closest_store = item[0]
        
        #calculate mfai
        mfai_6 = self.mfai - self.mfai/self.trips_per_month
        mfai_6 += ((closest_store.fsa) / self.mfai_max) * 100
        self.mfai = mfai_6
        #print(self.mfai - self.mfai/7)
        #print(((closest_store.fsa) / self.mfai_max) * 100)

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