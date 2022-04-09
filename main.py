import os
import yaml
import numpy as np
import pandas as pd
from model.model import generate_model_parameters, build_model
from model.demand_processing import PlantDemand

def optimization():
    config = yaml.load(open("config.yml"), Loader=yaml.FullLoader)
    
    ###################################
    # Data preprocessing
    ###################################
    # Prepare seed to plant demand 
    plant_demand = PlantDemand(config)
    plant_demand_df = plant_demand.generate_demand()
    # Save to intermediate file
    demand_output_path = config["paths"]["intermediate"]["demand"]
    plant_demand_df.to_excel(demand_output_path)

    ###################################
    # Optimization model
    ###################################
    generate_model_parameters(config, plant_demand_df)
    build_model(config)
    pass

if __name__ == "__main__":
    optimization()