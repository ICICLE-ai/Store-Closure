import numpy as np
import pandas as pd
import geopandas
from shapely.geometry import Polygon, Point
from shapely.ops import transform
import random
import requests
from io import BytesIO
from zipfile import ZipFile
import tempfile
import os
import pyproj


FIBSCODE = "39049"
YEAR = 2022
from config import APIKEY

county_code = FIBSCODE[2:]
state_code = FIBSCODE[:2]

# Function to generate a random point within a polygon
def get_random_point(tract_polygon,polygons):
    min_x, min_y, max_x, max_y = tract_polygon.bounds
    count = 0
    while True:
        print(count)
        # Generate a random point
        location = Point(random.uniform(min_x, max_x), random.uniform(min_y, max_y))
        
        # Check if the point is inside the polygon
        
        if tract_polygon.contains(location):
            count += 1
            if count == 1000:
                raise Exception()
            polygon = Polygon(((location.x+10, location.y+10),(location.x-10, location.y+10),(location.x-10, location.y-10),(location.x+10, location.y-10)))
            not_touching = True
            for polygon_2 in polygons:
                touches = polygon.intersects(polygon_2)
                if touches:
                    not_touching = False
                    break
            if not_touching:
                return polygon

#Dictionary to describe homedata Variables
households_variables_dict = {
    "B19001_001E": "total households in tract",
    "B19001_002E": "under 10k",
    "B19001_003E": "10k to 15k",
    "B19001_004E": "15k to 20k",
    "B19001_005E": "20k to 25k",
    "B19001_006E": "25k to 30k",
    "B19001_007E": "30k to 35k",
    "B19001_008E": "35k to 40k",
    "B19001_009E": "40k to 45k",
    "B19001_010E": "45k to 50k",
    "B19001_011E": "50k to 60k",
    "B19001_012E": "60k to 75k",
    "B19001_013E": "75k to 100k",
    "B19001_014E": "100k to 125k",
    "B19001_015E": "125k to 150k",
    "B19001_016E": "150k to 200k",
    "B19001_017E": "200k+",
    "B08201_002E": "0 Vehicle(s)",
    "B08201_003E": "1 Vehicle(s)",
    "B08201_004E": "2 Vehicle(s)",
    "B08201_005E": "3 Vehicle(s)",
    "B08201_006E": "4+ Vehicle(s)",
    "B08201_007E": "1 Person(s)",
    "B08201_008E": "1 Person(s) 0 Vehicle(s)",
    "B08201_009E": "1 Person(s) 1 Vehicle(s)",
    "B08201_010E": "1 Person(s) 2 Vehicle(s)",
    "B08201_011E": "1 Person(s) 3 Vehicle(s)",
    "B08201_012E": "1 Person(s) 4+ Vehicle(s)",
    "B08201_013E": "2 Person(s)",
    "B08201_014E": "2 Person(s) 0 Vehicle(s)",
    "B08201_015E": "2 Person(s) 1 Vehicle(s)",
    "B08201_016E": "2 Person(s) 2 Vehicle(s)",
    "B08201_017E": "2 Person(s) 3 Vehicle(s)",
    "B08201_018E": "2 Person(s) 4+ Vehicle(s)",
    "B08201_019E": "3 Person(s)",
    "B08201_020E": "3 Person(s) 0 Vehicle(s)",
    "B08201_021E": "3 Person(s) 1 Vehicle(s)",
    "B08201_022E": "3 Person(s) 2 Vehicle(s)",
    "B08201_023E": "3 Person(s) 3 Vehicle(s)",
    "B08201_024E": "3 Person(s) 4+ Vehicle(s)",
    "B08201_025E": "4+ Person(s)",
    "B08201_026E": "4+ Person(s) 0 Vehicle(s)",
    "B08201_027E": "4+ Person(s) 1 Vehicle(s)",
    "B08201_028E": "4+ Person(s) 2 Vehicle(s)",
    "B08201_029E": "4+ Person(s) 3 Vehicle(s)",
    "B08201_030E": "4+ Person(s) 4+ Vehicle(s)",
    "B08202_002E": "0 Worker(s)",
    "B08202_003E": "1 Worker(s)",
    "B08202_004E": "2 Worker(s)",
    "B08202_005E": "3+ Worker(s)",
    "B08202_007E": "1 Person(s) 0 Worker(s)",
    "B08202_008E": "1 Person(s) 1 Worker(s)",
    "B08202_010E": "2 Person(s) 0 Worker(s)",
    "B08202_011E": "2 Person(s) 1 Worker(s)",
    "B08202_012E": "2 Person(s) 2 Worker(s)",
    "B08202_014E": "3 Person(s) 0 Worker(s)",
    "B08202_015E": "3 Person(s) 1 Worker(s)",
    "B08202_016E": "3 Person(s) 2 Worker(s)",
    "B08202_017E": "3 Person(s) 3 Worker(s)",
    "B08202_019E": "4+ Person(s) 0 Worker(s)",
    "B08202_020E": "4+ Person(s) 1 Worker(s)",
    "B08202_021E": "4+ Person(s) 2 Worker(s)",
    "B08202_022E": "4+ Person(s) 3+ Worker(s)",
    "B08203_008E": "0 Worker(s) 0 Vehicle(s)",
    "B08203_009E": "0 Worker(s) 1 Vehicle(s)",
    "B08203_010E": "0 Worker(s) 2 Vehicle(s)",
    "B08203_011E": "0 Worker(s) 3 Vehicle(s)",
    "B08203_012E": "0 Worker(s) 4+ Vehicle(s)",
    "B08203_014E": "1 Worker(s) 0 Vehicle(s)",
    "B08203_015E": "1 Worker(s) 1 Vehicle(s)",
    "B08203_016E": "1 Worker(s) 2 Vehicle(s)",
    "B08203_017E": "1 Worker(s) 3 Vehicle(s)",
    "B08203_018E": "1 Worker(s) 4+ Vehicle(s)",
    "B08203_020E": "2 Worker(s) 0 Vehicle(s)",
    "B08203_021E": "2 Worker(s) 1 Vehicle(s)",
    "B08203_022E": "2 Worker(s) 2 Vehicle(s)",
    "B08203_023E": "2 Worker(s) 3 Vehicle(s)",
    "B08203_024E": "2 Worker(s) 4+ Vehicle(s)",
    "B08203_026E": "3+ Worker(s) 0 Vehicle(s)",
    "B08203_027E": "3+ Worker(s) 1 Vehicle(s)",
    "B08203_028E": "3+ Worker(s) 2 Vehicle(s)",
    "B08203_029E": "3+ Worker(s) 3 Vehicle(s)",
    "B08203_030E": "3+ Worker(s) 4+ Vehicle(s)",
    "B19019_002E": "Median Income for 1 Person(s)",
    "B19019_003E": "Median Income for 2 Person(s)",
    "B19019_004E": "Median Income for 3 Person(s)",
    "B19019_005E": "Median Income for 4 Person(s)",
    "B19019_006E": "Median Income for 5 Person(s)",
    "B19019_007E": "Median Income for 6 Person(s)",
    "B19019_008E": "Median Income for 7+ Person(s)"
}

