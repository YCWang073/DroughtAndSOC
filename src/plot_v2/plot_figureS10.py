"""Create manuscript Supplementary Figure S10.

Converted from PlotSupplementaryFig10.ipynb. Only complete figures are saved
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

cmap_continuous = mpl.colors.ListedColormap(['#FFF9C4', '#FFD54F', '#FF8A65', '#D84315', '#4E342E'])
cmap_continuous.set_under('white')
levels_continuous = [1, 2, 3, 4, 5]
cmap_change = mpl.colors.ListedColormap(
    ['#1E5A96', '#508CC8', '#96BEE6', '#D2E6FA', '#FFFFFF', '#FFE6C8', '#FFBE82', '#FF9646', '#E6641E'])
cmap_change.set_over('#B43C00')
cmap_change.set_under('#003264')
levels_change = [-16, -12, -8, -4, -1, 1, 4, 8, 12, 16]


def add_unified_colorbar(fig, ax, mesh, label, extend='both', show_texts=True):
    pos = ax.get_position()

    cax_height = 0.01
    cax_width = pos.width * 0.7
    cax_y = pos.y0 - cax_height - 0.035
    cax_x = pos.x0 + pos.width * 0.15

    cax = fig.add_axes([cax_x, cax_y, cax_width, cax_height])

    cbar = fig.colorbar(mesh, cax=cax, orientation='horizontal', extend=extend)
    if show_texts:
        cbar.ax.text(0, 1.2, "Decrease", ha='left', va='bottom', fontsize=16, transform=cbar.ax.transAxes)
        cbar.ax.text(1, 1.2, "Increase", ha='right', va='bottom', fontsize=16, transform=cbar.ax.transAxes)
    cbar.ax.tick_params(labelsize=18)
    cbar.set_label(label, fontsize=18)

    return cbar


def draw_rectange_map(hotpoint, dd, fig=False, ax=None, extent=[-180, 180, -60, 90], linewi=1, lines='-'):
    if not fig:
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
                transform=ccrs.PlateCarree(), )

def plot_figures10a(fig, ax):
    SSMI_SSP585 = xr.open_dataset("/run/media/yue/Elements SE/008_Screening_data_CMIP6/Masks/MaxDryingDuration_SSMI_ssp245.nc")['ssp245_SSMI12']
    SSMI_HISTORICAL = xr.open_dataset("/run/media/yue/Elements SE/008_Screening_data_CMIP6/Masks/MaxDryingDuration_SSMI_historical.nc")[
        'historical_SSMI12']

    SSMI_MAX_DUR_CHANGE = SSMI_SSP585 - SSMI_HISTORICAL
    SSMI_MAX_DUR_CHANGE = SSMI_MAX_DUR_CHANGE.where(landmask == 1)

    ax.set_extent([-170, 180, -60, 90], crs=ccrs.PlateCarree())

    lons = SSMI_MAX_DUR_CHANGE.lon.values
    lats = SSMI_MAX_DUR_CHANGE.lat.values

    lon_min, lon_max = SSMI_MAX_DUR_CHANGE.lon.min().values, SSMI_MAX_DUR_CHANGE.lon.max().values
    lat_min, lat_max = SSMI_MAX_DUR_CHANGE.lat.min().values, SSMI_MAX_DUR_CHANGE.lat.max().values

    d_lon = (lon_max - lon_min) / len(SSMI_MAX_DUR_CHANGE.lon)
    d_lat = (lat_max - lat_min) / len(SSMI_MAX_DUR_CHANGE.lat)

    vmin = SSMI_MAX_DUR_CHANGE.min().item()
    vmax = SSMI_MAX_DUR_CHANGE.max().item()
    cmap = cmap_change
    norm = mpl.colors.BoundaryNorm(levels_change, cmap.N)

    for i in range(len(lats)):
        for j in range(len(lons)):
            if np.isnan(SSMI_MAX_DUR_CHANGE[i, j].item()):
                continue

            value = SSMI_MAX_DUR_CHANGE[i, j].item()

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

    draw_hotpoint_labels(hotpoint_label, fig=fig, ax=ax)

    positive_count = np.sum(SSMI_MAX_DUR_CHANGE.values > 0)
    negative_count = np.sum(SSMI_MAX_DUR_CHANGE.values < 0)

    pie_ax = ax.inset_axes([-0.05, 0.05, 0.4, 0.4])

    colors = ['#ff7f0e', '#1f77b4']
    pie_ax.pie(
        [positive_count, negative_count],
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops={'edgecolor': 'w', 'alpha': 0.8, 'linewidth': 0.5, 'width': 0.65},
        textprops={'fontsize': 14}
    )

    ax.add_feature(cfeature.LAND, facecolor='white', edgecolor='black', linewidth=0.5)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)
    ax.set_title("Changes in the maximum Duration of SSMI(SSP2-4.5)", fontsize=16, pad=15)

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

    ax.text(-0.05, 1.05, '(a)',
            fontweight='bold',
            transform=ax.transAxes,
            fontsize=22,
            va='top', ha='left',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    return sm

def plot_figures10b(fig, ax):
    SPEI_SSP585 = xr.open_dataset("/run/media/yue/Elements SE/008_Screening_data_CMIP6/Masks/MaxDryingDuration_SPEI_ssp245.nc")['ssp245_SPEI12']
    SPEI_HISTORICAL = xr.open_dataset("/run/media/yue/Elements SE/008_Screening_data_CMIP6/Masks/MaxDryingDuration_SPEI_historical.nc")[
        'historical_SPEI12']

    SPEI_MAX_DUR_CHANGE = SPEI_SSP585 - SPEI_HISTORICAL
    SPEI_MAX_DUR_CHANGE = SPEI_MAX_DUR_CHANGE.where(landmask == 1)

    ax.set_extent([-170, 180, -60, 90], crs=ccrs.PlateCarree())

    lons = SPEI_MAX_DUR_CHANGE.lon.values
    lats = SPEI_MAX_DUR_CHANGE.lat.values

    lon_min, lon_max = SPEI_MAX_DUR_CHANGE.lon.min().values, SPEI_MAX_DUR_CHANGE.lon.max().values
    lat_min, lat_max = SPEI_MAX_DUR_CHANGE.lat.min().values, SPEI_MAX_DUR_CHANGE.lat.max().values

    d_lon = (lon_max - lon_min) / len(SPEI_MAX_DUR_CHANGE.lon)
    d_lat = (lat_max - lat_min) / len(SPEI_MAX_DUR_CHANGE.lat)

    vmin = SPEI_MAX_DUR_CHANGE.min().item()
    vmax = SPEI_MAX_DUR_CHANGE.max().item()
    cmap = cmap_change
    norm = mpl.colors.BoundaryNorm(levels_change, cmap.N)

    for i in range(len(lats)):
        for j in range(len(lons)):
            if np.isnan(SPEI_MAX_DUR_CHANGE[i, j].item()):
                continue

            value = SPEI_MAX_DUR_CHANGE[i, j].item()

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

    draw_hotpoint_labels(hotpoint_label, fig=fig, ax=ax)

    positive_count = np.sum(SPEI_MAX_DUR_CHANGE.values > 0)
    negative_count = np.sum(SPEI_MAX_DUR_CHANGE.values < 0)

    pie_ax = ax.inset_axes([-0.05, 0.05, 0.4, 0.4])

    colors = ['#ff7f0e', '#1f77b4']
    pie_ax.pie(
        [positive_count, negative_count],
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops={'edgecolor': 'w', 'alpha': 0.8, 'linewidth': 0.5, 'width': 0.65},
        textprops={'fontsize': 14}
    )

    ax.add_feature(cfeature.LAND, facecolor='white', edgecolor='black', linewidth=0.5)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)
    ax.set_title("Changes in the maximum Duration of SPEI", fontsize=16, pad=15)

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

    ax.text(-0.05, 1.05, '(b)',
            fontweight='bold',
            transform=ax.transAxes,
            fontsize=22,
            va='top', ha='left',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    return sm

def plot_figures10c(fig, ax):
    STI_SSP585 = xr.open_dataset("/run/media/yue/Elements SE/008_Screening_data_CMIP6/Masks/MaxDryingDuration_STI_ssp245.nc")['ssp245_STI12']
    STI_HISTORICAL = xr.open_dataset("/run/media/yue/Elements SE/008_Screening_data_CMIP6/Masks/MaxDryingDuration_STI_historical.nc")[
        'historical_STI12']

    STI_MAX_DUR_CHANGE = STI_SSP585 - STI_HISTORICAL
    STI_MAX_DUR_CHANGE = STI_MAX_DUR_CHANGE.where(landmask == 1)

    ax.set_extent([-170, 180, -60, 90], crs=ccrs.PlateCarree())

    lons = STI_MAX_DUR_CHANGE.lon.values
    lats = STI_MAX_DUR_CHANGE.lat.values

    lon_min, lon_max = STI_MAX_DUR_CHANGE.lon.min().values, STI_MAX_DUR_CHANGE.lon.max().values
    lat_min, lat_max = STI_MAX_DUR_CHANGE.lat.min().values, STI_MAX_DUR_CHANGE.lat.max().values

    d_lon = (lon_max - lon_min) / len(STI_MAX_DUR_CHANGE.lon)
    d_lat = (lat_max - lat_min) / len(STI_MAX_DUR_CHANGE.lat)

    vmin = STI_MAX_DUR_CHANGE.min().item()
    vmax = STI_MAX_DUR_CHANGE.max().item()
    cmap = cmap_change
    norm = mpl.colors.BoundaryNorm(levels_change, cmap.N)

    for i in range(len(lats)):
        for j in range(len(lons)):
            if np.isnan(STI_MAX_DUR_CHANGE[i, j].item()):
                continue

            value = STI_MAX_DUR_CHANGE[i, j].item()

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

    draw_hotpoint_labels(hotpoint_label, fig=fig, ax=ax)

    positive_count = np.sum(STI_MAX_DUR_CHANGE.values > 0)
    negative_count = np.sum(STI_MAX_DUR_CHANGE.values < 0)

    pie_ax = ax.inset_axes([-0.05, 0.05, 0.4, 0.4])

    colors = ['#ff7f0e', '#1f77b4']
    pie_ax.pie(
        [positive_count, negative_count],
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops={'edgecolor': 'w', 'alpha': 0.8, 'linewidth': 0.5, 'width': 0.65},
        textprops={'fontsize': 14}
    )

    ax.add_feature(cfeature.LAND, facecolor='white', edgecolor='black', linewidth=0.5)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)
    ax.set_title("Changes in the maximum Duration of STI", fontsize=16, pad=15)

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

    ax.text(-0.05, 1.05, '(c)',
            fontweight='bold',
            transform=ax.transAxes,
            fontsize=22,
            va='top', ha='left',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    return sm


def create_figures10():
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams['axes.edgecolor'] = 'black'
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Arial'],
        'font.sans-serif': ['Times New Roman'],
    })

    fig = plt.figure(figsize=(16, 20))

    gs = gridspec.GridSpec(3, 1, figure=fig, wspace=0.15, hspace=0.25, top=0.95, bottom=0.07, left=0.1, right=0.99)

    ax1 = fig.add_subplot(gs[0], projection=ccrs.Robinson(central_longitude=10))
    mesh1 = plot_figures10a(fig, ax1)

    ax2 = fig.add_subplot(gs[1], projection=ccrs.Robinson(central_longitude=10))
    mesh2 = plot_figures10b(fig, ax2)

    ax3 = fig.add_subplot(gs[2], projection=ccrs.Robinson(central_longitude=10))
    mesh3 = plot_figures10c(fig, ax3)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    pdf_path = os.path.join(OUTPUT_DIR, "FigureS10.pdf")
    plt.savefig(pdf_path, dpi=600, bbox_inches='tight')
    png_path = os.path.join(OUTPUT_DIR, "FigureS10.png")
    plt.savefig(png_path, dpi=600, bbox_inches='tight')

    print(f"Figure saved to: {png_path}")
    plt.close()

if __name__ == '__main__':
    create_figures10()
