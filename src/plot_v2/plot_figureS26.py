"""
Supplementary Figure S26：使用 reviewer-ready Rh SEM 结果重绘原 A–C 组合图。

主要更新
--------
1. SEM 文件路径改为 reviewer_ready；
2. 使用模型输出的标准化效应（*_std_estimate）；
3. 仅使用 analysis_valid == 1 的格点；
4. A图使用空间中位数和IQR，替代对全部网格直接求均值；
5. A图增加 SOC -> Rh，因为它是Rh模型的重要解释变量；
6. B图绘制 SSP5-8.5 下土壤水分对Rh的标准化总效应；
7. C图仍使用原有Rh模拟与观测数据，但改用pcolormesh提高绘图效率。
"""

from __future__ import annotations

from pathlib import Path

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import xarray as xr
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER
from matplotlib import gridspec
from matplotlib.colors import TwoSlopeNorm


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
OUTPUT_NAME = "FigureS26"

# 是否仅绘制 P < 0.05 的效应格点。默认False，与原图保持可比。
SIGNIFICANT_ONLY = False
P_THRESHOLD = 0.05

# B图色轴使用三个情景有效值绝对值的稳健分位数
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

with xr.open_dataset(LANDMASK_PATH) as _landmask_ds:
    landmask = _landmask_ds["mask"].load()


# =============================================================================
# 3. 通用函数
# =============================================================================


def sem_file(scenario: str, target: str = "rh") -> Path:
    """返回新版SEM文件路径。"""
    path = SEM_ROOT / f"SEM_{scenario}_{target}_reviewer_ready.nc"
    if not path.exists():
        raise FileNotFoundError(f"未找到SEM结果文件：{path}")
    return path


def get_sem_effect(
    ds: xr.Dataset,
    variable: str,
    p_variable: str | None = None,
) -> xr.DataArray:
    """读取SEM效应，并应用analysis_valid及可选显著性掩膜。"""
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
    """返回一维有限值数组。"""
    values = np.asarray(data.values, dtype=float).ravel()
    return values[np.isfinite(values)]


def spatial_summary(data: xr.DataArray) -> tuple[float, float, float]:
    """返回空间Q1、中位数和Q3。"""
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
    """兼容升序或降序经纬度的区域截取。"""
    lat_values = data["lat"].values
    lon_values = data["lon"].values

    lat_slice = slice(lat0, lat1) if lat_values[0] < lat_values[-1] else slice(lat1, lat0)
    lon_slice = slice(lon0, lon1) if lon_values[0] < lon_values[-1] else slice(lon1, lon0)
    return data.sel(lat=lat_slice, lon=lon_slice)


def robust_symmetric_limit(
    arrays: list[xr.DataArray],
    percentile: float = 98.0,
) -> float:
    """按绝对值稳健分位数确定以0为中心的对称色轴范围。"""
    pooled_parts = [finite_values(array) for array in arrays]
    pooled_parts = [part for part in pooled_parts if part.size]

    if not pooled_parts:
        return 1.0

    pooled = np.concatenate(pooled_parts)
    limit = float(np.nanpercentile(np.abs(pooled), percentile))
    if not np.isfinite(limit) or limit <= 0:
        limit = float(np.nanmax(np.abs(pooled)))
    return limit if np.isfinite(limit) and limit > 0 else 1.0


def add_unified_colorbar(fig, ax, mesh, label):
    """在地图下方添加统一横向颜色条。"""
    pos = ax.get_position()
    cax_height = 0.01
    cax_width = pos.width * 0.70
    cax_y = pos.y0 - cax_height - 0.035
    cax_x = pos.x0 + pos.width * 0.15

    cax = fig.add_axes([cax_x, cax_y, cax_width, cax_height])
    cbar = fig.colorbar(mesh, cax=cax, orientation="horizontal", extend="both")
    cbar.ax.tick_params(labelsize=16)
    cbar.set_label(label, fontsize=18)
    return cbar


