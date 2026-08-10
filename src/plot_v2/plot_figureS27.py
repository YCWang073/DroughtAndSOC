"""Create Supplementary Figure S27: signed selected partial-Spearman distributions."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_NAME = "FigureS27"
SCENARIOS = ("historical", "ssp126", "ssp245", "ssp370", "ssp585")
SCENARIO_LABELS = {
    "historical": "Historical\n(1985–2014)",
    "ssp126": "SSP1-2.6\n(2070–2099)",
    "ssp245": "SSP2-4.5\n(2070–2099)",
    "ssp370": "SSP3-7.0\n(2070–2099)",
    "ssp585": "SSP5-8.5\n(2070–2099)",
}
OUTCOMES = ("soc", "rh")
OUTCOME_LABELS = {"soc": "SOC", "rh": "Rh"}
INDICES = ("SPEI", "SSMI", "STI")
INDEX_COLORS = {"SPEI": "#4C78A8", "SSMI": "#8C6BB1", "STI": "#C98B36"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-root",
        type=Path,
        default=Path("/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6"),
        help="Root containing archived selected-sensitivity NetCDF files.",
    )
    parser.add_argument("--output-dir", type=Path, default=PROJECT_ROOT / "res/eiar_figs")
    return parser.parse_args()


def configure_matplotlib() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "font.size": 7,
            "axes.linewidth": 0.8,
            "axes.spines.right": False,
            "axes.spines.top": False,
            "pdf.fonttype": 42,
            "svg.fonttype": "none",
        }
    )


def load_coefficients(data_root: Path, outcome: str, index: str, scenario: str) -> np.ndarray:
    path = data_root / outcome / index / f"NORMALIZE_{scenario}_Max_sensitivity_{outcome}&{index}120.nc"
    if not path.is_file():
        raise FileNotFoundError(f"Missing selected-sensitivity archive: {path}")
    with xr.open_dataset(path) as dataset:
        values = np.asarray(dataset["max_correlation"].values, dtype=float).ravel()
    values = values[np.isfinite(values)]
    if values.size == 0:
        raise ValueError(f"No finite selected coefficients in {path}")
    return values


def plot_figureS27_panel(ax: plt.Axes, data_root: Path, outcome: str, scenario: str, show_y_labels: bool) -> None:
    summaries = {index: load_coefficients(data_root, outcome, index, scenario) for index in INDICES}
    positions = np.arange(len(INDICES), 0, -1)
    violins = ax.violinplot(
        [summaries[index] for index in INDICES],
        positions=positions,
        vert=False,
        widths=0.72,
        showmeans=False,
        showmedians=False,
        showextrema=False,
        bw_method=0.18,
    )
    for body, index in zip(violins["bodies"], INDICES):
        body.set_facecolor(INDEX_COLORS[index])
        body.set_edgecolor(INDEX_COLORS[index])
        body.set_alpha(0.58)
        body.set_linewidth(0.5)

    for position, index in zip(positions, INDICES):
        values = summaries[index]
        lower, median, upper = np.quantile(values, (0.25, 0.50, 0.75))
        ax.hlines(position, lower, upper, color="#222222", linewidth=1.2, zorder=4)
        ax.plot(median, position, marker="o", markersize=3.0, color="#222222", zorder=5)
        positive_fraction = 100.0 * np.mean(values > 0)
        ax.text(0.98, position, f"{positive_fraction:.0f}% +", ha="right", va="center", fontsize=5.5, color="#333333")

    ax.axvline(0, color="#222222", linestyle="--", linewidth=0.7, zorder=1)
    ax.set_xlim(-1.0, 1.0)
    ax.set_xticks((-1.0, -0.5, 0.0, 0.5, 1.0))
    ax.set_ylim(0.45, len(INDICES) + 0.55)
    ax.grid(axis="x", color="#D9D9D9", linewidth=0.45, zorder=0)
    ax.tick_params(axis="both", length=2.5, width=0.7, pad=2)
    ax.set_yticks(positions, INDICES)
    if not show_y_labels:
        ax.tick_params(axis="y", labelleft=False)


def create_figureS27(data_root: Path, output_dir: Path) -> None:
    """Create the 2 × 5 signed-coefficient distribution grid."""
    configure_matplotlib()
    figure, axes = plt.subplots(2, 5, figsize=(7.2, 3.5), sharex=True, sharey=True, constrained_layout=True)
    panel_index = 0
    for row, outcome in enumerate(OUTCOMES):
        for column, scenario in enumerate(SCENARIOS):
            axis = axes[row, column]
            plot_figureS27_panel(axis, data_root, outcome, scenario, show_y_labels=(column == 0))
            if row == 0:
                axis.set_title(SCENARIO_LABELS[scenario], fontsize=7, pad=5)
            if column == 0:
                axis.set_ylabel(OUTCOME_LABELS[outcome], fontweight="bold", labelpad=10)
            axis.text(0.01, 0.98, f"({chr(ord('a') + panel_index)})", transform=axis.transAxes, ha="left", va="top", fontsize=8, fontweight="bold")
            panel_index += 1

    figure.supxlabel("Signed selected partial-Spearman coefficient, r*")
    output_dir.mkdir(parents=True, exist_ok=True)
    for extension in ("png", "pdf", "svg"):
        figure.savefig(output_dir / f"{OUTPUT_NAME}.{extension}", dpi=600, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    arguments = parse_args()
    create_figureS27(arguments.data_root, arguments.output_dir)
