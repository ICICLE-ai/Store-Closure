from data import stores, households #imports two pandas dataframes for household data and store data
from geo_model import GeoModel

#number of steps in the model
num_steps = 5
#intialize Mesa model with stores and household data
model = GeoModel(stores,households)
#Run model for given number of steps
for i in range(num_steps):
    model.step()