#this file contains SPM and CSPM food store classes

class store():
    """
    This class represents an SPM or CSPM based on category
    Attributes: 
        - id (int): unique id
        - category (string): SPM or CSPM
        - lat (float): latitude of agent
        - lone (float): longitude of agent
        - FSA (int): Food Store Audit (index indicating the percentage of 87 USDA TFP items available at the store)
    """
    def __init__(self, id, category, lat, lon, FSA):
        """Initializes food store"""
        self.id = id
        self.category = category
        self.lat = lat
        self.lon = lon
        self.FSA = FSA
