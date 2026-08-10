"""Create manuscript Supplementary Figure S12.

Converted from PlotSupplementaryFig12.ipynb. Only complete figures are saved
to res/eiar_figs.
"""

import os

import matplotlib.patches as patches
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import numpy as np
from matplotlib import gridspec
import matplotlib as mpl

OUTPUT_DIR = "res/eiar_figs"

landmask = xr.open_dataset("/run/media/yue/Elements SE/008_Screening_data_CMIP6/Masks/landmask.nc")['mask']

def add_unified_colorbar(fig, ax, mesh, label):
    pos = ax.get_position()

    cax_height = 0.01
    cax_width = pos.width * 0.7
    cax_y = pos.y0 - cax_height - 0.035
    cax_x = pos.x0 + pos.width * 0.15

    cax = fig.add_axes([cax_x, cax_y, cax_width, cax_height])

    cbar = fig.colorbar(mesh, cax=cax, orientation='horizontal', extend='both')
    cbar.ax.text(0, 1.2, "Decrease", ha='left', va='bottom', fontsize=16, transform=cbar.ax.transAxes)
    cbar.ax.text(1, 1.2, "Increase", ha='right', va='bottom', fontsize=16, transform=cbar.ax.transAxes)
    cbar.ax.tick_params(labelsize=14)
    cbar.set_label(label, fontsize=14)

    return cbar

def draw_rectange_map(hotpoint, dd, fig=False, ax=None, extent=[-180, 180, -60, 90], linewi=1, lines='-'):
    if fig == False:
        fig = plt.figure(figsize=(12.27, 6.69), dpi=100, facecolor='white')
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
        ax.set_extent(extent, crs=ccrs.PlateCarree())
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.LAND, facecolor='#FFE9B5')

    ax.plot([hotpoint[dd][2], hotpoint[dd][3]], [hotpoint[dd][1], hotpoint[dd][1]], transform=ccrs.PlateCarree(),
            linewidth=linewi,
            color='k', ls=lines)
    ax.plot([hotpoint[dd][2], hotpoint[dd][3]], [hotpoint[dd][0], hotpoint[dd][0]], transform=ccrs.PlateCarree(),
            linewidth=linewi,
            color='k', ls=lines)
    ax.plot([hotpoint[dd][2], hotpoint[dd][2]], [hotpoint[dd][0], hotpoint[dd][1]], transform=ccrs.PlateCarree(),
            linewidth=linewi,
            color='k', ls=lines)
    ax.plot([hotpoint[dd][3], hotpoint[dd][3]], [hotpoint[dd][0], hotpoint[dd][1]], transform=ccrs.PlateCarree(),
            linewidth=linewi,
            color='k', ls=lines)

def draw_hotpoint_labels(hotpoint_label, fig=None, ax=None, fontsize=16, fontweight='bold', color='black'):
    for region_name, coords in hotpoint_label.items():
        lat, lon = coords
        ax.text(lon, lat, region_name,
                fontsize=fontsize,
                fontweight=fontweight,
                color=color,
                ha='center',
                va='center',
                transform=ccrs.PlateCarree(),)

