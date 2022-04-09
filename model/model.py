import numpy as np
from pulp import LpProblem, LpVariable, LpMinimize, LpConstraint, LpStatus, lpSum
from pulp import const, value
from pulp import PULP_CBC_CMD
from model.garden_manager import Plant, Container
from model.demand_processing import PlantDemand, ContainerManager
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
        self.soil_capacity_wanted = self.parameters["soil_capacity_wanted"]
        self.containers = self.parameters["containers"]
        self.containers_capacity = self.parameters["containers_capacity"]
        self.is_suitable = self.parameters["is_suitable"]
        self.no_plants = len(self.plants)
        self.no_containers = len(self.containers)

        self.model = LpProblem(name="plant_opt", sense=LpMinimize)

        self.create_decision_variables()
        self.create_constraints()
        self.create_objective_function()
        print("Create model for", self.no_plants, "plants in", self.no_containers, "containers.")



    def create_decision_variables(self):
        print("Create decision variables")
        # Allocation of plant p for container c
        self.allocation_flag = [
            [
                LpVariable(
                    f"plant_{c}_{p}",
                    lowBound=0,
                    cat=const.LpBinary,
                )
                for p in range(self.no_plants)
            ]
            for c in range(self.no_containers)
        ]

        # Allocated capacity of plant p for container c
        self.allocation_capacity = [
            [
                LpVariable(
                    f"plant_capacity_{c}_{p}",
                    lowBound=0,
                    cat=const.LpContinuous,
                )
                for p in range(self.no_plants)
            ]
            for c in range(self.no_containers)
        ]

        # Whether container is used
        self.container_allocation_flag = [
            LpVariable(
                f"container_{c}",
                lowBound=0,
                cat=const.LpBinary,
            )
            for c in range(self.no_containers)
        ]

    def create_constraints(self):
        print("Create constraints")

        # Each plant must be planted
        self.plant_allocation_constraint = {
            f"plant_allocation_constraint_{p}": self.model.addConstraint(
                LpConstraint(
                    e=lpSum(
                        self.allocation_flag[c][p] for c in range(self.no_containers)
                    ),
                    sense=const.LpConstraintEQ,
                    name=f"plant_allocation_constraint_{p}",
                    rhs=1,
                ),
            )
            for p in range(self.no_plants)
        }

        # Each plant capacity must be respected
        self.allocated_plant_capacity_constraint = {
            f"allocated_plant_capacity_constraint_{p}": self.model.addConstraint(
                LpConstraint(
                    e=lpSum(
                        self.allocation_capacity[c][p] for c in range(self.no_containers)
                    ),
                    sense=const.LpConstraintEQ,
                    name=f"allocated_plant_capacity_constraint_{p}",
                    rhs=self.soil_capacity_wanted[p],
                ),
            )
            for p in range(self.no_plants)
        }

        # Capacity of each container must be respected
        self.container_capacity_constraint = {
            f"container_capacity_{c}": self.model.addConstraint(
                LpConstraint(
                    e=lpSum(
                        self.allocation_capacity[c][p] for p in range(self.no_plants)
                    ),
                    sense=const.LpConstraintLE,
                    name=f"container_capacity_{c}",
                    rhs=self.containers_capacity[c],
                ),
            )
            for c in range(self.no_containers)
        }
        self.container_capacity_constraint = {
            f"container_capacity_bis_{c}": self.model.addConstraint(
                LpConstraint(
                    e=lpSum(
                        self.allocation_flag[c][p]*self.soil_capacity_wanted[p] for p in range(self.no_plants)
                    ),
                    sense=const.LpConstraintLE,
                    name=f"container_capacity_bis_{c}",
                    rhs=self.containers_capacity[c],
                ),
            )
            for c in range(self.no_containers)
        }
        

        # Whether container is used
        self.container_allocation_constraint = {
            f"container_allocation_constraint_{c}": self.model.addConstraint(
                LpConstraint(
                    e= self.container_allocation_flag[c]
                    - lpSum(
                        self.allocation_flag[c][p] for p in range(self.no_plants)
                    ),
                    sense=const.LpConstraintLE,
                    name=f"container_allocation_constraint_{c}",
                    rhs=0,
                ),
            )
            for c in range(self.no_containers)
        }

        self.suitable_container_constraint = {
            f"suitable_container": self.model.addConstraint(
                LpConstraint(
                    e=lpSum(
                        self.allocation_flag[c][p]
                        * (1-self.is_suitable[c][p])
                        for c in range(self.no_containers)
                        for p in range(self.no_plants)
                    ),
                    sense=const.LpConstraintEQ,
                    rhs=0,
                    name=f"suitable_container",
                ),
            )
        }

    def create_objective_function(self):
        print("Create objective function")
        # Number of containers used
        self.allocation_count = lpSum(self.container_allocation_flag[c]
        for c in range(self.no_containers))

        # Liters used (containers fully filled with soil even for one small plant)
        self.model.setObjective(self.allocation_count)

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

    def show_result_plan_by_plant(self):
        for c in range(self.no_containers):
            for p in range(self.no_plants):
                if self.allocation_flag[c][p].varValue != 0 :
                    print(self.plants[p].name, self.containers[c].name)

    def show_result_plan_by_container(self):
        for c in range(self.no_containers):
            container_result = []
            total_used = 0
            for p in range(self.no_plants):
                if self.allocation_flag[c][p].varValue != 0 :
                    container_result.append((self.plants[p].name, self.plants[p].capacity_needed))
                    total_used += self.plants[p].capacity_needed
            if container_result != []:
                print("=========================")
                print("Plan for :", self.containers[c].name)
                print("Using :", total_used, "/", self.containers[c].capacity, "L of soil")
                print(container_result)

        # For debug
        #for c in range(self.no_containers):
        #    for p in range(self.no_plants):
        #        if self.allocation_capacity[c][p].varValue != 0.0 :
        #            print(c, p, self.plants[p].name, self.allocation_flag[c][p].varValue, self.plants[p].capacity_needed, self.allocation_capacity[c][p].varValue, self.soil_capacity_wanted[p])


def generate_model_parameters(config, plant_demand_df, containers):
    print("Generate model parameters")
    # Demand
    plants = PlantDemand.get_plants_from_demand(plant_demand_df)
    soil_capacity_wanted = PlantDemand.get_needed_capacity_per_plant(plant_demand_df, plants)
    demand = PlantDemand.calculate_demand_per_plant(plant_demand_df, plants)
    is_suitable = ContainerManager.generate_suitable_parameters(plants, containers)
    containers_capacity = ContainerManager.generate_max_capacity(containers)

    parameters = {
        "soil_capacity_wanted" : soil_capacity_wanted,
        "plants" : plants,
        "containers" : containers,
        "containers_capacity" : containers_capacity,
        "is_suitable" : is_suitable
    }
    return parameters

def build_model(config, parameters):
    print("Build model")
    model = OptModel(config=config, parameters=parameters)
    return model


