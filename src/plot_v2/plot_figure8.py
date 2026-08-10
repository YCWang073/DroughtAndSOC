# -*- coding: utf-8 -*-
"""
Figure 8：使用 reviewer-ready SEM 结果重绘原 A–D 组合图。

主要更新
--------
1. SEM 文件路径改为 reviewer_ready；
2. 使用模型输出的标准化效应（*_std_estimate）；
3. 仅使用 analysis_valid == 1 的格点；
4. A图使用空间中位数和IQR，替代对全部网格直接求均值；
5. B图绘制土壤水分对SOC的标准化总效应；
6. C、D图仍使用原有SOC模拟与观测数据。
"""

from __future__ import annotations

from pathlib import Path

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib as mpl
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import xarray as xr
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER
from matplotlib import gridspec
from matplotlib.colors import TwoSlopeNorm
from matplotlib.lines import Line2D


# =============================================================================
# 1. 路径设置
# =============================================================================

SEM_ROOT = Path(
    r"/run/media/yue/Elements SE/010_SEM_result_CMIP6/reviewer_ready"
)

LANDMASK_PATH = Path(
    r"/run/media/yue/Elements SE/008_Screening_data_CMIP6/Masks/landmask.nc"
)

OUTPUT_DIR = Path("res/eiar_figs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_NAME = "Figure8"

SIGNIFICANT_ONLY = False
P_THRESHOLD = 0.05

MAP_COLOR_PERCENTILE = 98.0

SAVE_FIGURE = True
SAVE_DPI = 600


# =============================================================================
# 2. 全局样式
# =============================================================================

mpl.rcParams.update(mpl.rcParamsDefault)
mpl.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "DejaVu Sans"],
        "axes.facecolor": "white",
        "axes.edgecolor": "black",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)

landmask = xr.open_dataset(LANDMASK_PATH)["mask"]


# =============================================================================
# 3. 通用函数
# =============================================================================


def sem_file(scenario: str, target: str = "soc") -> Path:
    path = SEM_ROOT / f"SEM_{scenario}_{target}_reviewer_ready.nc"
    if not path.exists():
        raise FileNotFoundError(f"未找到SEM结果文件：{path}")
    return path


def get_sem_effect(
    ds: xr.Dataset,
    variable: str,
    p_variable: str | None = None,
) -> xr.DataArray:
    if "analysis_valid" not in ds:
        raise KeyError("SEM结果中缺少 analysis_valid。")
    if variable not in ds:
        raise KeyError(f"SEM结果中缺少变量：{variable}")

    result = ds[variable].where(ds["analysis_valid"] == 1)

    if SIGNIFICANT_ONLY and p_variable is not None:
        if p_variable not in ds:
            raise KeyError(f"SEM结果中缺少P值变量：{p_variable}")
        result = result.where(ds[p_variable] < P_THRESHOLD)

    return result


def finite_values(data: xr.DataArray) -> np.ndarray:
    values = np.asarray(data.values, dtype=float).ravel()
    return values[np.isfinite(values)]


def spatial_summary(data: xr.DataArray) -> tuple[float, float, float]:
    values = finite_values(data)
    if values.size == 0:
        return np.nan, np.nan, np.nan
    q1, median, q3 = np.quantile(values, [0.25, 0.50, 0.75])
    return float(q1), float(median), float(q3)


def select_region(
    data: xr.DataArray,
    lat0: float,
    lat1: float,
    lon0: float,
    lon1: float,
) -> xr.DataArray:
    lat_values = data["lat"].values
    lon_values = data["lon"].values

    lat_slice = (
        slice(lat0, lat1)
        if lat_values[0] < lat_values[-1]
        else slice(lat1, lat0)
    )
    lon_slice = (
        slice(lon0, lon1)
        if lon_values[0] < lon_values[-1]
        else slice(lon1, lon0)
    )
    return data.sel(lat=lat_slice, lon=lon_slice)


