import pandas as pd
import geopandas
import random
random.seed(1)

#Loads household and store data from csv files
stores_file_path = "data/marketdata.csv"
households_file_path = "data/homedata.csv"

#Dictionary to describe homedata Variables
households_variables_dict = {
    "B19001_001E": "total population in tract",
    "B19001_002E": "total population under $10,000",
    "B19001_003E": "total population 10k to 15k",
    "B19001_004E": "total population 15k to 20k",
    "B19001_005E": "total population 20k to 25k",
    "B19001_006E": "total population 25k to 30k",
    "B19001_007E": "total population 30k to 35k",
    "B19001_008E": "total population 35k to 40k",
    "B19001_009E": "total population 40k to 45k",
    "B19001_010E": "total population 45k to 50k",
    "B19001_011E": "total population 50k to 60k",
    "B19001_012E": "total population 60k to 75k",
    "B19001_013E": "total population 75k to 100k",
    "B19001_014E": "total population 100k to 125k",
    "B19001_015E": "total population 125k to 150k",
    "B19001_016E": "total population 150k to 200k",
    "B19001_017E": "total population 200k+",
}
households_variables_list = (
    "B19001_001E",
    "B19001_002E",
    "B19001_003E",
    "B19001_004E",
    "B19001_005E",
    "B19001_006E",
    "B19001_007E",
    "B19001_008E",
    "B19001_009E",
    "B19001_010E",
    "B19001_011E",
    "B19001_012E",
    "B19001_013E",
    "B19001_014E",
    "B19001_015E",
    "B19001_016E",
    "B19001_017E",
)

ohio_geodata = geopandas.read_file("data/tl_2022_39_tract.zip")
franklin_geodata = ohio_geodata[ohio_geodata['COUNTYFP'] == "039"]
franklin_geodata.to_crs(epsg=3857)
franklin_geodata = franklin_geodata.rename(columns={"TRACTCE":"tract"})
tract_data = pd.merge(franklin_geodata, TRACT DATAFRAME NAME HERE, on = "tract", how="inner")

#Stores data in variables. This data is imported by run.py
#and used to intialize the GeoModel
households = pd.read_csv(households_file_path)
stores = pd.read_csv(stores_file_path)

