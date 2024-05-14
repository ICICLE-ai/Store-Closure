import pandas as pd

csv_stores_file_path = "data/marketdata.csv"
csv_households_file_path = "data/homedata.csv"

households = pd.read_csv(csv_households_file_path)
stores = pd.read_csv(csv_stores_file_path)