def robust_symmetric_limit(
    arrays: list[xr.DataArray],
    percentile: float = 98.0,
) -> float:
    values = []
    for array in arrays:
        valid = finite_values(array)
        if valid.size:
            values.append(valid)

    if not values:
        return 1.0

    pooled = np.concatenate(values)
    limit = float(np.nanpercentile(np.abs(pooled), percentile))
    if not np.isfinite(limit) or limit <= 0:
        limit = float(np.nanmax(np.abs(pooled)))
    return limit if np.isfinite(limit) and limit > 0 else 1.0


def add_unified_colorbar(fig, ax, mesh, label):
    pos = ax.get_position()
    cax_height = 0.01
    cax_width = pos.width * 0.7
    cax_y = pos.y0 - cax_height - 0.035
    cax_x = pos.x0 + pos.width * 0.15

    cax = fig.add_axes([cax_x, cax_y, cax_width, cax_height])
    cbar = fig.colorbar(mesh, cax=cax, orientation="horizontal", extend="both")
    cbar.ax.tick_params(labelsize=16)
    cbar.set_label(label, fontsize=18)
    return cbar


def draw_rectange_map(
    hotpoint,
    key,
    fig=False,
    ax=None,
    extent=(-180, 180, -60, 90),
    linewi=1,
    lines="-",
):
    if fig is False:
        fig = plt.figure(figsize=(12.27, 6.69), dpi=100, facecolor="white")
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
        ax.set_extent(extent, crs=ccrs.PlateCarree())
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.LAND, facecolor="#FFE9B5")

    lat0, lat1, lon0, lon1 = hotpoint[key]
    ax.plot([lon0, lon1], [lat1, lat1], transform=ccrs.PlateCarree(),
            linewidth=linewi, color="k", ls=lines)
    ax.plot([lon0, lon1], [lat0, lat0], transform=ccrs.PlateCarree(),
            linewidth=linewi, color="k", ls=lines)
    ax.plot([lon0, lon0], [lat0, lat1], transform=ccrs.PlateCarree(),
            linewidth=linewi, color="k", ls=lines)
    ax.plot([lon1, lon1], [lat0, lat1], transform=ccrs.PlateCarree(),
            linewidth=linewi, color="k", ls=lines)


def calculate_total_carbon_store(soc, sftlf):
    grid_area_km2 = 9220
    grid_area_m2 = grid_area_km2 * 1e6
    soc_kg_per_grid = soc * (sftlf / 100) * grid_area_m2
    return soc_kg_per_grid.sum(dim=["lat", "lon"]) / 1e12


# =============================================================================
# 4. Panel A：新版SEM直接效应与总效应
# =============================================================================


