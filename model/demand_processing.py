import pandas as pd
from copy import deepcopy
from model.garden_manager import Plant, Container

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
    def get_plants_from_demand(demand_df):
        plants = []
        for _, row in demand_df.iterrows():
            for quantity in range(row["quantity"]) :
                name = row["name"]
                depth_needed = row["depth_needed"]
                capacity_needed = row["capacity_needed"]
                plant = Plant(
                    name=name,
                    depth_needed = depth_needed,
                    capacity_needed = capacity_needed
                )
                plants.append(plant)
        return plants

    @staticmethod
    def get_needed_capacity_per_plant(plant_demand_df, plants) :
        """Returns the necessary amount of soil to provide enough nutrients to the plant (in liters)
        """
        space_demand = plant_demand_df.set_index("name").to_dict()["capacity_needed"]
        demand = []
        for plant in plants:
            if plant.name in space_demand:
                demand.append(space_demand[plant.name])
            else :
                demand.append(0)
        return demand

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


class ContainerManager:
    def __init__(self, config: dict):
        self.config = deepcopy(config)
    
    def generate_available_containers(self):
        container_master_df = pd.read_excel(self.config["paths"]["raw"]["container_master"], engine = 'openpyxl')
        quantity_dict = dict(self.config["container_quantity"])
        containers = []
        for _, row in container_master_df.iterrows():
            name = row["name"]
            quantity = quantity_dict[name]
            for i in range(quantity) :                
                capacity = row["capacity"]
                depth = row["depth"]
                container = Container(
                    name=name,
                    capacity = capacity,
                    depth = depth
                )
                containers.append(container)
        return containers

    @staticmethod
    def generate_suitable_parameters(plants, containers):
        parameters = []
        for container in containers :
            container_parameters = []
            for plant in plants :
                container_parameters.append(container.is_suitable(plant))
            parameters.append(container_parameters)
        return parameters
    
    def generate_max_capacity(containers) :
        parameters = []
        for container in containers :
            parameters.append(container.capacity)
        return parameters