households_key_list = [
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
    "B08201_002E",
    "B08201_003E",
    "B08201_004E",
    "B08201_005E",
    "B08201_006E",
    "B08201_007E",
    "B08201_008E",
    "B08201_009E",
    "B08201_010E",
    "B08201_011E",
    "B08201_012E",
    "B08201_013E",
    "B08201_014E",
    "B08201_015E",
    "B08201_016E",
    "B08201_017E",
    "B08201_018E",
    "B08201_019E",
    "B08201_020E",
    "B08201_021E",
    "B08201_022E",
    "B08201_023E",
    "B08201_024E",
    "B08201_025E",
    "B08201_026E",
    "B08201_027E",
    "B08201_028E",
    "B08201_029E",
    "B08201_030E",
    "B08202_002E",
    "B08202_003E",
    "B08202_004E",
    "B08202_005E",
    "B08202_007E",
    "B08202_008E",
    "B08202_010E",
    "B08202_011E",
    "B08202_012E",
    "B08202_014E",
    "B08202_015E",
    "B08202_016E",
    "B08202_017E",
    "B08202_019E",
    "B08202_020E",
    "B08202_021E",
    "B08202_022E",
    "B08203_008E",
    "B08203_009E",
    "B08203_010E",
    "B08203_011E",
    "B08203_012E",
    "B08203_014E",
    "B08203_015E",
    "B08203_016E",
    "B08203_017E",
    "B08203_018E",
    "B08203_020E",
    "B08203_021E",
    "B08203_022E",
    "B08203_023E",
    "B08203_024E",
    "B08203_026E",
    "B08203_027E",
    "B08203_028E",
    "B08203_029E",
    "B08203_030E",
    "B19019_002E",
    "B19019_003E",
    "B19019_004E",
    "B19019_005E",
    "B19019_006E",
    "B19019_007E",
    "B19019_008E"
]

