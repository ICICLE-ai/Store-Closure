import pandas as pd

#Loads household and store data from csv files
csv_stores_file_path = "data/marketdata.csv"
csv_households_file_path = "data/homedata.csv"

#Stores data in variables. This data is imported by run.py
#and used to intialize the GeoModel
households = pd.read_csv(csv_households_file_path)
stores = pd.read_csv(csv_stores_file_path)