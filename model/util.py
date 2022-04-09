import matplotlib.pyplot as plt

def draw_grid(config, grid):
    fig, ax = plt.subplots()

    # Hide axes
    ax.xaxis.set_visible(False) 
    ax.yaxis.set_visible(False)

    # Table from Ed Smith answer
    ax.table(cellText=grid,loc='center')

    plt.savefig(config["paths"]["output"]["grid_result"],
            bbox_inches='tight',
            dpi=300
            )