def draw_rectangle_map(
    hotpoint: dict,
    key: str,
    ax,
    linewidth: float = 1.0,
    linestyle: str = "-",
):
    """绘制重点区域矩形框。"""
    lat0, lat1, lon0, lon1 = hotpoint[key]
    kwargs = {
        "transform": ccrs.PlateCarree(),
        "linewidth": linewidth,
        "color": "black",
        "ls": linestyle,
        "zorder": 5,
    }
    ax.plot([lon0, lon1], [lat1, lat1], **kwargs)
    ax.plot([lon0, lon1], [lat0, lat0], **kwargs)
    ax.plot([lon0, lon0], [lat0, lat1], **kwargs)
    ax.plot([lon1, lon1], [lat0, lat1], **kwargs)


def add_map_features(ax, fontsize: int = 18):
    """添加海岸线、国界和经纬网。"""
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
    gridliner.xlabel_style = {"size": fontsize, "color": "black"}
    gridliner.ylabel_style = {"size": fontsize, "color": "black"}


# =============================================================================
# 4. Panel A：新版Rh SEM直接效应与总效应
# =============================================================================


def plot_figure_s26_a(
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
    """
    使用reviewer-ready Rh SEM绘制标准化直接效应和总效应。

    Total:
      effect_total_pr_rh_std_estimate
      effect_total_mrso_rh_std_estimate
      effect_total_ts_rh_std_estimate
      effect_total_soc_rh_std_estimate

    Direct:
      path_rh_from_pr_std_estimate
      path_rh_from_mrso_std_estimate
      path_rh_from_ts_std_estimate
      path_rh_from_soc_std_estimate

    每个点表示analysis_valid格点的空间中位数，误差线表示IQR。
    """
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
            "Total": ("effect_total_pr_rh_std_estimate", "effect_total_pr_rh_p"),
            "Direct": ("path_rh_from_pr_std_estimate", "path_rh_from_pr_p"),
        },
        "MRSO": {
            "title": "Soil Moisture",
            "Total": ("effect_total_mrso_rh_std_estimate", "effect_total_mrso_rh_p"),
            "Direct": ("path_rh_from_mrso_std_estimate", "path_rh_from_mrso_p"),
        },
        "TS": {
            "title": "Surface Temperature",
            "Total": ("effect_total_ts_rh_std_estimate", "effect_total_ts_rh_p"),
            "Direct": ("path_rh_from_ts_std_estimate", "path_rh_from_ts_p"),
        },
        "SOC": {
            "title": "Soil Organic Carbon",
            "Total": ("effect_total_soc_rh_std_estimate", "effect_total_soc_rh_p"),
            "Direct": ("path_rh_from_soc_std_estimate", "path_rh_from_soc_p"),
        },
    }

    data: dict[str, dict[str, list[tuple[float, float, float]]]] = {}
    for key, definition in variable_defs.items():
        data[key] = {"Total": [], "Direct": []}
        for _, scenario in scenario_defs:
            with xr.open_dataset(sem_file(scenario, "rh")) as ds:
                for effect_type in ("Total", "Direct"):
                    value_name, p_name = definition[effect_type]
                    da = get_sem_effect(ds, value_name, p_name).load()
                    data[key][effect_type].append(spatial_summary(da))

    all_values: list[float] = []
    for variable_data in data.values():
        for effect_type in ("Total", "Direct"):
            for q1, median, q3 in variable_data[effect_type]:
                all_values.extend([q1, median, q3])

    finite_all = np.asarray(all_values, dtype=float)
    finite_all = finite_all[np.isfinite(finite_all)]
    if finite_all.size:
        data_min = float(np.min(finite_all))
        data_max = float(np.max(finite_all))
    else:
        data_min, data_max = -1.0, 1.0

    data_span = max(data_max - data_min, 0.1)
    y_min = min(0.0, data_min) - y_pad_ratio * data_span
    y_max = max(0.0, data_max) + y_pad_ratio * data_span

    subplot_spec = ax.get_subplotspec()
    fig.delaxes(ax)
    subgrid = GridSpecFromSubplotSpec(
        2,
        2,
        subplot_spec=subplot_spec,
        wspace=0.18,
        hspace=0.34,
    )

    scenarios = [display_name for display_name, _ in scenario_defs]
    x = np.arange(len(scenarios)) * cat_spacing
    axes = []

    variable_order = [("PR", 0, 0), ("MRSO", 0, 1), ("TS", 1, 0), ("SOC", 1, 1)]

    for variable, row_idx, col_idx in variable_order:
        axis = fig.add_subplot(
            subgrid[row_idx, col_idx],
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
            medians = np.asarray([item[1] for item in summaries], dtype=float)
            q1_values = np.asarray([item[0] for item in summaries], dtype=float)
            q3_values = np.asarray([item[2] for item in summaries], dtype=float)
            lower = medians - q1_values
            upper = q3_values - medians

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
                if median >= 0:
                    y_text = median + text_offset
                    va = "bottom"
                else:
                    y_text = median - text_offset
                    va = "top"
                axis.text(
                    x_value,
                    y_text,
                    f"{median:.3f}",
                    ha="center",
                    va=va,
                    fontsize=9,
                    color=colors[effect_type],
                )

        axis.axhline(0, color="black", linewidth=0.8)
        axis.margins(x=x_margin)
        axis.set_xticks(x)
        axis.set_xticklabels(scenarios, fontsize=14)
        axis.set_ylim(y_min, y_max)
        axis.grid(axis="y", alpha=0.3, linestyle="--", linewidth=0.8)
        axis.set_title(variable_defs[variable]["title"], fontsize=13, pad=8)
        axis.tick_params(axis="y", labelsize=12)
        axis.tick_params(axis="x", labelsize=14)
        if row_idx == 0:
            axis.set_xlabel("")
        else:
            axis.set_xlabel("Scenarios", fontsize=16)
        if col_idx == 1:
            axis.tick_params(axis="y", labelleft=False)
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)

    axes[0].set_ylabel("Standardized path coefficient", fontsize=12)
    axes[2].set_ylabel("Standardized path coefficient", fontsize=12)
    axes[0].text(
        -0.08,
        1.08,
        "(a)",
        fontweight="bold",
        transform=axes[0].transAxes,
        fontsize=22,
        va="top",
        ha="left",
    )


    handles, labels = axes[0].get_legend_handles_labels()
    unique = dict(zip(labels, handles))
    axes[0].legend(handles, labels, frameon=False, loc="upper left", fontsize=11)

    return axes


