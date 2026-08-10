"""Create Supplementary Figure S29: global drought-index collinearity diagnostics."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_NAME = "FigureS29"
SCENARIOS = ("historical", "ssp126", "ssp245", "ssp370", "ssp585")
SCENARIO_LABELS = {"historical": "Historical", "ssp126": "SSP1-2.6", "ssp245": "SSP2-4.5", "ssp370": "SSP3-7.0", "ssp585": "SSP5-8.5"}
SCENARIO_COLORS = {"historical": "#4D4D4D", "ssp126": "#4DAF4A", "ssp245": "#377EB8", "ssp370": "#FF7F00", "ssp585": "#E41A1C"}
INDICES = ("SPEI", "SSMI", "STI")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--diagnostics-csv", type=Path, default=PROJECT_ROOT / "src/review_check/res/review_check/drought_index_collinearity_diagnostics/collinearity_diagnostics.csv")
    parser.add_argument("--output-dir", type=Path, default=PROJECT_ROOT / "res/eiar_figs")
    return parser.parse_args()


def configure_matplotlib() -> None:
    mpl.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"], "font.size": 7, "axes.linewidth": 0.7, "axes.spines.right": False, "axes.spines.top": False, "pdf.fonttype": 42, "svg.fonttype": "none"})


def plot_figureS29a(axis: plt.Axes, data: pd.DataFrame) -> None:
    for scenario in SCENARIOS:
        subset = data.loc[data["scenario"].eq(scenario)].sort_values("scale_months")
        maximum_vif = subset[[f"{index}_vif_median" for index in INDICES]].max(axis=1)
        axis.plot(subset["scale_months"], maximum_vif, color=SCENARIO_COLORS[scenario], linewidth=1.1, label=SCENARIO_LABELS[scenario])
    axis.set_title("Maximum median VIF", loc="left", pad=4)
    axis.set_ylabel("Grid-cell median VIF")


def plot_figureS29b(axis: plt.Axes, data: pd.DataFrame) -> None:
    for scenario in SCENARIOS:
        subset = data.loc[data["scenario"].eq(scenario)].sort_values("scale_months")
        axis.plot(subset["scale_months"], subset["condition_index_median"], color=SCENARIO_COLORS[scenario], linewidth=1.1, label=SCENARIO_LABELS[scenario])
    axis.set_title("Median condition index", loc="left", pad=4)
    axis.set_ylabel("Grid-cell median condition index")


def create_figureS29(diagnostics_csv: Path, output_dir: Path) -> None:
    """Create the global VIF and condition-index panels."""
    if not diagnostics_csv.is_file():
        raise FileNotFoundError(f"Missing collinearity diagnostics: {diagnostics_csv}")
    configure_matplotlib()
    data = pd.read_csv(diagnostics_csv).loc[lambda frame: frame["region"].eq("global")].copy()
    figure, axes = plt.subplots(1, 2, figsize=(7.2, 2.65), constrained_layout=True)
    plot_figureS29a(axes[0], data)
    plot_figureS29b(axes[1], data)
    for label, axis in zip(("(a)", "(b)"), axes):
        axis.set_xlabel("Accumulation scale (months)")
        axis.set_xlim(1, 120)
        axis.grid(axis="y", alpha=0.22, linewidth=0.45)
        axis.tick_params(length=3, width=0.7)
        axis.text(-0.13, 1.04, label, transform=axis.transAxes, fontweight="bold", fontsize=8, ha="left", va="bottom")
    handles, labels = axes[0].get_legend_handles_labels()
    figure.legend(handles, labels, loc="upper center", ncol=5, bbox_to_anchor=(0.53, 1.14), columnspacing=1.1)
    output_dir.mkdir(parents=True, exist_ok=True)
    for extension in ("png", "pdf", "svg"):
        figure.savefig(output_dir / f"{OUTPUT_NAME}.{extension}", dpi=600, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    arguments = parse_args()
    create_figureS29(arguments.diagnostics_csv, arguments.output_dir)