def plot_figure8a(
    fig,
    ax,
    stem_width=2.0,
    stem_alpha=0.9,
    marker_size=80,
    marker_edgewidth=2.0,
    y_pad_ratio=0.14,
    colors=None,
    cat_spacing=1.0,
    offset_frac=0.17,
    x_margin=0.12,
):
    from matplotlib.gridspec import GridSpecFromSubplotSpec

    if colors is None:
        colors = {"Total": "#1f77b4", "Direct": "#ff7f0e"}

    scenario_defs = [
        ("Historical", "historical"),
        ("SSP1-2.6", "ssp126"),
        ("SSP5-8.5", "ssp585"),
    ]

    variable_defs = {
        "PR": {
            "title": "Precipitation",
            "Total": ("effect_total_pr_soc_std_estimate", "effect_total_pr_soc_p"),
            "Direct": ("path_soc_from_pr_std_estimate", "path_soc_from_pr_p"),
        },
        "MRSO": {
            "title": "Soil Moisture",
            "Total": ("effect_total_mrso_soc_std_estimate", "effect_total_mrso_soc_p"),
            "Direct": ("path_soc_from_mrso_std_estimate", "path_soc_from_mrso_p"),
        },
        "TS": {
            "title": "Surface Temperature",
            "Total": ("effect_total_ts_soc_std_estimate", "effect_total_ts_soc_p"),
            "Direct": ("path_soc_from_ts_std_estimate", "path_soc_from_ts_p"),
        },
    }

    data = {}
    for key, definition in variable_defs.items():
        data[key] = {"Total": [], "Direct": []}
        for display_name, scenario in scenario_defs:
            with xr.open_dataset(sem_file(scenario, "soc")) as ds:
                for effect_type in ("Total", "Direct"):
                    value_name, p_name = definition[effect_type]
                    da = get_sem_effect(ds, value_name, p_name).load()
                    data[key][effect_type].append(spatial_summary(da))

    all_values = []
    for variable_data in data.values():
        for effect_type in ("Total", "Direct"):
            for q1, median, q3 in variable_data[effect_type]:
                all_values.extend([q1, median, q3])

    all_values = np.asarray(all_values, dtype=float)
    all_values = all_values[np.isfinite(all_values)]
    if all_values.size:
        data_min = float(np.min(all_values))
        data_max = float(np.max(all_values))
    else:
        data_min, data_max = -1.0, 1.0

    data_span = max(data_max - data_min, 0.1)
    y_min = min(0.0, data_min) - y_pad_ratio * data_span
    y_max = max(0.0, data_max) + y_pad_ratio * data_span

    subplot_spec = ax.get_subplotspec()
    fig.delaxes(ax)
    subgrid = GridSpecFromSubplotSpec(
        1, 3, subplot_spec=subplot_spec, wspace=0.10
    )

    scenarios = [item[0] for item in scenario_defs]
    x = np.arange(len(scenarios)) * cat_spacing
    axes = []

    for index, variable in enumerate(("PR", "MRSO", "TS")):
        axis = fig.add_subplot(
            subgrid[0, index],
            sharey=axes[0] if axes else None,
        )
        axes.append(axis)

        x_total = x - offset_frac * cat_spacing
        x_direct = x + offset_frac * cat_spacing

        for effect_type, x_positions in (
            ("Total", x_total),
            ("Direct", x_direct),
        ):
            summaries = data[variable][effect_type]
            medians = np.array([item[1] for item in summaries], dtype=float)
            lower = medians - np.array([item[0] for item in summaries], dtype=float)
            upper = np.array([item[2] for item in summaries], dtype=float) - medians

            for x_value, median in zip(x_positions, medians):
                axis.vlines(
                    x_value,
                    0,
                    median,
                    color=colors[effect_type],
                    linewidth=stem_width,
                    alpha=stem_alpha,
                    zorder=2,
                )

            axis.errorbar(
                x_positions,
                medians,
                yerr=np.vstack([lower, upper]),
                fmt="none",
                ecolor=colors[effect_type],
                elinewidth=1.2,
                capsize=3,
                alpha=0.9,
                zorder=3,
            )

            axis.scatter(
                x_positions,
                medians,
                s=marker_size,
                facecolors="white",
                edgecolors=colors[effect_type],
                linewidths=marker_edgewidth,
                zorder=4,
                label=f"{effect_type} path coefficient",
            )

            text_offset = 0.035 * (y_max - y_min)
            for x_value, median in zip(x_positions, medians):
                if not np.isfinite(median):
                    continue
                vertical_alignment = "bottom" if median >= 0 else "top"
                y_text = median + text_offset if median >= 0 else median - text_offset
                axis.text(
                    x_value,
                    y_text,
                    f"{median:.3f}",
                    ha="center",
                    va=vertical_alignment,
                    fontsize=10,
                    color=colors[effect_type],
                )

        axis.axhline(0, color="black", linewidth=0.8)
        axis.margins(x=x_margin)
        axis.set_xticks(x)
        axis.set_xticklabels(scenarios, fontsize=14)
        axis.set_ylim(y_min, y_max)
        axis.grid(axis="y", alpha=0.3, linestyle="--", linewidth=0.8)
        axis.set_title(variable_defs[variable]["title"], fontsize=14, pad=8)
        axis.set_xlabel("Scenarios", fontsize=16)
        axis.tick_params(axis="y", labelsize=12)
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)

    axes[0].set_ylabel("Standardized path coefficient", fontsize=12)
    axes[0].text(
        -0.12,
        1.08,
        "(a)",
        fontweight="bold",
        transform=axes[0].transAxes,
        fontsize=22,
        va="top",
        ha="left",
    )

    for axis in axes[1:]:
        axis.label_outer()

    handles, labels = axes[0].get_legend_handles_labels()
    axes[0].legend(handles, labels, frameon=False, loc="upper left", fontsize=11)

    return axes


