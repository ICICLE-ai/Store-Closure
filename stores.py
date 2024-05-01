"""Module containing SPM and CSPM food store classes."""

class Store:
    """Class for SPM or CSPM.

    Attributes
    ----------
        - store_id (int): unique id
        - category (string): SPM or CSPM
        - lat (float): latitude of agent
        - lon (float): longitude of agent
        - fsa (int): Food Store Audit (index indicating the percentage of 87 USDA TFP items available at the store)

    """

    def __init__(self: "Store", store_id: int, category: str, lat: float, lon: float, fsa: int) -> None:
        """Initialize food store."""
        self.store_id = int(store_id)
        self.category = str(category)
        self.lat = float(lat)
        self.lon = float(lon)
        self.fsa = int(fsa)