def plot_figures12a(fig, ax):
    SPEI_SOC_HISTORICAL_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/SPEI/NORMALIZE_historical_Max_sensitivity_soc&SPEI120.nc")[
        'max_correlation'].__abs__()
    SSMI_SOC_HISTORICAL_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/SSMI/NORMALIZE_historical_Max_sensitivity_soc&SSMI120.nc")[
        'max_correlation'].__abs__()
    STI_SOC_HISTORICAL_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/STI/NORMALIZE_historical_Max_sensitivity_soc&STI120.nc")[
        'max_correlation'].__abs__()

    SPEI_SOC_SSP245_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/SPEI/NORMALIZE_ssp245_Max_sensitivity_soc&SPEI120.nc")[
        'max_correlation'].__abs__()
    SSMI_SOC_SSP245_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/SSMI/NORMALIZE_ssp245_Max_sensitivity_soc&SSMI120.nc")[
        'max_correlation'].__abs__()
    STI_SOC_SSP245_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/STI/NORMALIZE_ssp245_Max_sensitivity_soc&STI120.nc")[
        'max_correlation'].__abs__()

    SPEI_SOC_SSP370_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/SPEI/NORMALIZE_ssp370_Max_sensitivity_soc&SPEI120.nc")[
        'max_correlation'].__abs__()
    SSMI_SOC_SSP370_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/SSMI/NORMALIZE_ssp370_Max_sensitivity_soc&SSMI120.nc")[
        'max_correlation'].__abs__()
    STI_SOC_SSP370_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/STI/NORMALIZE_ssp370_Max_sensitivity_soc&STI120.nc")[
        'max_correlation'].__abs__()

    SPEI_RH_HISTORICAL_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/rh/SPEI/NORMALIZE_historical_Max_sensitivity_rh&SPEI120.nc")[
        'max_correlation'].__abs__()
    SSMI_RH_HISTORICAL_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/rh/SSMI/NORMALIZE_historical_Max_sensitivity_rh&SSMI120.nc")[
        'max_correlation'].__abs__()
    STI_RH_HISTORICAL_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/rh/STI/NORMALIZE_historical_Max_sensitivity_rh&STI120.nc")[
        'max_correlation'].__abs__()

    SPEI_RH_SSP245_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/rh/SPEI/NORMALIZE_ssp245_Max_sensitivity_rh&SPEI120.nc")[
        'max_correlation'].__abs__()
    SSMI_RH_SSP245_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/rh/SSMI/NORMALIZE_ssp245_Max_sensitivity_rh&SSMI120.nc")[
        'max_correlation'].__abs__()
    STI_RH_SSP245_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/rh/STI/NORMALIZE_ssp245_Max_sensitivity_rh&STI120.nc")[
        'max_correlation'].__abs__()

    SPEI_RH_SSP370_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/rh/SPEI/NORMALIZE_ssp370_Max_sensitivity_rh&SPEI120.nc")[
        'max_correlation'].__abs__()
    SSMI_RH_SSP370_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/rh/SSMI/NORMALIZE_ssp370_Max_sensitivity_rh&SSMI120.nc")[
        'max_correlation'].__abs__()
    STI_RH_SSP370_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/rh/STI/NORMALIZE_ssp370_Max_sensitivity_rh&STI120.nc")[
        'max_correlation'].__abs__()

    # 计算全球平均和标准差
    def calculate_stats(ds):
        mean = ds.mean(dim=['lat', 'lon']).item()
        std = ds.std(dim=['lat', 'lon']).item()
        return mean, std

    # SOC统计数据
    SPEI_SOC_HISTORICAL_MEAN, SPEI_SOC_HISTORICAL_STD = calculate_stats(SPEI_SOC_HISTORICAL_SEN)
    SSMI_SOC_HISTORICAL_MEAN, SSMI_SOC_HISTORICAL_STD = calculate_stats(SSMI_SOC_HISTORICAL_SEN)
    STI_SOC_HISTORICAL_MEAN, STI_SOC_HISTORICAL_STD = calculate_stats(STI_SOC_HISTORICAL_SEN)

    SPEI_SOC_SSP245_MEAN, SPEI_SOC_SSP245_STD = calculate_stats(SPEI_SOC_SSP245_SEN)
    SSMI_SOC_SSP245_MEAN, SSMI_SOC_SSP245_STD = calculate_stats(SSMI_SOC_SSP245_SEN)
    STI_SOC_SSP245_MEAN, STI_SOC_SSP245_STD = calculate_stats(STI_SOC_SSP245_SEN)

    SPEI_SOC_SSP370_MEAN, SPEI_SOC_SSP370_STD = calculate_stats(SPEI_SOC_SSP370_SEN)
    SSMI_SOC_SSP370_MEAN, SSMI_SOC_SSP370_STD = calculate_stats(SSMI_SOC_SSP370_SEN)
    STI_SOC_SSP370_MEAN, STI_SOC_SSP370_STD = calculate_stats(STI_SOC_SSP370_SEN)

    # RH统计数据
    SPEI_RH_HISTORICAL_MEAN, SPEI_RH_HISTORICAL_STD = calculate_stats(SPEI_RH_HISTORICAL_SEN)
    SSMI_RH_HISTORICAL_MEAN, SSMI_RH_HISTORICAL_STD = calculate_stats(SSMI_RH_HISTORICAL_SEN)
    STI_RH_HISTORICAL_MEAN, STI_RH_HISTORICAL_STD = calculate_stats(STI_RH_HISTORICAL_SEN)

    SPEI_RH_SSP245_MEAN, SPEI_RH_SSP245_STD = calculate_stats(SPEI_RH_SSP245_SEN)
    SSMI_RH_SSP245_MEAN, SSMI_RH_SSP245_STD = calculate_stats(SSMI_RH_SSP245_SEN)
    STI_RH_SSP245_MEAN, STI_RH_SSP245_STD = calculate_stats(STI_RH_SSP245_SEN)

    SPEI_RH_SSP370_MEAN, SPEI_RH_SSP370_STD = calculate_stats(SPEI_RH_SSP370_SEN)
    SSMI_RH_SSP370_MEAN, SSMI_RH_SSP370_STD = calculate_stats(SSMI_RH_SSP370_SEN)
    STI_RH_SSP370_MEAN, STI_RH_SSP370_STD = calculate_stats(STI_RH_SSP370_SEN)

    scenarios = ['Historical', 'SSP2-4.5', 'SSP3-7.0']

    # SOC数据和误差
    soc_data = [
        [SPEI_SOC_HISTORICAL_MEAN, SSMI_SOC_HISTORICAL_MEAN, STI_SOC_HISTORICAL_MEAN],
        [SPEI_SOC_SSP245_MEAN, SSMI_SOC_SSP245_MEAN, STI_SOC_SSP245_MEAN],
        [SPEI_SOC_SSP370_MEAN, SSMI_SOC_SSP370_MEAN, STI_SOC_SSP370_MEAN]
    ]

    soc_errors = [
        [SPEI_SOC_HISTORICAL_STD, SSMI_SOC_HISTORICAL_STD, STI_SOC_HISTORICAL_STD],
        [SPEI_SOC_SSP245_STD, SSMI_SOC_SSP245_STD, STI_SOC_SSP245_STD],
        [SPEI_SOC_SSP370_STD, SSMI_SOC_SSP370_STD, STI_SOC_SSP370_STD]
    ]

    # RH数据和误差
    rh_data = [
        [SPEI_RH_HISTORICAL_MEAN, SSMI_RH_HISTORICAL_MEAN, STI_RH_HISTORICAL_MEAN],
        [SPEI_RH_SSP245_MEAN, SSMI_RH_SSP245_MEAN, STI_RH_SSP245_MEAN],
        [SPEI_RH_SSP370_MEAN, SSMI_RH_SSP370_MEAN, STI_RH_SSP370_MEAN]
    ]

    rh_errors = [
        [SPEI_RH_HISTORICAL_STD, SSMI_RH_HISTORICAL_STD, STI_RH_HISTORICAL_STD],
        [SPEI_RH_SSP245_STD, SSMI_RH_SSP245_STD, STI_RH_SSP245_STD],
        [SPEI_RH_SSP370_STD, SSMI_RH_SSP370_STD, STI_RH_SSP370_STD]
    ]

    # Spatial SD describes grid-cell heterogeneity, not inferential uncertainty.
    # It is therefore not drawn as an error bar on these spatial means.
    bar_width = 0.11
    index = np.arange(len(scenarios))
    colors = ['#fca525', '#27c5cd', '#eb4116']

    # SOC and Rh are shown side by side; signs retain the direction of association.
    for i, drought_idx in enumerate(['SPEI', 'SSMI', 'STI']):
        # 获取当前指数的所有情景的值
        soc_values = [soc_data[j][i] for j in range(len(scenarios))]
        bars = ax.bar(index + 2 * i * bar_width,
                      soc_values,
                      width=bar_width,
                      color=colors[i],
                      edgecolor='black',
                      label=f'SOC-{drought_idx}' if i == 0 else "")

        # 在柱体端点添加数值标签
        for j, value in enumerate(soc_values):
            ax.text(index[j] + 2 * i * bar_width,
                    value + (0.005 if value >= 0 else -0.005),
                    f'{value:.2f}',
                    ha='center',
                    va='bottom' if value >= 0 else 'top',
                    fontsize=9)

    # Rh bars use hatching and retain their original signed values.
    for i, drought_idx in enumerate(['SPEI', 'SSMI', 'STI']):
        # 获取当前指数的所有情景的值
        rh_values = [rh_data[j][i] for j in range(len(scenarios))]
        bars = ax.bar(index + (2 * i + 1) * bar_width,
                      rh_values,
                      width=bar_width,
                      color=colors[i],
                      edgecolor='black',
                      alpha=0.7,
                      hatch='///',
                      label=f'RH-{drought_idx}' if i == 0 else "")

        # 在柱体端点添加数值标签
        for j, value in enumerate(rh_values):
            ax.text(index[j] + (2 * i + 1) * bar_width,
                    value + (0.005 if value >= 0 else -0.005),
                    f'{value:.2f}',
                    ha='center',
                    va='bottom' if value >= 0 else 'top',
                    fontsize=9)

    # 添加标签和标题
    ax.set_xlabel('Scenario', fontsize=16)
    ax.set_xticks(index + 2.5 * bar_width)
    ax.set_xticklabels(scenarios, fontsize=16)

    # 设置上下边框与右边框不显示
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # 添加横轴参考线
    ax.axhline(y=0, color='k', linewidth=0.8)

    ax.tick_params(axis='y', labelsize=16)

    # 添加图例（简化）
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=colors[0], edgecolor='black', label='SPEI'),
        Patch(facecolor=colors[1], edgecolor='black', label='SSMI'),
        Patch(facecolor=colors[2], edgecolor='black', label='STI'),
        Patch(facecolor='white', edgecolor='black', hatch='///', label='RH'),
        Patch(facecolor='white', edgecolor='black', label='SOC')
    ]
    ax.legend(handles=legend_elements,
              loc='upper center',
              bbox_to_anchor=(1.07, -0.15),
              ncol=5,
              fontsize=18,
              frameon=False)

    # 添加网格线
    ax.grid(True, linestyle='--', alpha=0.6, axis='y')

    # 添加标题
    ax.set_title('Spatial mean selected association magnitude, mean(|r*|)', fontsize=16, pad=15)

    # 添加图例标识
    ax.text(-0.15, 1.08, '(a)',
            fontweight='bold',
            transform=ax.transAxes,
            fontsize=22,
            va='top', ha='left')

    # 自动调整布局
    fig.tight_layout()

    return fig, ax