# =============================================================================
# 5. Panel B：新版SEM土壤水分对SOC总效应空间图
# =============================================================================


def plot_figure8b(fig, ax):
    value_name = "effect_total_mrso_soc_std_estimate"
    p_name = "effect_total_mrso_soc_p"

    scenario_arrays = {}
    for scenario in ("historical", "ssp126", "ssp585"):
        with xr.open_dataset(sem_file(scenario, "soc")) as ds:
            scenario_arrays[scenario] = get_sem_effect(
                ds, value_name, p_name
            ).load()

    historical = scenario_arrays["historical"]
    ssp126 = scenario_arrays["ssp126"]
    ssp585 = scenario_arrays["ssp585"]

    ax.set_extent([-170, 180, -60, 90], crs=ccrs.PlateCarree())

    color_limit = robust_symmetric_limit(
        [historical, ssp126, ssp585],
        MAP_COLOR_PERCENTILE,
    )
    cmap = plt.get_cmap("RdBu_r")
    norm = TwoSlopeNorm(vmin=-color_limit, vcenter=0.0, vmax=color_limit)

    mesh = ax.pcolormesh(
        ssp585.lon,
        ssp585.lat,
        ssp585,
        cmap=cmap,
        norm=norm,
        shading="auto",
        transform=ccrs.PlateCarree(),
        zorder=1,
    )

    hotpoint = {
        "AMZ-SE": [-24.1, 1.5, -60.5, -34.5],
        "NAMS": [18.3, 34.9, -119.9, -78.7],
        "AUS": [-38.8, -10.2, 114.1, 154.5],
        "SE-CHN": [21.0, 34.0, 99.4, 123.1],
        "S-AF": [-35.0, -12.8, 9.7, 50.6],
        "MED": [35.2, 56.1, -12.5, 70.3],
    }

    for key in hotpoint:
        draw_rectange_map(hotpoint, key, fig=fig, ax=ax)

    pooled = np.concatenate(
        [
            finite_values(historical),
            finite_values(ssp126),
            finite_values(ssp585),
        ]
    )
    xmin = float(np.nanpercentile(pooled, 1))
    xmax = float(np.nanpercentile(pooled, 99))
    if xmin == xmax:
        xmin -= 1e-3
        xmax += 1e-3

    def lonlat_to_axesxy(lon, lat):
        point = ax.projection.transform_points(
            ccrs.PlateCarree(),
            np.asarray([lon]),
            np.asarray([lat]),
        )[0, :2]
        display = ax.transData.transform(point)
        axes_xy = ax.transAxes.inverted().transform(display)
        return float(axes_xy[0]), float(axes_xy[1])

    inset_offset = {
        "AMZ-SE": (+0.07, -0.16),
        "NAMS": (-0.07, -0.10),
        "AUS": (-0.12, +0.06),
        "SE-CHN": (+0.11, -0.04),
        "S-AF": (+0.07, -0.09),
        "MED": (-0.17, -0.07),
    }
    inset_w, inset_h = 0.10, 0.12

    styles = {
        "ssp585": ("tab:red", "-", "SSP5-8.5"),
        "ssp126": ("tab:blue", "--", "SSP1-2.6"),
        "historical": ("tab:gray", ":", "Historical"),
    }

    x_grid = np.linspace(xmin, xmax, 200)

    def density(values):
        values = values[np.isfinite(values)]
        if values.size < 5:
            return np.zeros_like(x_grid)
        try:
            from scipy.stats import gaussian_kde

            return gaussian_kde(values).evaluate(x_grid)
        except Exception:
            hist, edges = np.histogram(
                values,
                bins=30,
                range=(xmin, xmax),
                density=True,
            )
            centers = 0.5 * (edges[:-1] + edges[1:])
            smooth = np.convolve(hist, np.ones(5) / 5.0, mode="same")
            return np.interp(x_grid, centers, smooth)

    for idx, (region, (lat0, lat1, lon0, lon1)) in enumerate(hotpoint.items()):
        region_values = {
            "ssp585": finite_values(select_region(ssp585, lat0, lat1, lon0, lon1)),
            "ssp126": finite_values(select_region(ssp126, lat0, lat1, lon0, lon1)),
            "historical": finite_values(select_region(historical, lat0, lat1, lon0, lon1)),
        }

        if all(values.size < 5 for values in region_values.values()):
            continue

        densities = {key: density(values) for key, values in region_values.items()}
        density_max = max(
            [np.nanmax(value) for value in densities.values()] + [1e-12]
        )
        densities = {
            key: value / density_max
            for key, value in densities.items()
        }

        center_lat = 0.5 * (lat0 + lat1)
        center_lon = 0.5 * (lon0 + lon1)
        center_x, center_y = lonlat_to_axesxy(center_lon, center_lat)
        dx, dy = inset_offset.get(region, (0.08, 0.05))
        x0 = np.clip(center_x + dx - inset_w / 2, 0.01, 0.99 - inset_w)
        y0 = np.clip(center_y + dy - inset_h / 2, 0.01, 0.99 - inset_h)

        inset = ax.inset_axes([x0, y0, inset_w, inset_h])
        inset.set_facecolor((1, 1, 1, 0.72))

        for scenario in ("ssp585", "ssp126", "historical"):
            color, linestyle, label = styles[scenario]
            values = densities[scenario]
            inset.plot(
                x_grid,
                values,
                lw=1.6,
                ls=linestyle,
                color=color,
                label=label,
            )
            inset.fill_between(x_grid, 0, values, alpha=0.15, color=color)

        inset.axvline(0, color="black", lw=0.8, ls="--", alpha=0.6)
        inset.set_xlim(xmin, xmax)
        inset.set_ylim(0, 1.05)
        inset.set_yticks([0, 1])
        inset.tick_params(axis="x", labelsize=9, pad=1, rotation=45)
        inset.tick_params(axis="y", labelsize=9, pad=1)
        inset.text(
            0.02,
            1.05,
            region,
            fontsize=10,
            weight="bold",
            va="top",
            ha="left",
            transform=inset.transAxes,
        )
        inset.spines["top"].set_visible(False)
        inset.spines["right"].set_visible(False)

        if idx == 0:
            inset.legend(
                loc="upper right",
                bbox_to_anchor=(1.30, 2.30),
                fontsize=10,
                frameon=False,
                handlelength=1.6,
            )

    ax.add_feature(cfeature.COASTLINE, linewidth=0.5, zorder=4)
    ax.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.5, zorder=4)

    gridliner = ax.gridlines(
        crs=ccrs.PlateCarree(),
        draw_labels=True,
        linewidth=0.5,
        color="gray",
        alpha=0.5,
        linestyle="--",
    )
    gridliner.top_labels = False
    gridliner.right_labels = False
    gridliner.xformatter = LONGITUDE_FORMATTER
    gridliner.yformatter = LATITUDE_FORMATTER
    gridliner.xlabel_style = {"size": 18, "color": "black"}
    gridliner.ylabel_style = {"size": 18, "color": "black"}

    position = ax.get_position()
    ax.set_position(
        [position.x0, position.y0 + 0.03, position.width, position.height]
    )

    colorbar = add_unified_colorbar(
        fig,
        ax,
        mesh,
        "Standardized total soil moisture–SOC path coefficient",
    )
    colorbar.locator = mticker.MaxNLocator(nbins=7)
    colorbar.update_ticks()

    ax.text(
        -0.02,
        1.02,
        "(b)",
        fontweight="bold",
        transform=ax.transAxes,
        fontsize=22,
        va="top",
        ha="left",
    )

    return mesh


