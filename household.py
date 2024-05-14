from mesa_geo import GeoAgent
from shapely.geometry import Point
from constants import (
    SEARCHRADIUS
)

class Household(GeoAgent):
    """Base algorithm for each agents' behavior.

    Attributes
    ----------
        - house_id (int): Unique id.
        - household_type (string): ERHC, ERLC, LRHC, or LRLC.
        - lat (float): latitude of agent.
        - lon (float): longitude of agent.
        - mfai (int): food availability.

    """

    def __init__(self, house_id, model, household_type, lat, lon, mfai, mfai_max: int, farther_prob: float, closer_prob: float):
        """Initialize agent's attributes."""
        super().__init__(house_id,model,Point(lat,lon),"epsg:2022")
        self.household_type = str(household_type)
        self.mfai = int(mfai)
        self.mfai_max = mfai_max
        self.farther_prob = farther_prob
        self.closer_prob = closer_prob
        self.model = model

    def step(self: "Household") -> None:
        """Define agent behavior at each step.

        (1) Finds a list of neighboring supermarket agents (SPM/CSPM)
        (2) Chooses one from the list based on market distance and pre-defined agent probabilities
        (3) Calculates food availability based on chosen market.
        """
        #(1) find all stores within SEARCHRADIUS
        closest_stores = self.model.space.get_neighbors_within_distance(self,SEARCHRADIUS)