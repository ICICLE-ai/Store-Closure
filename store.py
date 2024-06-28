from mesa_geo import GeoAgent
from shapely.geometry import Polygon
from shapely.ops import transform
import pyproj


class Store(GeoAgent):
    """
    Represents a Store. Extends the mesa_geo GeoAgent class. A store can either
    be a "CSPM" (convenience store) or a "SPM" (supermarket).
    """

    def __init__(self,  model, id: int, name, type, lat: float, lon: float, crs) -> None:
        """
        Initialize the Household Agent.

        Args:
            - store_id (int): unique id
            - model (GeoModel): model from mesa that places stores on a GeoSpace
            - category (string): SPM or CSPM
            - lat (float): latitude of agent
            - lon (float): longitude of agent
            - fsa (int): Food Store Audit (index indicating the percentage of 87 USDA TFP items available at the store)
        """

        #Transform shapely coordinates to mercator projection coords
        polygon = Polygon(((lat+0.00016, lon),(lat-0.00032, lon-0.00032),(lat-0.00032, lon+0.00032)))
        project = pyproj.Transformer.from_proj(
            pyproj.Proj('epsg:4326'), # source coordinate system
            pyproj.Proj('epsg:3857')) # destination coordinate system
        polygon = transform(project.transform, polygon)  # apply projection

        super().__init__(id,model,polygon,crs) # epsg:3857 is the mercator projection
        self.type = type
        self.name = name