# =============================================================================
# 6. Panel C：保持原SOC模拟-观测差值图
# =============================================================================


def plot_figure8c(fig, ax):
    obs_soc = xr.open_dataset(
        "/mnt/softwares/Drought_And_SOC/000_observasion_data_ERA5/"
        "01_preprocessed_data/merged_csoil_data.nc"
    )["cSoil"]
    mmem_soc = xr.open_dataset(
        "/run/media/yue/Elements SE/007-1_MEM_data_CMIP6/raw/soc_MMEM.nc"
    )["ssp126_soc"].sel(time=slice("1985-01-01", "2014-12-31")).mean(dim="time")
    mmwm_soc = xr.open_dataset(
        "/run/media/yue/Elements SE/007-2_MMWM_data_CMIP6/raw/soc_MMWM.nc"
    )["ssp126_soc"].sel(time=slice("1985-01-01", "2014-12-31")).mean(dim="time")
    sftlf = xr.open_dataset(
        "/run/media/yue/Elements SE/008_Screening_data_CMIP6/"
        "sftlf/sftlf_historical_1985-2014.nc"
    )["sftlf"]

    obs = calculate_total_carbon_store(obs_soc, sftlf)
    mmem = calculate_total_carbon_store(mmem_soc, sftlf)
    mmwm = calculate_total_carbon_store(mmwm_soc, sftlf)

    difference = mmwm_soc.where(landmask == 1) - obs_soc.where(landmask == 1)

    ax.set_extent([-170, 180, -60, 90], crs=ccrs.PlateCarree())
    cmap = plt.get_cmap("RdBu_r")
    norm = TwoSlopeNorm(vmin=-50, vcenter=0, vmax=50)

    mesh = ax.pcolormesh(
        difference.lon,
        difference.lat,
        difference,
        cmap=cmap,
        norm=norm,
        shading="auto",
        transform=ccrs.PlateCarree(),
        zorder=1,
    )

    ax.add_feature(cfeature.COASTLINE, linewidth=0.5, zorder=3)
    ax.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.5, zorder=3)
    ax.set_title("Historical MMWM–benchmark SOC difference", fontsize=18, pad=15)

    gridliner = ax.gridlines(
        crs=ccrs.PlateCarree(),
        draw_labels=True,
        linewidth=0.5,
        color="gray",
        alpha=0.5,
        linestyle="--",
    )
    gridliner.top_labels = False
    gridliner.right_labels = False
    gridliner.xformatter = LONGITUDE_FORMATTER
    gridliner.yformatter = LATITUDE_FORMATTER
    gridliner.xlabel_style = {"size": 18, "color": "black"}
    gridliner.ylabel_style = {"size": 18, "color": "black"}

    colorbar = add_unified_colorbar(fig, ax, mesh, "SOC difference (kg C m$^{-2}$)")
    colorbar.set_ticks(np.arange(-50, 51, 10))

    ax.text(
        -0.08,
        1.08,
        "(c)",
        fontweight="bold",
        transform=ax.transAxes,
        fontsize=22,
        va="top",
        ha="left",
    )

    ax.text(
        0.06,
        0.07,
        f"Benchmark: {obs.values:.2f} PgC\n"
        f"MMEM: {mmem.values:.2f} PgC\n"
        f"MMWM: {mmwm.values:.2f} PgC",
        fontsize=14,
        transform=ax.transAxes,
        va="bottom",
        ha="left",
    )

    return mesh