household_values_list = list = [
    "total households in tract",
    "under 10k",
    "10k to 15k",
    "15k to 20k",
    "20k to 25k",
    "25k to 30k",
    "30k to 35k",
    "35k to 40k",
    "40k to 45k",
    "45k to 50k",
    "50k to 60k",
    "60k to 75k",
    "75k to 100k",
    "100k to 125k",
    "125k to 150k",
    "150k to 200k",
    "200k+",
    "0 Vehicle(s)",
    "1 Vehicle(s)",
    "2 Vehicle(s)",
    "3 Vehicle(s)",
    "4+ Vehicle(s)",
    "1 Person(s)",
    "1 Person(s) 0 Vehicle(s)",
    "1 Person(s) 1 Vehicle(s)",
    "1 Person(s) 2 Vehicle(s)",
    "1 Person(s) 3 Vehicle(s)",
    "1 Person(s) 4+ Vehicle(s)",
    "2 Person(s)",
    "2 Person(s) 0 Vehicle(s)",
    "2 Person(s) 1 Vehicle(s)",
    "2 Person(s) 2 Vehicle(s)",
    "2 Person(s) 3 Vehicle(s)",
    "2 Person(s) 4+ Vehicle(s)",
    "3 Person(s)",
    "3 Person(s) 0 Vehicle(s)",
    "3 Person(s) 1 Vehicle(s)",
    "3 Person(s) 2 Vehicle(s)",
    "3 Person(s) 3 Vehicle(s)",
    "3 Person(s) 4+ Vehicle(s)",
    "4+ Person(s)",
    "4+ Person(s) 0 Vehicle(s)",
    "4+ Person(s) 1 Vehicle(s)",
    "4+ Person(s) 2 Vehicle(s)",
    "4+ Person(s) 3 Vehicle(s)",
    "4+ Person(s) 4+ Vehicle(s)",
    "0 Worker(s)",
    "1 Worker(s)",
    "2 Worker(s)",
    "3+ Worker(s)",
    "1 Person(s) 0 Worker(s)",
    "1 Person(s) 1 Worker(s)",
    "2 Person(s) 0 Worker(s)",
    "2 Person(s) 1 Worker(s)",
    "2 Person(s) 2 Worker(s)",
    "3 Person(s) 0 Worker(s)",
    "3 Person(s) 1 Worker(s)",
    "3 Person(s) 2 Worker(s)",
    "3 Person(s) 3 Worker(s)",
    "4+ Person(s) 0 Worker(s)",
    "4+ Person(s) 1 Worker(s)",
    "4+ Person(s) 2 Worker(s)",
    "4+ Person(s) 3+ Worker(s)",
    "0 Worker(s) 0 Vehicle(s)",
    "0 Worker(s) 1 Vehicle(s)",
    "0 Worker(s) 2 Vehicle(s)",
    "0 Worker(s) 3 Vehicle(s)",
    "0 Worker(s) 4+ Vehicle(s)",
    "1 Worker(s) 0 Vehicle(s)",
    "1 Worker(s) 1 Vehicle(s)",
    "1 Worker(s) 2 Vehicle(s)",
    "1 Worker(s) 3 Vehicle(s)",
    "1 Worker(s) 4+ Vehicle(s)",
    "2 Worker(s) 0 Vehicle(s)",
    "2 Worker(s) 1 Vehicle(s)",
    "2 Worker(s) 2 Vehicle(s)",
    "2 Worker(s) 3 Vehicle(s)",
    "2 Worker(s) 4+ Vehicle(s)",
    "3+ Worker(s) 0 Vehicle(s)",
    "3+ Worker(s) 1 Vehicle(s)",
    "3+ Worker(s) 2 Vehicle(s)",
    "3+ Worker(s) 3 Vehicle(s)",
    "3+ Worker(s) 4+ Vehicle(s)",
    "Median Income for 1 Person(s)",
    "Median Income for 2 Person(s)",
    "Median Income for 3 Person(s)",
    "Median Income for 4 Person(s)",
    "Median Income for 5 Person(s)",
    "Median Income for 6 Person(s)",
    "Median Income for 7+ Person(s)"
]

