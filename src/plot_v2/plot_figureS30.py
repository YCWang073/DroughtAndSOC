"""Create Supplementary Figure S30: single-index versus partial-map correspondence."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_NAME = "FigureS30"
SCENARIOS = ("historical", "ssp126", "ssp245", "ssp370", "ssp585")
SCENARIO_LABELS = {"historical": "Historical", "ssp126": "SSP1-2.6", "ssp245": "SSP2-4.5", "ssp370": "SSP3-7.0", "ssp585": "SSP5-8.5"}
OUTCOMES = ("SOC", "RH")
INDICES = ("SPEI", "SSMI", "STI")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--robustness-csv", type=Path, default=PROJECT_ROOT / "src/review_check/res/review_check/drought_index_robustness/single_vs_partial_summary.csv")
    parser.add_argument("--output-dir", type=Path, default=PROJECT_ROOT / "res/eiar_figs")
    return parser.parse_args()


def configure_matplotlib() -> None:
    mpl.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"], "font.size": 7, "axes.linewidth": 0.7, "axes.spines.right": False, "axes.spines.top": False, "pdf.fonttype": 42, "svg.fonttype": "none"})


def plot_figureS30_panel(axis: plt.Axes, data: pd.DataFrame, outcome: str):
    subset = data.loc[data["outcome"].str.upper().eq(outcome)]
    matrix = subset.pivot(index="scenario", columns="index", values="spatial_spearman_single_vs_partial").reindex(index=SCENARIOS, columns=INDICES)
    image = axis.imshow(matrix.to_numpy(), vmin=0.2, vmax=0.7, cmap="Blues", aspect="auto")
    axis.set_title(outcome, loc="left", pad=4)
    axis.set_xticks(range(len(INDICES)), INDICES)
    axis.set_yticks(range(len(SCENARIOS)), [SCENARIO_LABELS[item] for item in SCENARIOS])
    for row in range(matrix.shape[0]):
        for column in range(matrix.shape[1]):
            value = matrix.iat[row, column]
            axis.text(column, row, f"{value:.2f}", ha="center", va="center", color="white" if value < 0.5 else "#272727", fontsize=7)
    axis.tick_params(length=0)
    return image


def plot_figureS30a(axis: plt.Axes, data: pd.DataFrame):
    return plot_figureS30_panel(axis, data, "SOC")


def plot_figureS30b(axis: plt.Axes, data: pd.DataFrame):
    return plot_figureS30_panel(axis, data, "RH")


def create_figureS30(robustness_csv: Path, output_dir: Path) -> None:
    """Create SOC and Rh correspondence heatmaps."""
    if not robustness_csv.is_file():
        raise FileNotFoundError(f"Missing single-index robustness summary: {robustness_csv}")
    configure_matplotlib()
    data = pd.read_csv(robustness_csv).loc[lambda frame: frame["region"].eq("global")].copy()
    figure = plt.figure(figsize=(7.2, 2.85), constrained_layout=True)
    grid = figure.add_gridspec(1, 3, width_ratios=(1, 1, 0.05))
    axes = (figure.add_subplot(grid[0, 0]), figure.add_subplot(grid[0, 1]))
    image = plot_figureS30a(axes[0], data)
    plot_figureS30b(axes[1], data)
    for label, axis in zip(("(a)", "(b)"), axes):
        axis.text(-0.13, 1.04, label, transform=axis.transAxes, fontweight="bold", fontsize=8, ha="left", va="bottom")
    colorbar = figure.colorbar(image, cax=figure.add_subplot(grid[0, 2]))
    colorbar.set_label("Spatial Spearman correlation")
    colorbar.ax.tick_params(length=2, width=0.6)
    output_dir.mkdir(parents=True, exist_ok=True)
    for extension in ("png", "pdf", "svg"):
        figure.savefig(output_dir / f"{OUTPUT_NAME}.{extension}", dpi=600, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    arguments = parse_args()
    create_figureS30(arguments.robustness_csv, arguments.output_dir)