# =============================================================================
# 7. Panel D：保持原全球SOC总量哑铃图
# =============================================================================


def plot_figure8d(
    fig,
    ax,
    compact=True,
    annotate=True,
    show_delta=True,
    show_obs_offset=False,
):
    palette = {
        "obs": "#009E73",
        "hist": "#808080",
        "ssp126": "#1f77b4",
        "ssp585": "#d62728",
    }

    obs_soc = xr.open_dataset(
        "/mnt/softwares/Drought_And_SOC/000_observasion_data_ERA5/"
        "01_preprocessed_data/merged_csoil_data.nc"
    )["cSoil"]
    historical_mmem = xr.open_dataset(
        "/run/media/yue/Elements SE/007-1_MEM_data_CMIP6/raw/soc_MMEM.nc"
    )["ssp126_soc"].sel(time=slice("1985-01-01", "2014-12-31")).mean(dim="time")
    historical_mmwm = xr.open_dataset(
        "/run/media/yue/Elements SE/007-2_MMWM_data_CMIP6/raw/soc_MMWM.nc"
    )["ssp126_soc"].sel(time=slice("1985-01-01", "2014-12-31")).mean(dim="time")
    ssp126_mmem = xr.open_dataset(
        "/run/media/yue/Elements SE/007-1_MEM_data_CMIP6/raw/soc_MMEM.nc"
    )["ssp126_soc"].sel(time=slice("2070-01-01", "2099-12-31")).mean(dim="time")
    ssp126_mmwm = xr.open_dataset(
        "/run/media/yue/Elements SE/007-2_MMWM_data_CMIP6/raw/soc_MMWM.nc"
    )["ssp126_soc"].sel(time=slice("2070-01-01", "2099-12-31")).mean(dim="time")
    ssp585_mmem = xr.open_dataset(
        "/run/media/yue/Elements SE/007-1_MEM_data_CMIP6/raw/soc_MMEM.nc"
    )["ssp585_soc"].sel(time=slice("2070-01-01", "2099-12-31")).mean(dim="time")
    ssp585_mmwm = xr.open_dataset(
        "/run/media/yue/Elements SE/007-2_MMWM_data_CMIP6/raw/soc_MMWM.nc"
    )["ssp585_soc"].sel(time=slice("2070-01-01", "2099-12-31")).mean(dim="time")
    sftlf = xr.open_dataset(
        "/run/media/yue/Elements SE/008_Screening_data_CMIP6/"
        "sftlf/sftlf_historical_1985-2014.nc"
    )["sftlf"]

    obs = float(calculate_total_carbon_store(obs_soc, sftlf).values)
    pairs_m = [
        float(calculate_total_carbon_store(historical_mmem, sftlf).values),
        float(calculate_total_carbon_store(ssp126_mmem, sftlf).values),
        float(calculate_total_carbon_store(ssp585_mmem, sftlf).values),
    ]
    pairs_w = [
        float(calculate_total_carbon_store(historical_mmwm, sftlf).values),
        float(calculate_total_carbon_store(ssp126_mmwm, sftlf).values),
        float(calculate_total_carbon_store(ssp585_mmwm, sftlf).values),
    ]

    scenarios = ["Historical", "SSP1-2.6", "SSP5-8.5"]
    colors = [palette["hist"], palette["ssp126"], palette["ssp585"]]
    y_positions = np.arange(len(scenarios))

    ax.axvline(obs, ls="--", lw=1.5, color=palette["obs"], zorder=1)
    ax.text(
        obs,
        -0.05,
        "REF",
        transform=ax.get_xaxis_transform(),
        ha="center",
        va="bottom",
        fontsize=12,
        color=palette["obs"],
    )

    for y, x1, x2, color in zip(y_positions, pairs_m, pairs_w, colors):
        ax.plot([x1, x2], [y, y], lw=2.0, color=color, zorder=2)
        ax.scatter([x1], [y], s=26, marker="o", color=color,
                   edgecolor="0.2", linewidth=0.6, zorder=3)
        ax.scatter([x2], [y], s=26, marker="s", facecolors="white",
                   edgecolors=color, linewidth=1.0, zorder=4)

        if annotate:
            ax.annotate(
                f"{x1:,.2f}",
                (x1, y),
                xytext=(-4, 11),
                textcoords="offset points",
                ha="right",
                va="bottom",
                fontsize=12,
                color=color,
            )
            ax.annotate(
                f"{x2:,.2f}",
                (x2, y),
                xytext=(4, -9),
                textcoords="offset points",
                ha="left",
                va="top",
                fontsize=12,
                color=color,
            )

        if show_delta:
            midpoint = (x1 + x2) / 2
            difference = abs(x1 - x2)
            ax.text(
                midpoint,
                y - 0.35,
                f"MMEM − MMWM = {difference:.2f} PgC",
                ha="center",
                va="bottom",
                fontsize=9,
                color=color,
            )

        if show_obs_offset:
            for value, dy in ((x1, 0.10), (x2, -0.10)):
                ax.annotate(
                    "",
                    xy=(value, y + dy),
                    xytext=(obs, y + dy),
                    arrowprops=dict(arrowstyle="<->", lw=0.6, color="0.4"),
                )

    all_values = pairs_m + pairs_w + [obs]
    minimum, maximum = min(all_values), max(all_values)
    padding = (maximum - minimum) * (0.025 if compact else 0.06)
    ax.set_xlim(minimum - padding, maximum + padding)
    ax.set_yticks(y_positions)
    ax.set_ylim(-0.5, len(scenarios) - 0.5)
    ax.set_yticklabels(scenarios, fontsize=14)
    ax.set_xlabel("Global SOC stock (PgC)", fontsize=16)
    ax.grid(axis="x", lw=0.4, alpha=0.25)
    ax.xaxis.set_major_locator(mticker.MaxNLocator(nbins=5))
    ax.xaxis.set_major_formatter(
        mticker.FuncFormatter(lambda value, _: f"{value:,.0f}")
    )
    ax.tick_params(axis="x", labelsize=12)

    legend_elements = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor="black",
               markeredgecolor="0.2", label="MMEM", markersize=5),
        Line2D([0], [0], marker="s", color="none", markerfacecolor="white",
               markeredgecolor="black", label="MMWM", markersize=5),
        Line2D([0], [0], color=palette["obs"], lw=1.2, ls="--",
               label="Benchmark"),
    ]
    ax.legend(
        handles=legend_elements,
        ncol=3,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.14),
        frameon=False,
    )

    ax.text(
        -0.15,
        1.0,
        "(d)",
        fontweight="bold",
        transform=ax.transAxes,
        fontsize=22,
        va="top",
        ha="left",
    )

    return fig, ax


