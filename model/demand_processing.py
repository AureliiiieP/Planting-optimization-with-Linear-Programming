import pandas as pd
from copy import deepcopy

class PlantDemand:
    def __init__(self, config: dict):
        self.config = deepcopy(config)
    
    def generate_demand(self):
        # Read quantity from config file
        quantity_dict = dict(self.config["seed_quantity"])
        quantity_df = pd.DataFrame.from_dict(quantity_dict, orient="index", columns = ["quantity"]).reset_index()
        quantity_df = quantity_df.rename(columns = {'index':'name'})
        # Read plants specs from plant master
        plant_master_df = pd.read_excel(self.config["paths"]["raw"]["plant_master"], engine = 'openpyxl') # pandas uses xlrd by default. xlrd removed support for xlsx files.
        # Get demand for each plant
        self.demand = pd.merge(quantity_df, plant_master_df, on="name")
        return self.demand
    
    @staticmethod
    def calculate_demand_per_plant(plant_demand_df, plants) :
        quantity_demand = plant_demand_df.set_index("name").to_dict()["quantity"]
        demand = []
        for plant in plants:
            if plant.name in quantity_demand:
                demand.append(quantity_demand[plant.name])
            else :
                demand.append(0)
        return demand

