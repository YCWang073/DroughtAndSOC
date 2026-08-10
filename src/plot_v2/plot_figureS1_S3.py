"""Create manuscript Supplementary Figures S1 and S3.

Figure S1 shows continent-specific distance matrices for heterotrophic
respiration flux; Figure S3 shows the corresponding matrices for soil carbon
stock.  The source CSV files use ``obs`` as the benchmark identifier, which is
displayed in the figures as ``Benchmark``.
"""

import os

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import gridspec
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize


OUTPUT_DIR = "res/eiar_figs"
MODEL_INPUT_PATH = "/run/media/yue/Elements SE/007-2_MMWM_data_CMIP6"

CSV_MODEL_NAMES = [
    "CMCC-ESM2",
    "CESM2-WACCM",
    "NorESM2-MM",
    "TaiESM1",
    "EC-Earth3-Veg",
    "CMCC-CM2-SR5",
    "BCC-CSM2-MR",
    "obs",
]
DISPLAY_MODEL_NAMES = [*CSV_MODEL_NAMES[:-1], "Benchmark"]

CONTINENT_DICT = {
    "Asia": 0,
    "North America": 1,
    "Europe": 2,
    "Africa": 3,
    "South America": 4,
    "Oceania": 5,
}


def plot_figure_s1_panel(ax, variable, continent):
    """Plot one continent's model-distance matrix."""
    weight_path = os.path.join(
        MODEL_INPUT_PATH, f"{continent}_{variable}_distance_matrix.csv"
    )
    distance_matrix = pd.read_csv(weight_path, index_col=0)
    distance_matrix = distance_matrix.loc[CSV_MODEL_NAMES, CSV_MODEL_NAMES]

    norm = Normalize(vmin=0, vmax=2.2)
    matrix_values = distance_matrix.to_numpy()
    model_count = len(CSV_MODEL_NAMES)

    for row in range(model_count):
        for column in range(model_count):
            value = matrix_values[row, column]
            text_colour = "black" if value < 1.5 else "white"
            ax.add_patch(
                patches.Rectangle(
                    (column, row),
                    1,
                    1,
                    linewidth=1,
                    edgecolor="gray",
                    facecolor=plt.cm.YlGnBu(norm(value)),
                    alpha=0.8,
                )
            )
            ax.text(
                column + 0.5,
                row + 0.5,
                f"{value:.3f}",
                ha="center",
                va="center",
                fontsize=15,
                color=text_colour,
            )

    ax.set_xticks(np.arange(model_count) + 0.5)
    ax.set_yticks(np.arange(model_count) + 0.5)
    if continent in {"South America", "Oceania"}:
        ax.set_xticklabels(DISPLAY_MODEL_NAMES, rotation=45, ha="right", fontsize=18)
    else:
        ax.set_xticklabels([])

    if continent in {"South America", "Asia", "Europe"}:
        ax.set_yticklabels(DISPLAY_MODEL_NAMES, fontsize=18)
    else:
        ax.set_yticklabels([])

    title = "Australia" if continent == "Oceania" else continent
    ax.set_title(title, fontsize=20)

    ax.set_xticks(np.arange(model_count + 1), minor=True)
    ax.set_yticks(np.arange(model_count + 1), minor=True)
    ax.grid(which="minor", color="gray", linestyle="-", linewidth=1)
    ax.set_xlim(0, model_count)
    ax.set_ylim(0, model_count)
    ax.invert_yaxis()
    ax.tick_params(axis="x", labelsize=16)
    ax.tick_params(axis="y", labelsize=16)


def create_distance_matrix_figure(variable, title, filename, colourbar_max):
    """Create and save one complete, six-panel distance-matrix figure."""
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Arial"],
            "font.sans-serif": ["Times New Roman"],
        }
    )
    fig = plt.figure(figsize=(15, 20))
    grid = gridspec.GridSpec(3, 2, figure=fig)

    for continent, index in CONTINENT_DICT.items():
        axis = fig.add_subplot(grid[index])
        plot_figure_s1_panel(axis, variable, continent)

    fig.subplots_adjust(wspace=0.15, hspace=0.15, bottom=0.2)
    fig.suptitle(title, fontsize=22, fontweight="bold", y=0.92)

    colourbar_axis = fig.add_axes([0.15, 0.10, 0.7, 0.015])
    scalar_map = ScalarMappable(
        cmap=plt.cm.YlGnBu, norm=Normalize(vmin=0, vmax=colourbar_max)
    )
    scalar_map.set_array([])
    colourbar = fig.colorbar(
        scalar_map, cax=colourbar_axis, orientation="horizontal", extend="both"
    )
    colourbar.set_label("Distance", fontsize=20)
    colourbar.ax.tick_params(labelsize=16)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for extension in ("png", "pdf"):
        fig.savefig(
            os.path.join(OUTPUT_DIR, f"{filename}.{extension}"),
            dpi=600,
            bbox_inches="tight",
        )
    plt.close(fig)


def create_figure_s1():
    """Create manuscript Figure S1: heterotrophic-respiration distance matrices."""
    create_distance_matrix_figure(
        variable="rh",
        title="Distance Matrix of Heterotrophic Respiration Flux",
        filename="FigureS1",
        colourbar_max=2.0,
    )


def create_figure_s3():
    """Create manuscript Figure S3: soil-carbon-stock distance matrices."""
    create_distance_matrix_figure(
        variable="soc",
        title="Distance Matrix of Soil Carbon Stock",
        filename="FigureS3",
        colourbar_max=2.2,
    )


if __name__ == "__main__":
    create_figure_s1()
    create_figure_s3()
