from init import initialize_households_from_data, initialize_stores_from_data

csv_stores_file_path = 'data/marketdata.csv'
csv_households_file_path = 'data/homedata.csv'

stores = initialize_stores_from_data(csv_stores_file_path)
households = initialize_households_from_data(csv_stores_file_path)

first_store = stores[0]
print("Store Information:")
print("ID:", first_store.id)
print("Category:", first_store.category)
print("Latitude:", first_store.lat)
print("Longitude:", first_store.lon)
print("FSA:", first_store.FSA)

