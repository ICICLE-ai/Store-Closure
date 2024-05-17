from mesa_geo import GeoAgent
from shapely.geometry import Polygon
from shapely.ops import transform
import pyproj


class Store(GeoAgent):
    """
    Represents a Store. Extends the mesa_geo GeoAgent class. A store can either
    be a "CSPM" (convenience store) or a "SPM" (supermarket).
    """

    def __init__(self: "Store",  model: "GeoModel", store_id: int, category: str, lat: float, lon: float, fsa: int,crs) -> None:
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
        polygon = Polygon(((lat+0.00008, lon),(lat-0.00016, lon-0.00016),(lat-0.00016, lon+0.00016)))
        project = pyproj.Transformer.from_proj(
            pyproj.Proj('epsg:4326'), # source coordinate system
            pyproj.Proj('epsg:3857')) # destination coordinate system
        polygon = transform(project.transform, polygon)  # apply projection

        super().__init__(store_id,model,polygon,crs) # epsg:3857 is the mercator projection
        self.category = str(category)
        self.fsa = int(fsa)