# =============================================================================
# 5. Panel B：新版SEM土壤水分对Rh总效应空间图
# =============================================================================


def plot_figure_s26_b(fig, ax):
    """
    地图：SSP5-8.5时期 mrso -> Rh 的标准化总效应。
    插图：Historical、SSP1-2.6和SSP5-8.5在重点区域的效应密度。
    """
    value_name = "effect_total_mrso_rh_std_estimate"
    p_name = "effect_total_mrso_rh_p"

    scenario_arrays: dict[str, xr.DataArray] = {}
    for scenario in ("historical", "ssp126", "ssp585"):
        with xr.open_dataset(sem_file(scenario, "rh")) as ds:
            scenario_arrays[scenario] = get_sem_effect(
                ds,
                value_name,
                p_name,
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
        draw_rectangle_map(hotpoint, key, ax=ax)

    pooled_parts = [
        finite_values(historical),
        finite_values(ssp126),
        finite_values(ssp585),
    ]
    pooled_parts = [part for part in pooled_parts if part.size]
    if pooled_parts:
        pooled = np.concatenate(pooled_parts)
        xmin = float(np.nanpercentile(pooled, 1))
        xmax = float(np.nanpercentile(pooled, 99))
    else:
        xmin, xmax = -1.0, 1.0
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
        density_max = max([np.nanmax(value) for value in densities.values()] + [1e-12])
        densities = {key: value / density_max for key, value in densities.items()}

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

    add_map_features(ax, fontsize=18)

    position = ax.get_position()
    ax.set_position(
        [position.x0, position.y0 + 0.03, position.width, position.height]
    )

    colorbar = add_unified_colorbar(
        fig,
        ax,
        mesh,
        "Standardized total soil moisture–Rh path coefficient",
    )
    colorbar.locator = mticker.MaxNLocator(nbins=7)
    colorbar.update_ticks()

    ax.text(
        -0.08,
        1.08,
        "(b)",
        fontweight="bold",
        transform=ax.transAxes,
        fontsize=22,
        va="top",
        ha="left",
    )

    return mesh


# =============================================================================
# 6. Panel C：保持原Rh模拟-观测差值图
# =============================================================================


def plot_figure_s26_c(fig, ax):
    obs_path = (
        "/mnt/softwares/Drought_And_SOC/000_observasion_data_ERA5/"
        "01_preprocessed_data/merged_rh_data.nc"
    )
    mmwm_path = (
        "/run/media/yue/Elements SE/007-2_MMWM_data_CMIP6/raw/rh_MMWM.nc"
    )

    with xr.open_dataset(obs_path) as ds:
        obs_rh = ds["Rh"].load()
    with xr.open_dataset(mmwm_path) as ds:
        mmwm_rh = (
            ds["ssp126_rh"]
            .sel(time=slice("1985-01-01", "2014-12-31"))
            .mean(dim="time")
            .load()
        )

    difference = mmwm_rh.where(landmask == 1) - obs_rh.where(landmask == 1)

    ax.set_extent([-170, 180, -60, 90], crs=ccrs.PlateCarree())
    cmap = plt.get_cmap("RdBu_r")
    norm = TwoSlopeNorm(vmin=-1.0, vcenter=0.0, vmax=1.0)

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

    add_map_features(ax, fontsize=18)
    ax.set_title("Historical MMWM–benchmark Rh difference", fontsize=18, pad=15)

    colorbar = add_unified_colorbar(
        fig,
        ax,
        mesh,
        "Rh difference",
    )
    colorbar.set_ticks(np.arange(-1.0, 1.01, 0.2))

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

    return mesh


# =============================================================================
# 7. 创建与保存组合图
# =============================================================================

def create_figure_s26():
    """创建新版Rh补充图。"""
    fig = plt.figure(figsize=(10, 20), facecolor="white")

    grid = gridspec.GridSpec(
        3,
        1,
        figure=fig,
        height_ratios=[9.0, 6.0, 6.0],
        hspace=0.40,
        top=0.95,
        bottom=0.07,
        left=0.08,
        right=0.99,
    )

    placeholder = fig.add_subplot(grid[0, 0])
    plot_figure_s26_a(fig, placeholder)

    ax_map = fig.add_subplot(
        grid[1, 0],
        projection=ccrs.Robinson(central_longitude=10),
    )
    plot_figure_s26_b(fig, ax_map)

    ax_difference = fig.add_subplot(
        grid[2, 0],
        projection=ccrs.Robinson(central_longitude=10),
    )
    plot_figure_s26_c(fig, ax_difference)

    if SAVE_FIGURE:
        png_path = OUTPUT_DIR / f"{OUTPUT_NAME}.png"
        pdf_path = OUTPUT_DIR / f"{OUTPUT_NAME}.pdf"
        fig.savefig(png_path, dpi=SAVE_DPI, bbox_inches="tight")
        fig.savefig(pdf_path, dpi=SAVE_DPI, bbox_inches="tight")
        print(f"已保存：{png_path}")
        print(f"已保存：{pdf_path}")



if __name__ == "__main__":
    create_figure_s26()