def plot_figures12b(fig, ax):
    SPEI_SOC_HISTORICAL_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/SPEI/NORMALIZE_historical_Max_sensitivity_soc&SPEI120.nc")[
        'max_scale']
    SSMI_SOC_HISTORICAL_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/SSMI/NORMALIZE_historical_Max_sensitivity_soc&SSMI120.nc")[
        'max_scale']
    STI_SOC_HISTORICAL_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/STI/NORMALIZE_historical_Max_sensitivity_soc&STI120.nc")[
        'max_scale']

    SPEI_SOC_SSP245_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/SPEI/NORMALIZE_ssp245_Max_sensitivity_soc&SPEI120.nc")[
        'max_scale']
    SSMI_SOC_SSP245_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/SSMI/NORMALIZE_ssp245_Max_sensitivity_soc&SSMI120.nc")[
        'max_scale']
    STI_SOC_SSP245_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/STI/NORMALIZE_ssp245_Max_sensitivity_soc&STI120.nc")['max_scale']

    SPEI_SOC_SSP370_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/SPEI/NORMALIZE_ssp370_Max_sensitivity_soc&SPEI120.nc")[
        'max_scale']
    SSMI_SOC_SSP370_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/SSMI/NORMALIZE_ssp370_Max_sensitivity_soc&SSMI120.nc")[
        'max_scale']
    STI_SOC_SSP370_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/STI/NORMALIZE_ssp370_Max_sensitivity_soc&STI120.nc")['max_scale']

    SPEI_RH_HISTORICAL_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/rh/SPEI/NORMALIZE_historical_Max_sensitivity_rh&SPEI120.nc")[
        'max_scale']
    SSMI_RH_HISTORICAL_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/rh/SSMI/NORMALIZE_historical_Max_sensitivity_rh&SSMI120.nc")[
        'max_scale']
    STI_RH_HISTORICAL_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/rh/STI/NORMALIZE_historical_Max_sensitivity_rh&STI120.nc")[
        'max_scale']

    SPEI_RH_SSP245_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/rh/SPEI/NORMALIZE_ssp245_Max_sensitivity_rh&SPEI120.nc")['max_scale']
    SSMI_RH_SSP245_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/rh/SSMI/NORMALIZE_ssp245_Max_sensitivity_rh&SSMI120.nc")['max_scale']
    STI_RH_SSP245_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/rh/STI/NORMALIZE_ssp245_Max_sensitivity_rh&STI120.nc")['max_scale']

    SPEI_RH_SSP370_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/rh/SPEI/NORMALIZE_ssp370_Max_sensitivity_rh&SPEI120.nc")['max_scale']
    SSMI_RH_SSP370_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/rh/SSMI/NORMALIZE_ssp370_Max_sensitivity_rh&SSMI120.nc")['max_scale']
    STI_RH_SSP370_SEN = \
    xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/rh/STI/NORMALIZE_ssp370_Max_sensitivity_rh&STI120.nc")['max_scale']

    # 计算全球平均和标准差
    def calculate_stats(ds):
        mean = ds.mean(dim=['lat', 'lon']).item()
        std = ds.std(dim=['lat', 'lon']).item()
        return mean, std

    # SOC统计数据
    SPEI_SOC_HISTORICAL_MEAN, SPEI_SOC_HISTORICAL_STD = calculate_stats(SPEI_SOC_HISTORICAL_SEN)
    SSMI_SOC_HISTORICAL_MEAN, SSMI_SOC_HISTORICAL_STD = calculate_stats(SSMI_SOC_HISTORICAL_SEN)
    STI_SOC_HISTORICAL_MEAN, STI_SOC_HISTORICAL_STD = calculate_stats(STI_SOC_HISTORICAL_SEN)

    SPEI_SOC_SSP245_MEAN, SPEI_SOC_SSP245_STD = calculate_stats(SPEI_SOC_SSP245_SEN)
    SSMI_SOC_SSP245_MEAN, SSMI_SOC_SSP245_STD = calculate_stats(SSMI_SOC_SSP245_SEN)
    STI_SOC_SSP245_MEAN, STI_SOC_SSP245_STD = calculate_stats(STI_SOC_SSP245_SEN)

    SPEI_SOC_SSP370_MEAN, SPEI_SOC_SSP370_STD = calculate_stats(SPEI_SOC_SSP370_SEN)
    SSMI_SOC_SSP370_MEAN, SSMI_SOC_SSP370_STD = calculate_stats(SSMI_SOC_SSP370_SEN)
    STI_SOC_SSP370_MEAN, STI_SOC_SSP370_STD = calculate_stats(STI_SOC_SSP370_SEN)

    # RH统计数据
    SPEI_RH_HISTORICAL_MEAN, SPEI_RH_HISTORICAL_STD = calculate_stats(SPEI_RH_HISTORICAL_SEN)
    SSMI_RH_HISTORICAL_MEAN, SSMI_RH_HISTORICAL_STD = calculate_stats(SSMI_RH_HISTORICAL_SEN)
    STI_RH_HISTORICAL_MEAN, STI_RH_HISTORICAL_STD = calculate_stats(STI_RH_HISTORICAL_SEN)

    SPEI_RH_SSP245_MEAN, SPEI_RH_SSP245_STD = calculate_stats(SPEI_RH_SSP245_SEN)
    SSMI_RH_SSP245_MEAN, SSMI_RH_SSP245_STD = calculate_stats(SSMI_RH_SSP245_SEN)
    STI_RH_SSP245_MEAN, STI_RH_SSP245_STD = calculate_stats(STI_RH_SSP245_SEN)

    SPEI_RH_SSP370_MEAN, SPEI_RH_SSP370_STD = calculate_stats(SPEI_RH_SSP370_SEN)
    SSMI_RH_SSP370_MEAN, SSMI_RH_SSP370_STD = calculate_stats(SSMI_RH_SSP370_SEN)
    STI_RH_SSP370_MEAN, STI_RH_SSP370_STD = calculate_stats(STI_RH_SSP370_SEN)

    scenarios = ['Historical', 'SSP2-4.5', 'SSP3-7.0']

    # SOC数据和误差
    soc_data = [
        [SPEI_SOC_HISTORICAL_MEAN, SSMI_SOC_HISTORICAL_MEAN, STI_SOC_HISTORICAL_MEAN],
        [SPEI_SOC_SSP245_MEAN, SSMI_SOC_SSP245_MEAN, STI_SOC_SSP245_MEAN],
        [SPEI_SOC_SSP370_MEAN, SSMI_SOC_SSP370_MEAN, STI_SOC_SSP370_MEAN]
    ]

    soc_errors = [
        [SPEI_SOC_HISTORICAL_STD, SSMI_SOC_HISTORICAL_STD, STI_SOC_HISTORICAL_STD],
        [SPEI_SOC_SSP245_STD, SSMI_SOC_SSP245_STD, STI_SOC_SSP245_STD],
        [SPEI_SOC_SSP370_STD, SSMI_SOC_SSP370_STD, STI_SOC_SSP370_STD]
    ]

    # RH数据和误差
    rh_data = [
        [SPEI_RH_HISTORICAL_MEAN, SSMI_RH_HISTORICAL_MEAN, STI_RH_HISTORICAL_MEAN],
        [SPEI_RH_SSP245_MEAN, SSMI_RH_SSP245_MEAN, STI_RH_SSP245_MEAN],
        [SPEI_RH_SSP370_MEAN, SSMI_RH_SSP370_MEAN, STI_RH_SSP370_MEAN]
    ]

    rh_errors = [
        [SPEI_RH_HISTORICAL_STD, SSMI_RH_HISTORICAL_STD, STI_RH_HISTORICAL_STD],
        [SPEI_RH_SSP245_STD, SSMI_RH_SSP245_STD, STI_RH_SSP245_STD],
        [SPEI_RH_SSP370_STD, SSMI_RH_SSP370_STD, STI_RH_SSP370_STD]
    ]

    # Spatial SD describes grid-cell heterogeneity, not inferential uncertainty.
    # It is therefore not drawn as an error bar on these spatial means.
    bar_width = 0.11
    index = np.arange(len(scenarios))
    colors = ['#fca525', '#27c5cd', '#eb4116']  # 蓝、橙、绿

    # SOC and Rh are shown side by side. Accumulation timescales are always positive.
    for i, drought_idx in enumerate(['SPEI', 'SSMI', 'STI']):
        # 获取当前指数的所有情景的值
        soc_values = [soc_data[j][i] for j in range(len(scenarios))]
        bars = ax.bar(index + 2 * i * bar_width,
                      soc_values,
                      width=bar_width,
                      color=colors[i],
                      edgecolor='black',
                      label=f'SOC-{drought_idx}' if i == 0 else "")

        # 在柱体上方添加数值标签
        for j, value in enumerate(soc_values):
            ax.text(index[j] + 2 * i * bar_width,
                    value + 1.5,
                    f'{value:.1f}',
                    ha='center',
                    va='bottom',
                    fontsize=9)

    # Rh bars are distinguished by hatching, not by a sign inversion.
    for i, drought_idx in enumerate(['SPEI', 'SSMI', 'STI']):
        # 获取当前指数的所有情景的值
        rh_values = [rh_data[j][i] for j in range(len(scenarios))]
        bars = ax.bar(index + (2 * i + 1) * bar_width,
                      rh_values,
                      width=bar_width,
                      color=colors[i],
                      edgecolor='black',
                      alpha=0.7,
                      hatch='///',
                      label=f'RH-{drought_idx}' if i == 0 else "")

        # 在柱体上方添加数值标签
        for j, value in enumerate(rh_values):
            ax.text(index[j] + (2 * i + 1) * bar_width,
                    value + 1.5,
                    f'{value:.1f}',
                    ha='center',
                    va='bottom',
                    fontsize=9)

    # 添加标签和标题
    ax.set_xlabel('Scenario', fontsize=16)
    ax.set_xticks(index + 2.5 * bar_width)
    ax.set_xticklabels(scenarios, fontsize=16)

    # 设置上边框与右边框不显示
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # 添加横轴参考线
    ax.axhline(y=0, color='k', linewidth=0.8)

    ax.tick_params(axis='y', labelsize=16)

    # 添加网格线
    ax.grid(True, linestyle='--', alpha=0.6, axis='y')

    # 添加标题
    ax.set_title('Spatial mean maximum associated accumulation timescale (months)', fontsize=16, pad=15)

    # 添加图例标识
    ax.text(-0.15, 1.08, '(b)',
            fontweight='bold',
            transform=ax.transAxes,
            fontsize=22,
            va='top', ha='left')

    # 自动调整布局
    fig.tight_layout()

    return fig, ax