# =============================================================================
# 8. 整图生成
# =============================================================================


def create_figure8():
    fig = plt.figure(figsize=(16, 20), facecolor="white")

    grid = gridspec.GridSpec(
        3,
        2,
        figure=fig,
        width_ratios=[4, 1],
        height_ratios=[3, 6, 4],
        wspace=0.07,
        hspace=0.40,
        top=0.95,
        bottom=0.07,
        left=0.10,
        right=0.99,
    )

    ax_a = fig.add_subplot(grid[0, :])
    plot_figure8a(fig, ax_a)

    ax_b = fig.add_subplot(
        grid[1, :],
        projection=ccrs.Robinson(central_longitude=10),
    )
    plot_figure8b(fig, ax_b)

    ax_c = fig.add_subplot(
        grid[2, 0],
        projection=ccrs.Robinson(central_longitude=10),
    )
    plot_figure8c(fig, ax_c)

    ax_d = fig.add_subplot(grid[2, 1])
    plot_figure8d(fig, ax_d)

    if SAVE_FIGURE:
        png_path = OUTPUT_DIR / f"{OUTPUT_NAME}.png"
        pdf_path = OUTPUT_DIR / f"{OUTPUT_NAME}.pdf"
        fig.savefig(
            png_path,
            dpi=SAVE_DPI,
            bbox_inches="tight",
            facecolor="white",
        )
        fig.savefig(
            pdf_path,
            dpi=SAVE_DPI,
            bbox_inches="tight",
            facecolor="white",
        )
        print(f"已保存：{png_path}")
        print(f"已保存：{pdf_path}")


if __name__ == "__main__":
    create_figure8()
