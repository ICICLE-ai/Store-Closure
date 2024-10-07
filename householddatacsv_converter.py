#This file converts household testing data to the old file format 
import pandas as pd
from shapely import wkt
from pyproj import Transformer

# Step 1: Read the input CSV
input_csv = pd.read_csv('./Benchmarking_datasets/testing_data_columbus.csv')

# Function to extract the centroid (longitude, latitude) from a location string (assumed WKT format)
def extract_centroid(location_wkt):
    # Convert the WKT string to a shapely Polygon object
    polygon = wkt.loads(location_wkt)
    centroid = polygon.centroid
    return centroid.x, centroid.y  # longitude, latitude

# Function to convert income to hhinc8 (household income in 8 brackets)
def convert_income_to_hhinc8(income):
    # Example income brackets mapping (you can adjust based on your requirements)
    if income < 20000:
        return 1
    elif income < 40000:
        return 2
    elif income < 60000:
        return 3
    elif income < 80000:
        return 4
    elif income < 100000:
        return 5
    elif income < 120000:
        return 6
    elif income < 140000:
        return 7
    else:
        return 8

# Function to convert vehicles to owncar (binary 0/1)
def convert_vehicles_to_owncar(vehicles):
    return 1 if vehicles > 0 else 0

# Step 2: Apply transformations to each row
output_data = []
transformer = Transformer.from_crs(3857, 4326)
for index, row in input_csv.iterrows():
    location_wkt = row['location']  # Assuming the location is in WKT format
    income = row['income']
    vehicles = row['vehicles']
    
    # Extract longitude and latitude from the location (WKT polygon)
    longitude, latitude = extract_centroid(location_wkt)
    longitude, latitude = transformer.transform(longitude, latitude)
    # Convert income to hhinc8
    hhinc8 = convert_income_to_hhinc8(income)
    
    # Convert vehicles to owncar
    owncar = convert_vehicles_to_owncar(vehicles)
    
    # Set a default category (adjust as needed)
    category = "default_category"
    if hhinc8 > 3:
        if vehicles > 0:
            category = "ERHC"
        else:
            category = "ERLC"
    else:
        if vehicles > 0:
            category = "LRHC"
        else:
            category = "LRLC"
    
    # Set a default salary (or map this from income if needed)
    salary = income  # You can map this separately if required

    # Append transformed data in the new order: longitude, latitude, hhinc8, owncar, category, salary
    output_data.append([longitude, latitude, hhinc8, owncar, category, salary])

# Step 3: Create a new DataFrame with the new format
output_df = pd.DataFrame(output_data, columns=['longitude', 'latitude', 'hhinc8', 'owncar', 'category', 'salary'])

# Step 4: Write the output DataFrame to a new CSV
output_df.to_csv('output_file_house.csv', index=False)

print("Converted")
