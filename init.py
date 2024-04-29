#file to define initialization of households and stores from CSVs
import csv
from stores import store
from households import BaseAgent, ERHC, ERLC, LRHC, LRLC

def initialize_stores_from_data(csv_filepath):
    """
    Initialize a list of Store objects from a CSV file
    """
    stores = []
    with open(csv_filepath, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row if it exists
        for idx, row in enumerate(reader, start=1):
            # Extract data from the row
            lon, lat, category, fsa =  row[:4]
            # Create a Store object and append it to the list
            stores.append(store(id=idx, category=category, lat=lat, lon=lon, fsa=fsa))
    return stores

#TODO: potential issue if houshold and store have same id?
def initialize_households_from_data(csv_filepath):
    """
    Initialize a list of household objects from a CSV file
    """
    agents = []
    with open(csv_filepath, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row if it exists
        for idx, row in enumerate(reader, start=1):
            # Extract data from the row
            lon, lat, hhinc8, owncar, category, salary = row[:6] #TODO: account for hhinc8, owncar, salary later?
            # Create a BaseAgent object and append it to the list
            if category == "ERHC":
                agents.append(ERHC(id=idx, household_type=category, lat=lat, lon=lon, mfai=0))
            elif category == "ERLC":
                agents.append(ERLC(id=idx, household_type=category, lat=lat, lon=lon, mfai=0))
            elif category == "LRHC":
                agents.append(LRHC(id=idx, household_type=category, lat=lat, lon=lon, mfai=0))
            elif category == "LRLC":
                agents.append(LRLC(id=idx, household_type=category, lat=lat, lon=lon, mfai=0))
            else:
                print("error appending household",idx, "no category specified") #error case
    return agents