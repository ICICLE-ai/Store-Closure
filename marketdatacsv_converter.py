#This file converts market testing data to the old file format 
import pandas as pd
from shapely import wkt
from shapely.geometry import Polygon
from pyproj import Transformer

input_csv = pd.read_csv('input_file.csv')
#print(input_csv.columns)

def extract_centroid(polygon_wkt):
    polygon = wkt.loads(polygon_wkt)
    centroid = polygon.centroid
    return centroid.x, centroid.y

def abbreviate_category(category):
    if category.lower() == "supermarket":
        return "SPM"
    elif category.lower() == "convenience":
        return "CSPM"
    else:
        return "unknown"

output_data = []
transformer = Transformer.from_crs(3857, 4326)
for index, row in input_csv.iterrows():
    #print(f"Row polygon data: {row['polygon']}")
    category = row['category']
    polygon = row['polygon']  
    
    # Extract longitude and latitude from the centroid of the polygon
    longitude, latitude = extract_centroid(polygon)
    longitude, latitude = transformer.transform(longitude, latitude)
    # Default score value
    FSA = 90 if category == "supermarket" else 50
    category_abbr = abbreviate_category(category)
    print(category_abbr)
    # Append transformed data in the new order: longitude, latitude, category, score
    output_data.append([longitude, latitude, category_abbr, FSA])

output_df = pd.DataFrame(output_data, columns=['longitude', 'latitude', 'category', 'FSA'])

output_df.to_csv('output_file_market.csv', index=False)

print("Converted")