def plot_figures12c(fig, ax):
    SSMI_SOC_SSP370_SEN = xr.open_dataset(
        "/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/SSMI/NORMALIZE_ssp370_Max_sensitivity_soc&SSMI120.nc"
    )["max_correlation"]
    SSMI_SOC_SSP245_SEN = xr.open_dataset(
        "/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/SSMI/NORMALIZE_ssp245_Max_sensitivity_soc&SSMI120.nc"
    )["max_correlation"]
    SSMI_SOC_HISTORICAL_SEN = xr.open_dataset(
        "/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/SSMI/NORMALIZE_historical_Max_sensitivity_soc&SSMI120.nc"
    )["max_correlation"]

    diff = SSMI_SOC_SSP370_SEN.where(landmask == 1) - SSMI_SOC_HISTORICAL_SEN.where(landmask == 1)
    diff2 = SSMI_SOC_SSP245_SEN.where(landmask == 1) - SSMI_SOC_HISTORICAL_SEN.where(landmask == 1)

    ax.set_extent([-170, 180, -60, 90], crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND, facecolor="white", edgecolor="black", linewidth=0.5)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.5)

    lons = diff.lon.values
    lats = diff.lat.values
    lon_min, lon_max = lons.min(), lons.max()
    lat_min, lat_max = lats.min(), lats.max()
    d_lon = (lon_max - lon_min) / len(lons)
    d_lat = (lat_max - lat_min) / len(lats)

    colors_class = ["#FF6B6B", "#4ECDC4", "#C8D6E5"]
    pos_count = neg_count = zero_count = 0

    for i in range(len(lats)):
        for j in range(len(lons)):
            v = diff[i, j].item()
            if np.isnan(v) and (landmask[i, j] == 0):
                continue

            if np.isnan(v) and (landmask[i, j] == 1):
                facecolor = colors_class[2]
                zero_count += 1
            else:
                if v > 0:
                    facecolor = colors_class[0]
                    pos_count += 1
                elif v < 0:
                    facecolor = colors_class[1]
                    neg_count += 1
                else:
                    facecolor = colors_class[2]
                    zero_count += 1

            patch = patches.FancyBboxPatch(
                (lons[j] - d_lon / 2, lats[i] - d_lat / 2),
                d_lon, d_lat,
                edgecolor="none",
                facecolor=facecolor,
                alpha=1,
                boxstyle="round,pad=0.05,rounding_size=0.3",
                transform=ccrs.PlateCarree(),
                zorder=1,
            )
            ax.add_patch(patch)

    hotpoint = {
        "AMZ-SE": [-24.1, 1.5, -60.5, -34.5],
        "NAMS": [18.3, 34.9, -119.9, -78.7],
        "AUS": [-38.8, -10.2, 114.1, 154.5],
        "SE-CHN": [21.0, 34.0, 99.4, 123.1],
        "S-AF": [-35.0, -12.8, 9.7, 50.6],
        "MED": [35.2, 56.1, -12.5, 70.3],
    }
    hotpoint_label = {
        "AMZ-SE": [5, -35],
        "NAMS": [26.6, -133],
        "AUS": [-24.5, 104],
        "SE-CHN": [27.5, 140],
        "S-AF": [-40, 30.2],
        "MED": [45.7, -25],
    }
    for k in hotpoint.keys():
        draw_rectange_map(hotpoint, k, fig=fig, ax=ax, extent=[-180, 180, -60, 90])

    pie_ax = ax.inset_axes([-0.08, -0.02, 0.4, 0.4])
    pie_ax.pie(
        [pos_count, neg_count, zero_count],
        colors=colors_class, autopct="%1.1f%%", startangle=90,
        wedgeprops={"edgecolor": "w", "alpha": 0.8, "linewidth": 0.5, "width": 0.6},
        textprops={"fontsize": 14},
    )

    bar_ax = ax.inset_axes([0.01, 0.27, 0.015, 0.3])
    bar_ax.axis("off")
    color_labels = ["Increase", "Decrease", "NS"]
    for i, (c, lab) in enumerate(zip(colors_class, color_labels)):
        y0 = 1 - (i + 1) / 3
        bar_ax.add_patch(patches.Rectangle((0, y0), 1, 1 / 3, color=c, ec="none"))
        bar_ax.text(1.2, y0 + 1 / 6, lab, va="center", ha="left", fontsize=11)

    valid_all = np.concatenate([
        diff.values[np.isfinite(diff.values)],
        diff2.values[np.isfinite(diff2.values)]
    ])
    xmin = np.nanpercentile(valid_all, 1) if valid_all.size else -1.0
    xmax = np.nanpercentile(valid_all, 99) if valid_all.size else 1.0
    if xmin == xmax:
        xmin, xmax = xmin - 1e-3, xmax + 1e-3

    def lonlat_to_axesxy(lon, lat):
        pt = ax.projection.transform_points(
            ccrs.PlateCarree(), np.asarray([lon]), np.asarray([lat])
        )[0, :2]
        disp = ax.transData.transform(pt)
        axxy = ax.transAxes.inverted().transform(disp)
        return float(axxy[0]), float(axxy[1])

    inset_offset = {
        "AMZ-SE": (+0.07, -0.16),
        "NAMS": (-0.07, -0.10),
        "AUS": (-0.12, +0.06),
        "SE-CHN": (+0.11, -0.04),
        "S-AF": (+0.07, -0.09),
        "MED": (-0.17, -0.07),
    }
    inset_w, inset_h = 0.10, 0.12

    col_585, col_126 = "#d35400", "#16a085"
    ls_585, ls_126 = "-", "--"

    for idx, (reg, (lat0, lat1, lon0, lon1)) in enumerate(hotpoint.items()):
        vals_585 = diff.sel(lat=slice(lat0, lat1), lon=slice(lon0, lon1)).values
        vals_126 = diff2.sel(lat=slice(lat0, lat1), lon=slice(lon0, lon1)).values
        vals_585 = vals_585[np.isfinite(vals_585)]
        vals_126 = vals_126[np.isfinite(vals_126)]
        if (vals_585.size < 5) and (vals_126.size < 5):
            continue

        x_grid = np.linspace(xmin, xmax, 200)

        def density(vals):
            if vals.size < 5:
                return np.zeros_like(x_grid)
            try:
                from scipy.stats import gaussian_kde
                kde = gaussian_kde(vals)
                return kde.evaluate(x_grid)
            except Exception:
                hist, edges = np.histogram(vals, bins=30, range=(xmin, xmax), density=True)
                centers = 0.5 * (edges[:-1] + edges[1:])
                smooth = np.convolve(hist, np.ones(5) / 5.0, mode="same")
                return np.interp(x_grid, centers, smooth)

        y585 = density(vals_585)
        y126 = density(vals_126)
        ymax = max(np.nanmax(y585) if y585.size else 0, np.nanmax(y126) if y126.size else 0, 1e-12)
        y585 = y585 / ymax
        y126 = y126 / ymax

        c_lat = 0.5 * (lat0 + lat1)
        c_lon = 0.5 * (lon0 + lon1)
        cx, cy = lonlat_to_axesxy(c_lon, c_lat)
        dx, dy = inset_offset.get(reg, (0.08, 0.05))
        x0 = np.clip(cx + dx - inset_w / 2, 0.01, 0.99 - inset_w)
        y0 = np.clip(cy + dy - inset_h / 2, 0.01, 0.99 - inset_h)

        iax = ax.inset_axes([x0, y0, inset_w, inset_h])
        iax.set_facecolor((1, 1, 1, 0.65))
        iax.plot(x_grid, y585, lw=1.6, ls=ls_585, color=col_585, label="SSP3-7.0")
        iax.fill_between(x_grid, 0, y585, alpha=0.18, color=col_585)
        iax.plot(x_grid, y126, lw=1.6, ls=ls_126, color=col_126, label="SSP2-4.5")
        iax.fill_between(x_grid, 0, y126, alpha=0.18, color=col_126)
        iax.axvline(0, color="k", lw=0.8, ls="--", alpha=0.6)

        iax.set_xlim(xmin, xmax)
        iax.set_ylim(0, 1.05)
        iax.set_xticks([t for t in [-1.0, -0.5, 0, 0.5, 1.0] if xmin <= t <= xmax])
        iax.set_yticks([0, 1])
        iax.tick_params(axis="x", labelsize=12, pad=1, rotation=45)
        iax.tick_params(axis="y", labelsize=12, pad=1)
        for s in ["top", "right"]:
            iax.spines[s].set_visible(False)

        if idx == 0:
            iax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.8), bbox_transform=iax.transAxes, fontsize=10,
                       frameon=False, handlelength=1.6)

        iax.text(0.02, 1.05, reg, fontsize=10, weight='bold',
                 va='top', ha='left', transform=iax.transAxes)

        for spine in ["top", "right"]:
            iax.spines[spine].set_visible(False)

    gl = ax.gridlines(
        crs=ccrs.PlateCarree(), draw_labels=True,
        linewidth=0.5, color="gray", alpha=0.5, linestyle="--"
    )
    gl.top_labels = False
    gl.right_labels = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {"size": 20, "color": "black"}
    gl.ylabel_style = {"size": 20, "color": "black"}

    ax.text(
        -0.05, 1.05, '(c)', fontweight="bold",
        transform=ax.transAxes, fontsize=22, va="top", ha="left",
        bbox=dict(facecolor="white", alpha=0.8, edgecolor="none"),
    )

    ax.set_title("Changes in the selected association magnitude of SOC with SSMI", fontsize=16, pad=15)
    return None

