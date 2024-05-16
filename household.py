from mesa_geo import GeoAgent
from shapely.geometry import Polygon
from shapely.ops import transform
import pyproj
from constants import (
    SEARCHRADIUS # How far the household looks for store candidates
)


class Household(GeoAgent):

    """
    Represents one Household. Extends the mesa_geo GeoAgent class. The step function
    defines the behavior of a single household on each step through the model.
    """

    def __init__(self, house_id: int, model: "GeoModel", household_type: str, lat: float, lon: float, mfai: int, mfai_max: int, farther_prob: float, closer_prob: float,crs):
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
        polygon = Polygon(((lat+0.0001, lon+0.0001),(lat-0.0001, lon+0.0001),(lat-0.0001, lon-0.0001),(lat+0.0001, lon-0.0001)))
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

    def step(self) -> None:
        """
        Defines the behavior of a single household on each step through the model.

        Currently does:
        (1) Finds a list of neighboring agents
        
        """
        #(1) find all stores within SEARCHRADIUS
        closest_agents = self.model.space.get_neighbors_within_distance(self,SEARCHRADIUS)