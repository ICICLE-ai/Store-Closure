from mesa_geo import GeoAgent
from shapely.geometry import Polygon
from shapely.ops import transform
import pyproj
from store import Store
import random
random.seed(1)


class Household(GeoAgent):

    """
    Represents one Household. Extends the mesa_geo GeoAgent class. The step function
    defines the behavior of a single household on each step through the model.
    """

    def __init__(self, house_id: int, model: "GeoModel", lat: float, lon: float, farther_prob: float, closer_prob: float, trips_per_month: int, max_carry_percent: float, search_radius: int, crs: str):
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
            - search_radius: how far to search for stores (units unclear??)
            - crs: geometry
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
        self.search_radius = search_radius

    def choose_store(self, search_radius):
        """
        Helper method for step function. This method optimizes time complexity of the step function
        by recursively increasing search radius until it finds a spm and a cspm. Ideally this function will not
        recurse except in edge cases. Ultimately, this method finds and chooses store to shop at.

        TODO: statistical analysis should be used to find the most optimal search radius and increase to search radius
        for each step. This function is the main bottleneck for speed in this model and should be optimized perfectly.

        Args:
            - search_radius: radius to search for stores.

        returns:
            - chosen_store: chosen store to shop at.
        """

        #(1) find all agents within search radius
        closest_agents = self.model.space.get_neighbors_within_distance(self,search_radius)

        #Find all Stores within search radius, and get closest store.
        closest_cspm = None
        cspm_distance = search_radius
        closest_spm = None
        spm_distance = search_radius
        #Get closest cspm and closest spm
        for agent in closest_agents:
            if (isinstance(agent,Store)):
                if (agent.category == "SPM"):
                    distance = self.model.space.distance(self,agent)
                    if distance <= spm_distance:
                        spm_distance = distance
                        closest_spm = agent
                if (agent.category == "CSPM"):
                    distance = self.model.space.distance(self,agent)
                    if distance <= cspm_distance:
                        cspm_distance = distance
                        closest_cspm = agent

        #If stores could not be found with current search radius, expand search radius
        if (closest_cspm == None) or (closest_spm == None):
            return self.choose_store(search_radius+500)

        #Randomly (with weighted by closer prob or farther prob) choose to go to cspm or spm
        chosen_store = None
        distance = self.model.space.distance(self,closest_spm)
        #print(distance)
        distance = self.model.space.distance(self,closest_cspm)
        #print(distance)
        if(spm_distance>cspm_distance):
            #if farther, choose SPM with fartherprob
            chosen_store = random.choices([closest_spm,closest_cspm], weights=[self.farther_prob,1-self.farther_prob])[0]
        else:
            #if closer, choose SPM with closerprob
            chosen_store = random.choices([closest_spm,closest_cspm], weights=[self.closer_prob,1-self.closer_prob])[0]

        return chosen_store
    
    def step(self) -> None:
        """
        Defines the behavior of a single household on each step through the model.

        (1) Finds closest SPM and Closest CSPM
        (2) Calculates mfai based on chosen store's fsa score
        
        """
        chosen_store = self.choose_store(self.search_radius)

        # calculate mfai score:
        # code returns a moving average, however mfai per month is calculated like:
        # FOR EACH VISIT: (number of visits per month given by trips_per_month)
        # Sum of Food per month += ((Store's FSA score) * (Percent that the agent can carry))
        # AT END OF MONTH
        # mfai = ((Sum of Food per month) / (Maximum MFAI)) * 100
        food_on_this_visit = ((chosen_store.fsa*self.max_carry_percent) / self.mfai_max) * 100
        self.mfai = (self.mfai - self.mfai/self.trips_per_month) + food_on_this_visit