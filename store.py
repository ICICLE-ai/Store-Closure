from mesa_geo import GeoAgent
from shapely.geometry import Point

"""Module containing SPM and CSPM food store classes."""

class Store(GeoAgent):
    """Class for SPM or CSPM.

    Attributes
    ----------
        - store_id (int): unique id
        - category (string): SPM or CSPM
        - lat (float): latitude of agent
        - lon (float): longitude of agent
        - fsa (int): Food Store Audit (index indicating the percentage of 87 USDA TFP items available at the store)

    """

    def __init__(self: "Store",  model: "GeoModel", store_id: int, category: str, lat: float, lon: float, fsa: int) -> None:
        """Initialize food store."""
        super().__init__(store_id,model,Point(lat,lon),"epsg:3857") # epsg:3857 is the mercator projection
        self.category = str(category)
        self.fsa = int(fsa)