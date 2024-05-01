"""Module for agent-based model algorithm for households."""
import math
import random

from constants import (
    CLOSERPROB,
    ERHCFARTHERPROB,
    ERHCMAX,
    ERLCFARTHERPROB,
    ERLCMAX,
    LRHCFARTHERPROB,
    LRHCMAX,
    LRLCFARTHERPROB,
    LRLCMAX,
    SEARCHRADIUS,
)


class BaseAgent:
    """Base algorithm for each agents' behavior.

    Attributes
    ----------
        - house_id (int): Unique id.
        - household_type (string): ERHC, ERLC, LRHC, or LRLC.
        - lat (float): latitude of agent.
        - lon (float): longitude of agent.
        - mfai (int): food availability.

    """

    def __init__(self, house_id, household_type, lat, lon, mfai):
        """Initialize agent's attributes."""
        self.house_id = int(house_id)
        self.household_type = str(household_type)
        self.lat = float(lat)
        self.lon = float(lon)
        self.mfai = int(mfai)

    def calculate_distance(self, otherLat, otherLon):
        """Calculate euclidean distance from self to other point."""
        return math.sqrt((self.lat - otherLat)**2 + (self.lon - otherLon)**2)

    def find_closest_stores(self, stores, search_radius):
        """Find the closest stores to home within search_radius."""
        closest_spms = []
        closest_cspms = []
        for store in stores:
            distance = self.calculate_distance(store.lat, store.lon)
            if distance <= search_radius:
                if store.category == "SPM":
                    closest_spms.append((store, distance))
                elif store.category == "CSPM":
                    closest_cspms.append((store, distance))
                else:
                    print("store",store.store_id,"does not have category!") #error case
        #sort the lists by distance
        closest_spms = sorted(closest_spms, key=lambda x: x[1])
        closest_cspms = sorted(closest_cspms, key=lambda x: x[1])
        return closest_spms,closest_cspms

    def step(self: "BaseAgent", mfai_max: int, farther_prob: float, closer_prob: float, store_list: list) -> None:
        """Define agent behavior at each step.

        (1) Finds a list of neighboring supermarket agents (SPM/CSPM)
        (2) Chooses one from the list based on market distance and pre-defined agent probabilities
        (3) Calculates food availability based on chosen market.
        """
        #(1) find all stores within SEARCHRADIUS
        nearest_spms, nearest_cspms = self.find_closest_stores(store_list, SEARCHRADIUS)

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

#below are classes for ERHC, ERLC, LRHC, LRLC that are subclasses of BaseAgent
class ERHC(BaseAgent):
    """ERHC Household: Enough Resources Has Car."""

    def __init__(self: "ERHC", house_id: int, household_type: str, lat: float, lon: float, mfai: int) -> None:
        """Initialize ERHC Household."""
        super().__init__(house_id, household_type, lat=lat, lon=lon, mfai=mfai)
    def step(self: "LRLC", store_list: list) -> None:
        """Step function for ERHC, uses specific constants for mfai_max and fartherProbability."""
        super().step(mfai_max=ERHCMAX, farther_prob=ERHCFARTHERPROB, closer_prob=CLOSERPROB, store_list=store_list)

class ERLC(BaseAgent):
    """ERLC Household: Enough Resources Low Car."""

    def __init__(self: "ERLC", house_id: int, household_type: str, lat: float, lon: float, mfai: int) -> None:
        """Initialize ERLC Household."""
        super().__init__(house_id, household_type=household_type, lat=lat, lon=lon, mfai=mfai)
    def step(self: "ERLC", store_list: list) -> None:
        """Step function for ERLC, uses specific constants for mfai_max and fartherProbability."""
        super().step(mfai_max=ERLCMAX, farther_prob=ERLCFARTHERPROB, closer_prob=CLOSERPROB, store_list=store_list)

class LRHC(BaseAgent):
    """LRHC Household: Low Resources Has Car."""

    def __init__(self: "LRHC", house_id: int, household_type: str, lat: float, lon: float, mfai: int) -> None:
        """Initialize LRHC Household."""
        super().__init__(house_id, household_type=household_type, lat=lat, lon=lon, mfai=mfai)
    def step(self: "LRHC", store_list: list) -> None:
        """Step function for LRHC, uses specific constants for mfai_max and fartherProbability."""
        super().step(mfai_max=LRHCMAX, farther_prob=LRHCFARTHERPROB, closer_prob=CLOSERPROB, store_list=store_list)

class LRLC(BaseAgent):
    """LRLC Household: Low Resources Low Car."""

    def __init__(self: "LRLC", house_id: int, household_type: str, lat: float, lon: float, mfai: int) -> None:
        """Initialize LRLC Household."""
        super().__init__(house_id, household_type=household_type, lat=lat, lon=lon, mfai=mfai)
    def step(self: "LRLC", store_list: list) -> None:
        """Step function for LRLC, uses specific constants for mfai_max and fartherProbability."""
        super().step(mfai_max=LRLCMAX, farther_prob=LRLCFARTHERPROB, closer_prob=CLOSERPROB, store_list=store_list)
