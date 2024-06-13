import pandas as pd
import geopandas
import random
random.seed(1)

county_data_filepath = "franklin_data.csv"
geodata_filepath = "data/tl_2022_39_tract.zip"

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

county_data = pd.read_csv(county_data_filepath)
geodata = geopandas.read_file(geodata_filepath)
county_geodata = geodata[geodata['COUNTYFP'] == "039"]
county_geodata.to_crs(epsg=3857)
county_geodata = county_geodata.rename(columns={"TRACTCE":"tract"})
data = pd.merge(county_geodata, county_data, on = "tract", how="inner")
fake_households = pd.DataFrame()
for row in data.iterrows():
  for i in range(row["B19001_001E"]):
    


#Stores data in variables. This data is imported by run.py
#and used to intialize the GeoModel
households = 
stores = pd.read_csv("marketdata.csv")

