"""Create manuscript Supplementary Figure S16.

Converted from PlotSupplementaryFig13&14&15.ipynb. Only complete figures
are saved to res/eiar_figs.
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

def add_unified_colorbar(fig, ax, mesh, label, y_offset=0.035):
    pos = ax.get_position()

    cax_height = 0.01
    cax_width = pos.width * 0.7
    cax_y = pos.y0 - cax_height - y_offset
    cax_x = pos.x0 + pos.width * 0.15

    cax = fig.add_axes([cax_x, cax_y, cax_width, cax_height])

    cbar = fig.colorbar(mesh, cax=cax, orientation='horizontal', extend='both')
    cbar.ax.text(0, 1.2, "Decrease", ha='left', va='bottom', fontsize=14, transform=cbar.ax.transAxes)
    cbar.ax.text(1, 1.2, "Increase", ha='right', va='bottom', fontsize=14, transform=cbar.ax.transAxes)
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

    ax.plot([hotpoint[dd][2], hotpoint[dd][3]], [hotpoint[dd][1], hotpoint[dd][1]], transform=ccrs.PlateCarree(), linewidth=linewi,
            color='k', ls=lines)
    ax.plot([hotpoint[dd][2], hotpoint[dd][3]], [hotpoint[dd][0], hotpoint[dd][0]], transform=ccrs.PlateCarree(), linewidth=linewi,
            color='k', ls=lines)
    ax.plot([hotpoint[dd][2], hotpoint[dd][2]], [hotpoint[dd][0], hotpoint[dd][1]], transform=ccrs.PlateCarree(), linewidth=linewi,
            color='k', ls=lines)
    ax.plot([hotpoint[dd][3], hotpoint[dd][3]], [hotpoint[dd][0], hotpoint[dd][1]], transform=ccrs.PlateCarree(), linewidth=linewi,
            color='k', ls=lines)

def draw_hotpoint_labels(hotpoint_label, fig=None, ax=None, fontsize=14, fontweight='bold', color='black'):
    for region_name, coords in hotpoint_label.items():
        lat, lon = coords
        ax.text(lon, lat, region_name,
                fontsize=fontsize,
                fontweight=fontweight,
                color=color,
                ha='center',
                va='center',
                transform=ccrs.PlateCarree(),)

def plot_figures16a(fig, ax):
    SSMI_SOC_SSP370_SEN = xr.open_dataset("/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/SSMI/NORMALIZE_ssp245_Max_sensitivity_soc&SSMI120.nc")['max_correlation']
    SSMI_SOC_HISTORICAL_SEN = xr.open_dataset("/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/SSMI/NORMALIZE_historical_Max_sensitivity_soc&SSMI120.nc")['max_correlation']

    SSMI_SOC_SSP370_SEN = SSMI_SOC_SSP370_SEN.where(landmask == 1) - SSMI_SOC_HISTORICAL_SEN.where(landmask == 1)

    ax.set_extent([-170, 180, -60, 90], crs=ccrs.PlateCarree())

    lons = SSMI_SOC_SSP370_SEN.lon.values
    lats = SSMI_SOC_SSP370_SEN.lat.values

    lon_min, lon_max = SSMI_SOC_SSP370_SEN.lon.min().values, SSMI_SOC_SSP370_SEN.lon.max().values
    lat_min, lat_max = SSMI_SOC_SSP370_SEN.lat.min().values, SSMI_SOC_SSP370_SEN.lat.max().values

    cmap_change = mpl.colors.ListedColormap(['#70D3C2', '#92D9C0', '#A8CEB4', '#BEC3A8', '#CCB69C', '#D6A792', '#E09888', '#EB897F', '#F57A76'])
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
                    (lons[j] - d_lon/2, lats[i] - d_lat/2),
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
                (lons[j] - d_lon/2, lats[i] - d_lat/2),
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
        wedgeprops={'edgecolor': 'w', 'alpha':0.8, 'linewidth': 0.5, 'width':0.6},
        textprops={'fontsize': 11}
    )

    ax.add_feature(cfeature.LAND, facecolor='white', edgecolor='black', linewidth=0.5)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)
    ax.set_title("Changes in the selected assiciation magnitude of $SOC$ with SSMI(SSP3-7.0)", fontsize=14, pad=15)

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
    gl.xlabel_style = {'size': 16, 'color': 'black'}
    gl.ylabel_style = {'size': 16, 'color': 'black'}

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array(np.array([]))

    ax.text(-0.05, 1.05, '(a)',
            fontweight='bold',
            transform=ax.transAxes,
            fontsize=18,
            va='top', ha='left',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    return sm

def plot_figures16b(fig, ax):
    SSMI_SOC_SSP370_SEN = xr.open_dataset("/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/SSMI/NORMALIZE_ssp245_Max_sensitivity_soc&SSMI120.nc")['max_correlation']
    SSMI_SOC_HISTORICAL_SEN = xr.open_dataset("/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/SSMI/NORMALIZE_historical_Max_sensitivity_soc&SSMI120.nc")['max_correlation']

    SSMI_SOC_SSP370_SEN = SSMI_SOC_SSP370_SEN.where(landmask == 1) - SSMI_SOC_HISTORICAL_SEN.where(landmask == 1)

    ax.set_extent([-170, 180, -60, 90], crs=ccrs.PlateCarree())

    lons = SSMI_SOC_SSP370_SEN.lon.values
    lats = SSMI_SOC_SSP370_SEN.lat.values

    lon_min, lon_max = SSMI_SOC_SSP370_SEN.lon.min().values, SSMI_SOC_SSP370_SEN.lon.max().values
    lat_min, lat_max = SSMI_SOC_SSP370_SEN.lat.min().values, SSMI_SOC_SSP370_SEN.lat.max().values

    cmap_change = mpl.colors.ListedColormap(['#70D3C2', '#92D9C0', '#A8CEB4', '#BEC3A8', '#CCB69C', '#D6A792', '#E09888', '#EB897F', '#F57A76'])
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
                    (lons[j] - d_lon/2, lats[i] - d_lat/2),
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
                (lons[j] - d_lon/2, lats[i] - d_lat/2),
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
        wedgeprops={'edgecolor': 'w', 'alpha':0.8, 'linewidth': 0.5, 'width':0.6},
        textprops={'fontsize': 11}
    )

    ax.add_feature(cfeature.LAND, facecolor='white', edgecolor='black', linewidth=0.5)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)
    ax.set_title("Changes in the selected assiciation magnitude of $SOC$ with SSMI(SSP2-4.5)", fontsize=14, pad=15)

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
    gl.xlabel_style = {'size': 16, 'color': 'black'}
    gl.ylabel_style = {'size': 16, 'color': 'black'}

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array(np.array([]))

    ax.text(-0.05, 1.05, '(b)',
            fontweight='bold',
            transform=ax.transAxes,
            fontsize=18,
            va='top', ha='left',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    return sm

def plot_figures16c(fig, ax):
    SSMI_SOC_SSP370_SEN = xr.open_dataset("/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/SPEI/NORMALIZE_ssp245_Max_sensitivity_soc&SPEI120.nc")['max_correlation']
    SSMI_SOC_HISTORICAL_SEN = xr.open_dataset("/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/SPEI/NORMALIZE_historical_Max_sensitivity_soc&SPEI120.nc")['max_correlation']

    SSMI_SOC_SSP370_SEN = SSMI_SOC_SSP370_SEN.where(landmask == 1) - SSMI_SOC_HISTORICAL_SEN.where(landmask == 1)

    ax.set_extent([-170, 180, -60, 90], crs=ccrs.PlateCarree())

    lons = SSMI_SOC_SSP370_SEN.lon.values
    lats = SSMI_SOC_SSP370_SEN.lat.values

    lon_min, lon_max = SSMI_SOC_SSP370_SEN.lon.min().values, SSMI_SOC_SSP370_SEN.lon.max().values
    lat_min, lat_max = SSMI_SOC_SSP370_SEN.lat.min().values, SSMI_SOC_SSP370_SEN.lat.max().values

    cmap_change = mpl.colors.ListedColormap(['#70D3C2', '#92D9C0', '#A8CEB4', '#BEC3A8', '#CCB69C', '#D6A792', '#E09888', '#EB897F', '#F57A76'])
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
                    (lons[j] - d_lon/2, lats[i] - d_lat/2),
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
                (lons[j] - d_lon/2, lats[i] - d_lat/2),
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
        wedgeprops={'edgecolor': 'w', 'alpha':0.8, 'linewidth': 0.5, 'width':0.6},
        textprops={'fontsize': 11}
    )

    ax.add_feature(cfeature.LAND, facecolor='white', edgecolor='black', linewidth=0.5)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)
    ax.set_title("Changes in the selected assiciation magnitude of $SOC$ with SPEI", fontsize=14, pad=15)

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
    gl.xlabel_style = {'size': 16, 'color': 'black'}
    gl.ylabel_style = {'size': 16, 'color': 'black'}

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array(np.array([]))
    cbar = add_unified_colorbar(fig, ax, sm, "", y_offset=0.07)

    ax.text(-0.05, 1.05, '(c)',
            fontweight='bold',
            transform=ax.transAxes,
            fontsize=18,
            va='top', ha='left',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    return sm

def plot_figures16d(fig, ax):
    SSMI_SOC_SSP370_SEN = xr.open_dataset("/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/STI/NORMALIZE_ssp245_Max_sensitivity_soc&STI120.nc")['max_correlation']
    SSMI_SOC_HISTORICAL_SEN = xr.open_dataset("/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/soc/STI/NORMALIZE_historical_Max_sensitivity_soc&STI120.nc")['max_correlation']

    SSMI_SOC_SSP370_SEN = SSMI_SOC_SSP370_SEN.where(landmask == 1) - SSMI_SOC_HISTORICAL_SEN.where(landmask == 1)

    ax.set_extent([-170, 180, -60, 90], crs=ccrs.PlateCarree())

    lons = SSMI_SOC_SSP370_SEN.lon.values
    lats = SSMI_SOC_SSP370_SEN.lat.values

    lon_min, lon_max = SSMI_SOC_SSP370_SEN.lon.min().values, SSMI_SOC_SSP370_SEN.lon.max().values
    lat_min, lat_max = SSMI_SOC_SSP370_SEN.lat.min().values, SSMI_SOC_SSP370_SEN.lat.max().values

    cmap_change = mpl.colors.ListedColormap(['#70D3C2', '#92D9C0', '#A8CEB4', '#BEC3A8', '#CCB69C', '#D6A792', '#E09888', '#EB897F', '#F57A76'])
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
                    (lons[j] - d_lon/2, lats[i] - d_lat/2),
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
                (lons[j] - d_lon/2, lats[i] - d_lat/2),
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
        wedgeprops={'edgecolor': 'w', 'alpha':0.8, 'linewidth': 0.5, 'width':0.6},
        textprops={'fontsize': 11}
    )

    ax.add_feature(cfeature.LAND, facecolor='white', edgecolor='black', linewidth=0.5)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)
    ax.set_title("Changes in the selected assiciation magnitude of $SOC$ with STI", fontsize=14, pad=15)

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
    gl.xlabel_style = {'size': 16, 'color': 'black'}
    gl.ylabel_style = {'size': 16, 'color': 'black'}

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array(np.array([]))
    cbar = add_unified_colorbar(fig, ax, sm, "", y_offset=0.07)

    ax.text(-0.05, 1.05, '(d)',
            fontweight='bold',
            transform=ax.transAxes,
            fontsize=18,
            va='top', ha='left',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    return sm

def create_figures16():
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams['axes.edgecolor'] = 'black'
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Arial'],
        'font.sans-serif': ['Times New Roman'],
    })

    fig = plt.figure(figsize=(16, 9))
    gs = gridspec.GridSpec(2, 2, figure=fig, wspace=0.15, hspace=0.15, top=0.95, bottom=0.07, left=0.1, right=0.99)

    ax0 = fig.add_subplot(gs[0], projection=ccrs.Robinson(central_longitude=10))
    mesh0 = plot_figures16a(fig, ax0)

    ax1 = fig.add_subplot(gs[1], projection=ccrs.Robinson(central_longitude=10))
    mesh1 = plot_figures16b(fig, ax1)

    ax2 = fig.add_subplot(gs[2], projection=ccrs.Robinson(central_longitude=10))
    mesh2 = plot_figures16c(fig, ax2)

    ax3 = fig.add_subplot(gs[3], projection=ccrs.Robinson(central_longitude=10))
    mesh3 = plot_figures16d(fig, ax3)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    pdf_path = os.path.join(OUTPUT_DIR, "FigureS16.pdf")
    plt.savefig(pdf_path, dpi=600, bbox_inches='tight')
    png_path = os.path.join(OUTPUT_DIR, "FigureS16.png")
    plt.savefig(png_path, dpi=600, bbox_inches='tight')

    print(f"Figure saved to: {png_path}")
    plt.close()

if __name__ == '__main__':
    create_figures16()
