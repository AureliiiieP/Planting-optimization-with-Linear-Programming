from model.garden_processing import Plant

def generate_model_parameters(config, plant_demand_df):
    print("Generate model parameters")
    plants = Plant.read_from_demand(plant_demand_df)
    print(plants)
    pass

def build_model(config):
    print("Build model")
    pass