#Read csvs into pandas dataframes
county_data = pd.DataFrame()
for count in range(int(len(households_key_list)/50)+1):
    variables = ""
    if ((count+1)*50) > len(households_key_list):
        variables = ",".join(households_key_list[(50*count):])
    elif count == 0:
        if (int(len(households_key_list)/50)+1) == 1:
            variables = ",".join(households_key_list[:])
        else:
            variables = ",".join(households_key_list[:(50*(count+1)-1)])
    else:
        variables = ",".join(households_key_list[(50*count):(50*(count+1)-1)])
    url = f"https://api.census.gov/data/{YEAR}/acs/acs5?get=NAME,{variables}&for=tract:*&in=state:{state_code}&in=county:{county_code}&key={APIKEY}"
    response = requests.request("GET", url)
    if len(county_data != 0):
        county_data = pd.merge(pd.DataFrame(response.json()[1:], columns=response.json()[0]), county_data, on='NAME', how='inner')
    else:
        county_data = pd.DataFrame(response.json()[1:], columns=response.json()[0])



# Load in tract data
tract_url = f"https://www2.census.gov/geo/tiger/TIGER{YEAR}/TRACT/tl_{YEAR}_{state_code}_tract.zip"
response = requests.request("GET", tract_url)
# Use BytesIO to handle the zip file in memory
with ZipFile(BytesIO(response.content)) as zip_ref:
    # Create a temporary directory to extract the zip file
    with tempfile.TemporaryDirectory() as tmpdirname:
        zip_ref.extractall(tmpdirname)
        
        # Find the shapefile or GeoJSON file in the extracted contents
        for root, dirs, files in os.walk(tmpdirname):
            for file in files:
                if file.endswith(".shp") or file.endswith(".geojson"):
                    file_path = os.path.join(root, file)
                    # Load the file into a GeoDataFrame
                    geodata = geopandas.read_file(file_path)


#Merge geographical dataframe (containing shapely ploygons) with census data
geodata.crs = 'EPSG:3857'
county_geodata = geodata[geodata['COUNTYFP'] == county_code]
county_geodata = county_geodata.rename(columns={"TRACTCE":"tract_y"})
county_geodata["tract_y"] = county_geodata["tract_y"].astype(int)
county_data["tract_y"] = county_data["tract_y"].astype(int)
data = pd.merge(county_geodata, county_data, on = "tract_y", how="inner")
data.rename(columns=households_variables_dict, inplace = True)
households = pd.DataFrame(columns = ["id","latitude","longitude","polygon","income"])

def swap_xy(x, y):
    return y, x

#Iterate through each tract
total_count = 0
for index,row in data.iterrows():
    if ((row['tract_y']>5000)&(row['tract_y']<6000)):
        tract_polygon = Polygon(row["geometry"])
        tract_polygon = transform(swap_xy, tract_polygon)
        project = pyproj.Transformer.from_proj(
            pyproj.Proj('epsg:4326'), # source coordinate system
            pyproj.Proj('epsg:3857')) # destination coordinate system
        tract_polygon = transform(project.transform, tract_polygon)  # apply 
        total_households = row["total households in tract"]
        if total_households == 0:
            continue
        weights = np.array(row["under 10k":"200k+"]).astype(int)
        
        polygons = []
        for household_num in range(int(tract_polygon.area/1000)):
            location = Point()
            polygon = Polygon()
            if (len(polygons) != 0):
                polygon = get_random_point(tract_polygon,polygons)
            else:
                location = tract_polygon.centroid
                polygon = Polygon(((location.x+10, location.y+10),(location.x-10, location.y+10),(location.x-10, location.y-10),(location.x+10, location.y-10)))
            location = polygon.centroid
            income = random.choices(household_values_list[1:17], weights, k=1)[0]
            households.loc[total_count] = {"id":total_count,"latitude":location.y,"longitude":location.x,"polygon":polygon,"income":income}
            total_count+=1
            polygons.append(polygon)

households.to_csv('households.csv', index=False)
print(households)