from pulp import LpProblem, LpVariable, LpMinimize, LpConstraint
from pulp import PULP_CBC_CMD
from model.garden_processing import Plant, ContainerGrid
from model.demand_processing import PlantDemand
from copy import deepcopy

class OptModel(object):
    def __init__(
        self,
        config: dict,
        parameters: dict
    ):
        self.config = deepcopy(config)
        self.parameters = deepcopy(parameters)
        self.plants = self.parameters["plants"]
        self.container = self.parameters["container"]
        self.grid = self.container.grid
        self.no_plants = len(self.plants)
        self.no_cell_x = self.container.no_x
        self.no_cell_y = self.container.no_y

        self.model = LpProblem(name="plant_opt", sense=LpMinimize)

        self.create_decision_variables()
        self.create_constraints()
        self.create_object_function()

        

    def generate_container_grid(self):
        pass

    def create_decision_variables(self):
        # Allocation for seed i for each grid cell with coodinates (x, y)
        self.allocation = [
            [
                [
                    LpVariable(
                        f"seed_{i}_x_{x}_y_{y}",
                        lowBound=0,
                        cat=const.LpBinary,
                    )
                    for x in range(self.no_cell_x)
                ]
                for y in range(self.no_cell_y)
            ]
        ]
        pass

    def create_constraints(self):
        # Quantity placed in container match demand quantity for each type of seed i
        # Only one seed per cell
        pass

    def create_object_function(self):
        # A plant is happy if space needed is respected
        # 1 if space_available >= space_needed. space_available/space_needed otherwise.
        #self.total_plant_happiness
        pass
    
    def optimize(self):
        solver = PULP_CBC_CMD(
            mip=1,
            msg=1,
            threads=1,
            gapRel=self.params["gap_tolerance"],
        )

def generate_model_parameters(config, plant_demand_df):
    print("Generate model parameters")
    plants = Plant.read_from_demand(plant_demand_df)
    demand = PlantDemand.calculate_demand_per_plant(plant_demand_df, plants)
    space_wanted = Plant.get_size_per_plant(plant_demand_df, plants)
    container_size = config["container_size"]
    container = ContainerGrid(length=container_size["length"], width=container_size["width"], cell_size = config["cell_size"])

    parameters = {
        "container_size" : container_size,
        "demand" : demand,
        "space_wanted" : space_wanted,
        "plants" : plants,
        "container" : container
    }
    return parameters

def build_model(config, parameters):
    print("Build model")
    model = OptModel(config=config, parameters=parameters)
    pass



