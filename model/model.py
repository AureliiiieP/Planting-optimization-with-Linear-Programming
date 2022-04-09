from pulp import LpProblem, LpVariable, LpMaximize, LpConstraint, LpStatus, lpSum
from pulp import const, value
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
        self.demand = self.parameters["demand"]
        self.plants = self.parameters["plants"]
        self.container = self.parameters["container"]
        self.grid = self.container.grid
        self.no_plants = len(self.plants)
        self.no_cell_x = self.container.no_x
        self.no_cell_y = self.container.no_y

        self.model = LpProblem(name="plant_opt", sense=LpMaximize)

        self.create_decision_variables()
        self.create_constraints()
        self.create_object_function()
        print("Create model for", self.no_plants, "seeds in", self.no_cell_x, "x", self.no_cell_y, "cells.")
    
    def generate_container_grid(self):
        pass

    def create_decision_variables(self):
        print("Create decision variables")
        # Allocation for seed i for each grid cell with coodinates (x, y)
        self.allocation = [
            [
                [
                    LpVariable(
                        f"seed_{i}_x_{x}_y_{y}",
                        lowBound=0,
                        cat=const.LpBinary,
                    )
                    for y in range(self.no_cell_y)
                ]
                for x in range(self.no_cell_x)
            ]
            for i in range(self.no_plants)
        ]

        self.happiness_plant = [
            LpVariable(
                f"happiness_plant_{i}",
                lowBound=0,
                cat=const.LpContinuous,
            )
            for i in range(self.no_plants)
        ]

    def create_constraints(self):
        print("Create constraints")
        # All demanded seeds must be placed somewhere in the container
        self.placed_seed_constraint = {
            f"placed_seed_constraint{i}": self.model.addConstraint(
                LpConstraint(
                    e=lpSum(
                        self.allocation[i][x][y] for x in range(self.no_cell_x) for y in range(self.no_cell_y)
                    ),
                    sense=const.LpConstraintEQ,
                    name=f"placed_seed_constraint{i}",
                    rhs=1,
                ),
            )
            for i in range(self.no_plants)
        }

        # Only one seed maximum per cell
        self.cell_allocation_flag_constraint = {
            f"cell_allocation_flag_{x}_{y}": self.model.addConstraint(
                LpConstraint(
                    e=lpSum(
                        self.allocation[i][x][y] for i in range(self.no_plants)
                    ),
                    sense=const.LpConstraintLE,
                    name=f"cell_allocation_flag_{x}_{y}",
                    rhs=1,
                ),
            )
            for x in range(self.no_cell_x)
            for y in range(self.no_cell_y)
        }

        # Happiness per plant
        self.happiness_plant_constraint = {
            f"happiness_plant_{i}": self.model.addConstraint(
                LpConstraint(
                    e=self.happiness_plant[i],
                    sense=const.LpConstraintEQ,
                    name=f"happiness_plant_{i}",
                    rhs=1,
                ),
            )
            for i in range(self.no_plants)
        }

    def create_object_function(self):
        print("Create objective function")
        # A plant is happy if space needed is respected
        # 1 if space_available >= space_needed. space_available/space_needed otherwise.
        #self.total_plant_happiness
        self.total_happiness = lpSum(self.happiness_plant[i] for i in range(self.no_plants))
        objective = self.total_happiness
        self.model.setObjective(objective)
    
    def optimize(self):
        solver = PULP_CBC_CMD(
            mip=1,
            msg=1,
            threads=1,
            gapRel=self.config["solver"]["gap_tolerance"],
        )
        self.model.solve(solver=solver)
        print(f"LpStatus : {LpStatus[self.model.status]}")
        print(f"Objective: {value(self.model.objective)}")
    
    def generate_output_grid(self):
        grid = [[[] for x in range(self.no_cell_x)] for y in range(self.no_cell_y)]
        for x in range(self.no_cell_x) :
            for y in range(self.no_cell_y):
                for i in range(self.no_plants):
                    if self.allocation[i][x][y].varValue != 0.0 :
                        grid[y][x] = self.plants[i].name
        return grid

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
    return model



