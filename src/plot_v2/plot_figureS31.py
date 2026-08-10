"""Create Supplementary Figure S31: paired spatial-block-bootstrap contrasts."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_NAME = "FigureS31"
SCENARIOS = ("historical", "ssp126", "ssp245", "ssp370", "ssp585")
SCENARIO_LABELS = {"historical": "Historical", "ssp126": "SSP1-2.6", "ssp245": "SSP2-4.5", "ssp370": "SSP3-7.0", "ssp585": "SSP5-8.5"}
OUTCOMES = ("SOC", "RH")
CONTRASTS = ("SPEI - SSMI", "SPEI - STI", "SSMI - STI")
CONTRAST_COLORS = {"SPEI - SSMI": "#3775BA", "SPEI - STI": "#B64342", "SSMI - STI": "#42949E"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bootstrap-csv", type=Path, default=PROJECT_ROOT / "res/review_check/selected_sensitivity_bootstrap/pairwise_selected_sensitivity_bootstrap.csv")
    parser.add_argument("--output-dir", type=Path, default=PROJECT_ROOT / "res/eiar_figs")
    return parser.parse_args()


def configure_matplotlib() -> None:
    mpl.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"], "font.size": 7, "axes.linewidth": 0.7, "axes.spines.right": False, "axes.spines.top": False, "pdf.fonttype": 42, "svg.fonttype": "none"})


def plot_figureS31_panel(axis: plt.Axes, data: pd.DataFrame, outcome: str) -> None:
    offsets = dict(zip(CONTRASTS, (-0.22, 0.0, 0.22)))
    subset = data.loc[data["outcome"].str.upper().eq(outcome)]
    for scenario_position, scenario in enumerate(SCENARIOS):
        scenario_data = subset.loc[subset["scenario"].eq(scenario)]
        for contrast in CONTRASTS:
            row = scenario_data.loc[scenario_data["contrast"].eq(contrast)].iloc[0]
            estimate = row["mean_difference"]
            x_error = np.array([[estimate - row["bootstrap_ci_2_5"]], [row["bootstrap_ci_97_5"] - estimate]])
            axis.errorbar(estimate, scenario_position + offsets[contrast], xerr=x_error, fmt="o", color=CONTRAST_COLORS[contrast], capsize=2.0, markersize=3.8, elinewidth=1.0, label=contrast if scenario_position == 0 else None)
    axis.axvline(0, color="#767676", linewidth=0.8, linestyle="--", zorder=0)
    axis.set_title(outcome, loc="left", pad=4)
    axis.set_xlabel("Difference in spatial mean selected |partial Spearman r|")
    axis.grid(axis="x", alpha=0.22, linewidth=0.45)
    axis.tick_params(length=3, width=0.7)


def plot_figureS31a(axis: plt.Axes, data: pd.DataFrame) -> None:
    plot_figureS31_panel(axis, data, "SOC")


def plot_figureS31b(axis: plt.Axes, data: pd.DataFrame) -> None:
    plot_figureS31_panel(axis, data, "RH")


def create_figureS31(bootstrap_csv: Path, output_dir: Path) -> None:
    """Create SOC and Rh paired spatial-block-bootstrap forest plots."""
    if not bootstrap_csv.is_file():
        raise FileNotFoundError(f"Missing bootstrap summary: {bootstrap_csv}")
    configure_matplotlib()
    data = pd.read_csv(bootstrap_csv).loc[lambda frame: frame["region"].eq("global")].copy()
    figure, axes = plt.subplots(1, 2, figsize=(7.2, 3.2), constrained_layout=True, sharey=True)
    plot_figureS31a(axes[0], data)
    plot_figureS31b(axes[1], data)
    for label, axis in zip(("(a)", "(b)"), axes):
        axis.text(-0.13, 1.04, label, transform=axis.transAxes, fontweight="bold", fontsize=8, ha="left", va="bottom")
    axes[0].set_yticks(range(len(SCENARIOS)), [SCENARIO_LABELS[item] for item in SCENARIOS])
    axes[0].set_ylabel("Scenario")
    axes[0].invert_yaxis()
    handles, labels = axes[0].get_legend_handles_labels()
    figure.legend(handles, labels, loc="upper center", ncol=3, bbox_to_anchor=(0.54, 1.14), columnspacing=1.5)
    output_dir.mkdir(parents=True, exist_ok=True)
    for extension in ("png", "pdf", "svg"):
        figure.savefig(output_dir / f"{OUTPUT_NAME}.{extension}", dpi=600, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    arguments = parse_args()
    create_figureS31(arguments.bootstrap_csv, arguments.output_dir)
