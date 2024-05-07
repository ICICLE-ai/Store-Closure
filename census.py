# Imports
from pandas import DataFrame
import requests
from geopandas import read_file
from io import BytesIO


class CensusAPI:
    
    """
    Class Initialization Arguments:
    census_api_key   #API key to access census data
    """
    def __init__(self,census_api_key):
        self.census_api_key = census_api_key
    

    """
    Get ACS (American Community Survey) data.

    Arguments:
    variables      #List of variables requested from ACS data set
    state_name     #State name eg. "Wisconsin" OR "*" for all states (counties must also be "*")
    county_name    #County name eg. "Milwaukee County" (must include the "County") OR "*" for all counties
    year           #Year of data

    Returns Pandas Dataframe
    """
    def get_acs_data(self, variables, state_name, county_name, year):
        state_code = 0
        county_code = 0
        if (type(variables) != list):
            raise Exception("Variables must be in a list even if you only have one. e.g [B01001_001E] or [B01001_001E,B01001_001C]")
        if (state_name != "*") and (county_name != "*"):
            state_code, county_code = self.get_state_and_county_code(state_name,county_name)
        elif (county_name == "*") and (state_name != "*"):
            state_code = self.get_state_code(state_name)
            county_code = "*"
        elif (state_name == "*") and (county_name == "*"):
          state_code = "*"
          county_code = "*"
        else:
            raise Exception("Incorrect arguments for get_acs_data")
        variables = ",".join(variables)
        # URL for ACS data
        survey_url = f"https://api.census.gov/data/{year}/acs/acs5?get=NAME,{variables}&for=county:{county_code}&in=state:{state_code}&key={self.census_api_key}"
        # Request ACS data
        response = requests.request("GET", survey_url)
        if response.status_code != 200:
            raise Exception("API Call Failed")
        acs_data = DataFrame(response.json()[1:], columns=response.json()[0])
        return acs_data

    
    """
    Get Geographical data for given state.

    Arguments:
    state_name     #State name eg. "Wisconsin"
    year           #Year of data

    Returns Geopandas DataFrame.
    """
    def get_geo_data(self, state_name, year):
        state_code = self.get_state_code(state_name)
        # Load in tract data
        tract_url = f"https://www2.census.gov/geo/tiger/TIGER{year}/TRACT/tl_{year}_{state_code}_tract.zip"
        response = requests.request("GET", tract_url)
        print(response)
        data = response.content
        # Convert data to GeoDataFrame
        geo_tract_data = read_file(BytesIO(data))
        return geo_tract_data

    
    """Helper Method for class"""
    def get_state_and_county_code(self,state_name,county_name):
        # URL for getting county and state codes
        states_url = f"https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=county:*&in=state:*&key={self.census_api_key}"
        
        # Request States data
        response = requests.request("GET", states_url)
        if response.status_code != 200:
            raise Exception("API Call Failed")
        states_data = DataFrame(response.json()[1:], columns=["County, State", "Zipcode", "State Code", "County Code"])
        
        #Get state code and county code
        county_code = 0
        state_code = 0
        for index,row in states_data.iterrows():
            if (row["County, State"] == f"{county_name}, {state_name}"):
                state_code = row["State Code"]
                county_code = row["County Code"]
                break
        if (state_code == 0) or (county_code == 0):
            raise Exception("Could not find state and/or county")
        return state_code, county_code

    """Helper Method for class"""
    def get_state_code(self,state_name):
        # URL for getting county and state codes
        states_url = f"https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=county:*&in=state:*&key={self.census_api_key}"
        
        # Request States data
        response = requests.request("GET", states_url)
        if response.status_code != 200:
            raise Exception("API Call Failed")
        states_data = DataFrame(response.json()[1:], columns=["County, State", "Zipcode", "State Code", "County Code"])
        
        #Get state code and county code
        state_code = 0
        for index,row in states_data.iterrows():
            if (row["County, State"].endswith(state_name)):
                state_code = row["State Code"]
                break
        if (state_code == 0):
            raise Exception("Could not find state and/or county")
        return state_code
