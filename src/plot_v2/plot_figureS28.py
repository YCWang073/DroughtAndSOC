"""Create Supplementary Figure S28: individual-model SOC and Rh trajectories."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_NAME = "FigureS28"
SCENARIOS = ("ssp126", "ssp245", "ssp370", "ssp585")
SCENARIO_LABELS = {"ssp126": "SSP1-2.6", "ssp245": "SSP2-4.5", "ssp370": "SSP3-7.0", "ssp585": "SSP5-8.5"}
OUTCOMES = ("SOC", "RH")
OUTCOME_LABELS = {"SOC": "SOC (kg C m$^{-2}$)", "RH": "Rh (kg C m$^{-2}$ yr$^{-1}$)"}
SCENARIO_COLORS = {
    "SOC": {"ssp126": "#3498DB", "ssp245": "#27AE60", "ssp370": "#F39C12", "ssp585": "#E74C3C"},
    "RH": {"ssp126": "#2980B9", "ssp245": "#16A085", "ssp370": "#D35400", "ssp585": "#C0392B"},
}
HISTORICAL_COLORS = {"SOC": "#2C3E50", "RH": "#7F8C8D"}
HISTORICAL_SCENARIO = "ssp126"
HISTORICAL_END_YEAR = 2014
PLOT_START_YEAR = 1985
PLOT_END_YEAR = 2099


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trajectory-csv", type=Path, default=PROJECT_ROOT / "res/review_check/model_spread/annual_model_trajectories.csv")
    parser.add_argument("--output-dir", type=Path, default=PROJECT_ROOT / "res/eiar_figs")
    return parser.parse_args()


def configure_matplotlib() -> None:
    mpl.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"], "font.size": 7, "axes.linewidth": 0.8, "axes.spines.right": False, "axes.spines.top": False, "pdf.fonttype": 42, "svg.fonttype": "none"})


def load_trajectories(path: Path) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(f"Missing trajectory archive: {path}")
    frame = pd.read_csv(path)
    required = {"outcome", "scenario", "aggregation", "series_id", "region", "year", "value"}
    missing = required.difference(frame.columns)
    if missing:
        raise KeyError(f"Trajectory archive lacks columns: {sorted(missing)}")
    return frame.loc[frame["region"].eq("global") & frame["outcome"].isin(OUTCOMES) & frame["scenario"].isin(SCENARIOS) & frame["year"].between(PLOT_START_YEAR, PLOT_END_YEAR)].copy()


def add_period_background(axis: plt.Axes) -> None:
    axis.axvspan(PLOT_START_YEAR, HISTORICAL_END_YEAR, color="#E6F5FF", zorder=0)
    axis.axvspan(HISTORICAL_END_YEAR, PLOT_END_YEAR, color="#FFF9E6", zorder=0)
    axis.axvline(HISTORICAL_END_YEAR, color="#6E6E6E", linewidth=0.7, zorder=1)


def plot_figureS28_panel(axis: plt.Axes, frame: pd.DataFrame, outcome: str) -> None:
    add_period_background(axis)
    historical = frame.loc[frame["outcome"].eq(outcome) & frame["scenario"].eq(HISTORICAL_SCENARIO) & frame["year"].le(HISTORICAL_END_YEAR)]
    for _, series in historical.loc[historical["aggregation"].eq("individual_model")].groupby("series_id"):
        axis.plot(series["year"], series["value"], color=HISTORICAL_COLORS[outcome], linewidth=0.55, alpha=0.30)
    for aggregation, linestyle, width in (("MMWM", "-", 1.55), ("MMEM", "--", 1.25)):
        series = historical.loc[historical["aggregation"].eq(aggregation)]
        axis.plot(series["year"], series["value"], color=HISTORICAL_COLORS[outcome], linestyle=linestyle, linewidth=width, zorder=4)

    for scenario in SCENARIOS:
        future = frame.loc[frame["outcome"].eq(outcome) & frame["scenario"].eq(scenario) & frame["year"].ge(HISTORICAL_END_YEAR)]
        color = SCENARIO_COLORS[outcome][scenario]
        for _, series in future.loc[future["aggregation"].eq("individual_model")].groupby("series_id"):
            axis.plot(series["year"], series["value"], color=color, linewidth=0.55, alpha=0.18)
        for aggregation, linestyle, width in (("MMWM", "-", 1.55), ("MMEM", "--", 1.25)):
            series = future.loc[future["aggregation"].eq(aggregation)]
            axis.plot(series["year"], series["value"], color=color, linestyle=linestyle, linewidth=width, zorder=4)


def add_legends(figure: plt.Figure) -> None:
    def scenario_handles(outcome: str) -> list[mlines.Line2D]:
        return [mlines.Line2D([], [], color=SCENARIO_COLORS[outcome][scenario], linewidth=1.6, label=SCENARIO_LABELS[scenario]) for scenario in SCENARIOS]
    style_handles = [mlines.Line2D([], [], color="#303030", linewidth=1.6, label="MMWM (solid)"), mlines.Line2D([], [], color="#303030", linestyle="--", linewidth=1.4, label="MMEM (dashed)"), mlines.Line2D([], [], color="#7A7A7A", linewidth=0.8, alpha=0.45, label="individual models (thin)")]
    figure.legend(handles=scenario_handles("SOC"), loc="upper center", bbox_to_anchor=(0.59, 0.992), ncol=4, fontsize=6.3, columnspacing=1.0, handlelength=2.0)
    figure.legend(handles=scenario_handles("RH"), loc="upper center", bbox_to_anchor=(0.59, 0.946), ncol=4, fontsize=6.3, columnspacing=1.0, handlelength=2.0)
    figure.legend(handles=style_handles, loc="upper center", bbox_to_anchor=(0.59, 0.900), ncol=3, fontsize=6.3, columnspacing=1.0, handlelength=2.0)
    figure.text(0.085, 0.972, "SOC:", ha="left", va="center", fontsize=6.3, fontweight="bold")
    figure.text(0.085, 0.926, "Rh:", ha="left", va="center", fontsize=6.3, fontweight="bold")


def create_figureS28(trajectory_csv: Path, output_dir: Path) -> None:
    """Create the SOC/Rh model trajectory panels."""
    configure_matplotlib()
    trajectories = load_trajectories(trajectory_csv)
    figure, axes = plt.subplots(2, 1, figsize=(7.2, 6.25), sharex=True)
    figure.subplots_adjust(left=0.10, right=0.95, bottom=0.05, top=0.84, hspace=0.10)
    for label, axis, outcome in zip(("(a)", "(b)"), axes, OUTCOMES):
        plot_figureS28_panel(axis, trajectories, outcome)
        axis.set_xlim(PLOT_START_YEAR, PLOT_END_YEAR)
        axis.set_xticks((1985, 2000, 2014, 2030, 2050, 2070, 2099))
        axis.set_ylabel(OUTCOME_LABELS[outcome])
        if outcome == "RH":
            axis.set_xlabel("Year")
        else:
            axis.set_ylim(4.0, 29.0)
            axis.set_yticks((4, 9, 14, 19, 24, 29))
        axis.tick_params(axis="both", length=2.5, width=0.7, pad=2)
        axis.text(0.01, 0.98, label, transform=axis.transAxes, ha="left", va="top", fontsize=8, fontweight="bold")
        axis.text(1999, 0.98, "Historical", transform=axis.get_xaxis_transform(), ha="center", va="top", fontsize=6)
        axis.text(2057, 0.98, "Future scenarios", transform=axis.get_xaxis_transform(), ha="center", va="top", fontsize=6)
    add_legends(figure)
    output_dir.mkdir(parents=True, exist_ok=True)
    for extension in ("png", "pdf", "svg"):
        figure.savefig(output_dir / f"{OUTPUT_NAME}.{extension}", dpi=600, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    arguments = parse_args()
    create_figureS28(arguments.trajectory_csv, arguments.output_dir)