def plot_figures12d(fig, ax):
    SSMI_SOC_SSP370_SEN = \
    xr.open_dataset("/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/SPEI/NORMALIZE_ssp370_Max_sensitivity_soc&SPEI120.nc")[
        'max_correlation']
    SSMI_SOC_HISTORICAL_SEN = \
    xr.open_dataset("/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/SPEI/NORMALIZE_historical_Max_sensitivity_soc&SPEI120.nc")[
        'max_correlation']

    SSMI_SOC_SSP370_SEN = SSMI_SOC_SSP370_SEN.where(landmask == 1) - SSMI_SOC_HISTORICAL_SEN.where(landmask == 1)

    ax.set_extent([-170, 180, -60, 90], crs=ccrs.PlateCarree())

    lons = SSMI_SOC_SSP370_SEN.lon.values
    lats = SSMI_SOC_SSP370_SEN.lat.values

    lon_min, lon_max = SSMI_SOC_SSP370_SEN.lon.min().values, SSMI_SOC_SSP370_SEN.lon.max().values
    lat_min, lat_max = SSMI_SOC_SSP370_SEN.lat.min().values, SSMI_SOC_SSP370_SEN.lat.max().values

    cmap_change = mpl.colors.ListedColormap(
        ['#70D3C2', '#92D9C0', '#A8CEB4', '#BEC3A8', '#CCB69C', '#D6A792', '#E09888', '#EB897F', '#F57A76'])
    cmap_change.set_over('#FF6B6B')
    cmap_change.set_under('#4ECDC4')

    levels_change = [-0.9, -0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9]

    cmap = cmap_change
    norm = mpl.colors.BoundaryNorm(levels_change, cmap.N)
    vmin = SSMI_SOC_SSP370_SEN.min().item()
    vmax = SSMI_SOC_SSP370_SEN.max().item()

    d_lon = (lon_max - lon_min) / len(SSMI_SOC_SSP370_SEN.lon)
    d_lat = (lat_max - lat_min) / len(SSMI_SOC_SSP370_SEN.lat)

    for i in range(len(lats)):
        for j in range(len(lons)):
            value = SSMI_SOC_SSP370_SEN[i, j].item()
            if landmask[i, j] != 1:
                continue
            if np.isnan(value):
                patch = patches.FancyBboxPatch(
                    (lons[j] - d_lon / 2, lats[i] - d_lat / 2),
                    d_lon, d_lat,
                    edgecolor='none',
                    facecolor='#C8D6E5',
                    alpha=1,
                    boxstyle="round,pad=0.05,rounding_size=0.3",
                    transform=ccrs.PlateCarree(),
                    zorder=1
                )
                ax.add_patch(patch)
                continue
            patch = patches.FancyBboxPatch(
                (lons[j] - d_lon / 2, lats[i] - d_lat / 2),
                d_lon, d_lat,
                edgecolor='none',
                facecolor=cmap(norm(value)),
                alpha=1,
                boxstyle="round,pad=0.05,rounding_size=0.3",
                transform=ccrs.PlateCarree(),
                zorder=1
            )
            ax.add_patch(patch)

    positive_count = np.sum(SSMI_SOC_SSP370_SEN.values > 0)
    negative_count = np.sum(SSMI_SOC_SSP370_SEN.values < 0)
    zero_count = np.sum(landmask == 1) - positive_count - negative_count

    colors = ['#FF6B6B', '#4ECDC4', '#C8D6E5']
    pie_ax = ax.inset_axes([-0.05, 0.05, 0.4, 0.4])
    pie_ax.pie(
        [positive_count, negative_count, zero_count],
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops={'edgecolor': 'w', 'alpha': 0.8, 'linewidth': 0.5, 'width': 0.6},
        textprops={'fontsize': 12}
    )

    ax.add_feature(cfeature.LAND, facecolor='white', edgecolor='black', linewidth=0.5)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)
    ax.set_title("Changes in the selected association magnitude of SOC with SPEI", fontsize=16, pad=15)

    hotpoint = {
        'AMZ-SE': [-24.1, 1.5, -60.5, -34.5, ],
        'NAMS': [18.3, 34.9, -119.9, -78.7, ],
        'AUS': [-38.8, -10.2, 114.1, 154.5, ],
        'SE-CHN': [21.0, 34.0, 99.4, 123.1, ],
        'S-AF': [-35.0, -12.8, 9.7, 50.6, ],
        'MED': [35.2, 56.1, -12.5, 70.3, ]
    }

    hotpoint_label = {
        'AMZ-SE': [5, -35, ],
        'NAMS': [26.6, -133],
        'AUS': [-24.5, 104, ],
        'SE-CHN': [27.5, 140, ],
        'S-AF': [-40, 30.2, ],
        'MED': [45.7, -25, ]
    }
    for dd in hotpoint.keys():
        draw_rectange_map(hotpoint, dd, fig=fig, ax=ax, extent=[-180, 180, -60, 90])

    draw_hotpoint_labels(hotpoint_label, fig=fig, ax=ax, fontsize=10)

    gl = ax.gridlines(
        crs=ccrs.PlateCarree(),
        draw_labels=True,
        linewidth=0.5, color='gray', alpha=0.5, linestyle='--'
    )
    gl.top_labels = False
    gl.right_labels = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size': 20, 'color': 'black'}
    gl.ylabel_style = {'size': 20, 'color': 'black'}

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array(np.array([]))
    cbar = add_unified_colorbar(fig, ax, sm, "")

    ax.text(-0.1, 1.1, '(d)',
            fontweight='bold',
            transform=ax.transAxes,
            fontsize=22,
            va='top', ha='left',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    return sm

def plot_figures12e(fig, ax):
    SSMI_SOC_SSP370_SEN = \
    xr.open_dataset("/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/STI/NORMALIZE_ssp370_Max_sensitivity_soc&STI120.nc")[
        'max_correlation']
    SSMI_SOC_HISTORICAL_SEN = \
    xr.open_dataset("/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/STI/NORMALIZE_historical_Max_sensitivity_soc&STI120.nc")[
        'max_correlation']

    SSMI_SOC_SSP370_SEN = SSMI_SOC_SSP370_SEN.where(landmask == 1) - SSMI_SOC_HISTORICAL_SEN.where(landmask == 1)

    ax.set_extent([-170, 180, -60, 90], crs=ccrs.PlateCarree())

    lons = SSMI_SOC_SSP370_SEN.lon.values
    lats = SSMI_SOC_SSP370_SEN.lat.values

    lon_min, lon_max = SSMI_SOC_SSP370_SEN.lon.min().values, SSMI_SOC_SSP370_SEN.lon.max().values
    lat_min, lat_max = SSMI_SOC_SSP370_SEN.lat.min().values, SSMI_SOC_SSP370_SEN.lat.max().values

    cmap_change = mpl.colors.ListedColormap(
        ['#70D3C2', '#92D9C0', '#A8CEB4', '#BEC3A8', '#CCB69C', '#D6A792', '#E09888', '#EB897F', '#F57A76'])
    cmap_change.set_over('#FF6B6B')
    cmap_change.set_under('#4ECDC4')
    levels_change = [-0.9, -0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9]

    cmap = cmap_change
    norm = mpl.colors.BoundaryNorm(levels_change, cmap.N)
    vmin = SSMI_SOC_SSP370_SEN.min().item()
    vmax = SSMI_SOC_SSP370_SEN.max().item()

    d_lon = (lon_max - lon_min) / len(SSMI_SOC_SSP370_SEN.lon)
    d_lat = (lat_max - lat_min) / len(SSMI_SOC_SSP370_SEN.lat)

    for i in range(len(lats)):
        for j in range(len(lons)):
            value = SSMI_SOC_SSP370_SEN[i, j].item()
            if landmask[i, j] != 1:
                continue
            if np.isnan(value):
                patch = patches.FancyBboxPatch(
                    (lons[j] - d_lon / 2, lats[i] - d_lat / 2),
                    d_lon, d_lat,
                    edgecolor='none',
                    facecolor='#C8D6E5',
                    alpha=1,
                    boxstyle="round,pad=0.05,rounding_size=0.3",
                    transform=ccrs.PlateCarree(),
                    zorder=1
                )
                ax.add_patch(patch)
                continue
            patch = patches.FancyBboxPatch(
                (lons[j] - d_lon / 2, lats[i] - d_lat / 2),
                d_lon, d_lat,
                edgecolor='none',
                facecolor=cmap(norm(value)),
                alpha=1,
                boxstyle="round,pad=0.05,rounding_size=0.3",
                transform=ccrs.PlateCarree(),
                zorder=1
            )
            ax.add_patch(patch)

    positive_count = np.sum(SSMI_SOC_SSP370_SEN.values > 0)
    negative_count = np.sum(SSMI_SOC_SSP370_SEN.values < 0)
    zero_count = np.sum(landmask == 1) - positive_count - negative_count

    colors = ['#FF6B6B', '#4ECDC4', '#C8D6E5']
    pie_ax = ax.inset_axes([-0.05, 0.05, 0.4, 0.4])

    pie_ax.pie(
        [positive_count, negative_count, zero_count],
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops={'edgecolor': 'w', 'alpha': 0.8, 'linewidth': 0.5, 'width': 0.6},
        textprops={'fontsize': 12}
    )

    ax.add_feature(cfeature.LAND, facecolor='white', edgecolor='black', linewidth=0.5)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)
    ax.set_title("Changes in the selected association magnitude of SOC with STI", fontsize=16, pad=15)

    hotpoint = {
        'AMZ-SE': [-24.1, 1.5, -60.5, -34.5, ],
        'NAMS': [18.3, 34.9, -119.9, -78.7, ],
        'AUS': [-38.8, -10.2, 114.1, 154.5, ],
        'SE-CHN': [21.0, 34.0, 99.4, 123.1, ],
        'S-AF': [-35.0, -12.8, 9.7, 50.6, ],
        'MED': [35.2, 56.1, -12.5, 70.3, ]
    }

    hotpoint_label = {
        'AMZ-SE': [5, -35, ],
        'NAMS': [26.6, -133],
        'AUS': [-24.5, 104, ],
        'SE-CHN': [27.5, 140, ],
        'S-AF': [-40, 30.2, ],
        'MED': [45.7, -25, ]
    }
    for dd in hotpoint.keys():
        draw_rectange_map(hotpoint, dd, fig=fig, ax=ax, extent=[-180, 180, -60, 90])

    draw_hotpoint_labels(hotpoint_label, fig=fig, ax=ax, fontsize=10)

    gl = ax.gridlines(
        crs=ccrs.PlateCarree(),
        draw_labels=True,
        linewidth=0.5, color='gray', alpha=0.5, linestyle='--'
    )
    gl.top_labels = False
    gl.right_labels = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size': 20, 'color': 'black'}
    gl.ylabel_style = {'size': 20, 'color': 'black'}

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array(np.array([]))
    cbar = add_unified_colorbar(fig, ax, sm, "")

    ax.text(-0.1, 1.1, '(e)',
            fontweight='bold',
            transform=ax.transAxes,
            fontsize=22,
            va='top', ha='left',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    return sm

def create_figures12():
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams['axes.edgecolor'] = 'black'
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Arial'],
        'font.sans-serif': ['Times New Roman'],
    })

    fig = plt.figure(figsize=(16, 20))

    gs = gridspec.GridSpec(3, 2, figure=fig, height_ratios=[3, 4, 3], wspace=0.15, hspace=0.2, top=0.95, bottom=0.07,
                           left=0.1, right=0.99)

    ax1 = fig.add_subplot(gs[0])
    mesh1 = plot_figures12a(fig, ax1)

    ax2 = fig.add_subplot(gs[1])
    mesh2 = plot_figures12b(fig, ax2)

    ax3 = fig.add_subplot(gs[1, :], projection=ccrs.Robinson(central_longitude=10))
    mesh3 = plot_figures12c(fig, ax3)

    ax4 = fig.add_subplot(gs[4], projection=ccrs.Robinson(central_longitude=10))
    mesh4 = plot_figures12d(fig, ax4)

    ax5 = fig.add_subplot(gs[5], projection=ccrs.Robinson(central_longitude=10))
    mesh5 = plot_figures12e(fig, ax5)

    ax3_position = ax3.get_position()
    new_ax3_position = [ax3_position.x0, ax3_position.y0 - 0.05, ax3_position.width, ax3_position.height]
    ax3.set_position(new_ax3_position)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    pdf_path = os.path.join(OUTPUT_DIR, "FigureS12.pdf")
    plt.savefig(pdf_path, dpi=600, bbox_inches='tight')
    png_path = os.path.join(OUTPUT_DIR, "FigureS12.png")
    plt.savefig(png_path, dpi=600, bbox_inches='tight')

    print(f"Figure saved to: {png_path}")
    plt.close()

if __name__ == '__main__':
    create_figures12()
