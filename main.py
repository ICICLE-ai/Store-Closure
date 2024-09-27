import itertools
from mesa.datacollection import DataCollector
from mesa import Agent, Model
from mesa.time import BaseScheduler
from mesa.space import MultiGrid
from mesa_geo.geoagent import GeoAgent, AgentCreator
from mesa_geo import GeoSpace
import random
import numpy as np
import sys
#import matplotlib.pyplot as plt
import requests
from shapely.geometry import Polygon
from data import erhc_values,erlc_values,lrhc_values,lrlc_values,spm_values,cspm_values,erhc_data,erlc_data,lrhc_data,lrlc_data,spm_data,cspm_data
from agent import erhc,erlc,lrhc,lrlc,spm,cspm
from shapely.geometry import Polygon
import time
import logging
global h
h=0
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#log messages to terminal in above format
class ABM(Model):
    Map_coordinates = [39.9612, -82.9988]
    def __init__(self):
        logging.info("starting") #use logging as opposed to print statements to ensure display in terminal
        start_time = time.time()
        global h
        self.schedule = BaseScheduler(self)
        self.grid = GeoSpace()
        self.running = True
        
        ERHC = AgentCreator(erhc, {"model": self, "fa": 0,'fsa_sum':0})
        agents_erhc = ERHC.from_GeoDataFrame(erhc_values, unique_id="id")
        for agent in agents_erhc:
            
            self.grid.add_agents(agent)
            
            self.schedule.add(agent)
                #print(agent.latitude," ",agent.longitude)

        ERLC = AgentCreator(erlc, {"model": self, "fa": 0,'fsa_sum':0})
        agents_erlc = ERLC.from_GeoDataFrame(erlc_values,unique_id="id",set_attributes=True)
        for agent in agents_erlc:
            self.grid.add_agents(agent)
            self.schedule.add(agent)


        LRHC = AgentCreator(lrhc, {"model": self, "fa": 0,'fsa_sum':0})
        agents_lrhc = LRHC.from_GeoDataFrame(lrhc_values,unique_id="id")
        for agent in agents_lrhc:
            self.grid.add_agents(agent)
            self.schedule.add(agent)

        LRLC = AgentCreator(lrlc, {"model": self, "fa": 0,'fsa_sum':0})
        agents_lrlc = LRLC.from_GeoDataFrame(lrlc_values,unique_id="id")
        for agent in agents_lrlc:
            self.grid.add_agents(agent)
            self.schedule.add(agent)


        SPM = AgentCreator(spm, {"model": self, "fa": 55})
        agents_spm = SPM.from_GeoDataFrame(spm_values,unique_id="id")
        i=0
        for agent in agents_spm:
            self.grid.add_agents(agents_spm)
            self.schedule.add(agent)

        CSPM = AgentCreator(cspm, {"model": self, "fa": 55})
        agents_cspm = CSPM.from_GeoDataFrame(cspm_values,unique_id="id")
        for agent in agents_cspm:
            self.grid.add_agents(agent)
            self.schedule.add(agent)

        self.datacollector = DataCollector({"ERHC_FA": lambda m: m.get_total_fa(erhc),
                                            "ERLC_FA": lambda m: m.get_total_fa(erlc),
                                            "LRHC_FA": lambda m: m.get_total_fa(lrhc),
                                            "LRLC_FA": lambda m: m.get_total_fa(lrlc)})
        end_time = time.time()
        init_time = end_time - start_time
        logging.info(f"Init time: {init_time:.6f} seconds")
        #q = self.datacollector.get_model_vars_dataframe()
        #q.to_csv("data.csv")

    def step(self):
        start_time = time.time()
        self.schedule.step()
        self.datacollector.collect(self)
        q = self.datacollector.get_model_vars_dataframe()
        q.to_csv("data.csv")
        end_time = time.time()
        step_time = end_time - start_time
        logging.info(f"Step time: {step_time:.6f} seconds")
        


    def get_total_fa(self, agent_type, total_fa=0):
        #agent_fa = [agent.fa for agent in agent_type]

        #total_fa = sum(agent_fa)
        for agent in self.schedule.agents:
            if isinstance(agent, agent_type):
                total_fa += agent.fa

        return total_fa


