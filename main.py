import yaml
import pandas as pd
from model.model import generate_model_parameters, build_model
from model.demand_processing import PlantDemand, ContainerManager

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

    # Prepare available containers
    container_manager = ContainerManager(config)
    containers = container_manager.generate_available_containers()

    ###################################
    # Optimization model
    ###################################
    parameters = generate_model_parameters(config, plant_demand_df, containers)
    model = build_model(config, parameters)
    model.optimize()
    if model.model.status == 1:
        #model.show_result_plan_by_plant()
        model.show_result_plan_by_container()

if __name__ == "__main__":
    optimization()