"""Module for main function that runs the algorithm."""
from init import initialize_households_from_data, initialize_stores_from_data

"""import api key from config.py file, please make your own config.py and use your api key"""
from config import api_key

"""This calls the census api to get data (written by charlie)"""
import census ##UNUSED RIGHT NOW

csv_stores_file_path = "data/marketdata.csv"
csv_households_file_path = "data/homedata.csv"

stores = initialize_stores_from_data(csv_stores_file_path)
households = initialize_households_from_data(csv_households_file_path)

#Adjust the steps and num agents to run below for testing:
steps = 5
num_agents_to_run = 10
for i in range(steps):
    for agent in households[:num_agents_to_run]:
        #print("On step", i+1, "with agent", agent.id)
        agent.step(stores)
        print("---", agent.household_type,"household", agent.house_id,"has a MFAI score of", agent.mfai, "at week", i+1,"---")
    print()

#print first store for debugging
first_store = stores[0]
print("Store Information:")
print("ID:", first_store.store_id)
print("Category:", first_store.category)
print("Latitude:", first_store.lat)
print("Longitude:", first_store.lon)
print("FSA:", first_store.fsa)

