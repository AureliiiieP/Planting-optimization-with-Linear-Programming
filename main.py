import yaml
import pandas as pd
from model.model import generate_model_parameters, build_model
from model.demand_processing import PlantDemand
from model.util import draw_grid

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
    parameters = generate_model_parameters(config, plant_demand_df)
    model = build_model(config, parameters)
    model.optimize()
    if model.model.status == 1:
        grid_output = model.generate_output_grid()
        draw_grid(config, grid_output)
        print(grid_output)

if __name__ == "__main__":
    optimization()