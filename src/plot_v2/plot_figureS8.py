"""Create manuscript Supplementary Figure S8.

Converted from PlotExtendedFig2.ipynb. Only complete figures are saved
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
cmap_change = mpl.colors.ListedColormap(['#1E5A96', '#508CC8', '#96BEE6', '#D2E6FA', '#FFFFFF', '#FFE6C8', '#FFBE82', '#FF9646', '#E6641E'])
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

    ax.plot([hotpoint[dd][2], hotpoint[dd][3]], [hotpoint[dd][1], hotpoint[dd][1]], transform=ccrs.PlateCarree(), linewidth=linewi,
            color='k', ls=lines)
    ax.plot([hotpoint[dd][2], hotpoint[dd][3]], [hotpoint[dd][0], hotpoint[dd][0]], transform=ccrs.PlateCarree(), linewidth=linewi,
            color='k', ls=lines)
    ax.plot([hotpoint[dd][2], hotpoint[dd][2]], [hotpoint[dd][0], hotpoint[dd][1]], transform=ccrs.PlateCarree(), linewidth=linewi,
            color='k', ls=lines)
    ax.plot([hotpoint[dd][3], hotpoint[dd][3]], [hotpoint[dd][0], hotpoint[dd][1]], transform=ccrs.PlateCarree(), linewidth=linewi,
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

def plot_figures8a(fig, ax):
    SPEI_HISTORICAL = xr.open_dataset("/run/media/yue/Elements SE/008_Screening_data_CMIP6/Masks/MaxDryingDuration_SSMI_historical.nc")['historical_SSMI12']
    SPEI_HISTORICAL = SPEI_HISTORICAL.where(landmask == 1)

    ax.set_extent([-170, 180, -60, 90], crs=ccrs.PlateCarree())

    lons = SPEI_HISTORICAL.lon.values
    lats = SPEI_HISTORICAL.lat.values

    lon_min, lon_max = SPEI_HISTORICAL.lon.min().values, SPEI_HISTORICAL.lon.max().values
    lat_min, lat_max = SPEI_HISTORICAL.lat.min().values, SPEI_HISTORICAL.lat.max().values

    d_lon = (lon_max - lon_min) / len(SPEI_HISTORICAL.lon)
    d_lat = (lat_max - lat_min) / len(SPEI_HISTORICAL.lat)

    cmap = plt.get_cmap("GnBu")
    vmin = SPEI_HISTORICAL.min().item()
    vmax = SPEI_HISTORICAL.max().item()
    norm = plt.Normalize(0, 24)

    for i in range(len(lats)):
        for j in range(len(lons)):
            if np.isnan(SPEI_HISTORICAL[i, j].item()):
                continue

            value = SPEI_HISTORICAL[i, j].item()

            patch = patches.FancyBboxPatch(
                    (lons[j] - d_lon/2, lats[i] - d_lat/2),
                    d_lon, d_lat,
                    edgecolor='none',
                    facecolor=cmap(norm(value)),
                    alpha=1,
                    boxstyle="round,pad=0.05,rounding_size=0.3",
                    transform=ccrs.PlateCarree(),
                    zorder = 1
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

    draw_hotpoint_labels(hotpoint_label, fig=fig, ax=ax, fontsize=10)

    ax.add_feature(cfeature.LAND, facecolor='white', edgecolor='black', linewidth=0.5)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)
    ax.set_title("The maximum Duration of SSMI", fontsize=16, pad=15)

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
    cbar = add_unified_colorbar(fig, ax, sm, "Historical Maximum Duration of SSMI (months)", extend='neither', show_texts=False)
    cbar.set_ticks(np.arange(0, 25, 4))

    ax.text(-0.1, 1.1, '(a)',
            fontweight='bold',
            transform=ax.transAxes,
            fontsize=22,
            va='top', ha='left',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    return sm

def plot_figures8b(fig, ax):
    SPEI_HISTORICAL = xr.open_dataset("/run/media/yue/Elements SE/008_Screening_data_CMIP6/Masks/MaxDryingDuration_STI_historical.nc")['historical_STI12']
    SPEI_HISTORICAL = SPEI_HISTORICAL.where(landmask == 1)

    ax.set_extent([-170, 180, -60, 90], crs=ccrs.PlateCarree())

    lons = SPEI_HISTORICAL.lon.values
    lats = SPEI_HISTORICAL.lat.values

    lon_min, lon_max = SPEI_HISTORICAL.lon.min().values, SPEI_HISTORICAL.lon.max().values
    lat_min, lat_max = SPEI_HISTORICAL.lat.min().values, SPEI_HISTORICAL.lat.max().values

    d_lon = (lon_max - lon_min) / len(SPEI_HISTORICAL.lon)
    d_lat = (lat_max - lat_min) / len(SPEI_HISTORICAL.lat)

    cmap = plt.get_cmap("GnBu")
    vmin = SPEI_HISTORICAL.min().item()
    vmax = SPEI_HISTORICAL.max().item()
    norm = plt.Normalize(0, 24)

    for i in range(len(lats)):
        for j in range(len(lons)):
            if np.isnan(SPEI_HISTORICAL[i, j].item()):
                continue

            value = SPEI_HISTORICAL[i, j].item()

            patch = patches.FancyBboxPatch(
                    (lons[j] - d_lon/2, lats[i] - d_lat/2),
                    d_lon, d_lat,
                    edgecolor='none',
                    facecolor=cmap(norm(value)),
                    alpha=1,
                    boxstyle="round,pad=0.05,rounding_size=0.3",
                    transform=ccrs.PlateCarree(),
                    zorder = 1
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

    draw_hotpoint_labels(hotpoint_label, fig=fig, ax=ax, fontsize=10)

    ax.add_feature(cfeature.LAND, facecolor='white', edgecolor='black', linewidth=0.5)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)
    ax.set_title("The maximum Duration of STI", fontsize=16, pad=15)

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
    cbar = add_unified_colorbar(fig, ax, sm, "Historical Maximum Duration of STI (months)", extend='neither', show_texts=False)
    cbar.set_ticks(np.arange(0, 25, 4))

    ax.text(-0.1, 1.1, '(b)',
            fontweight='bold',
            transform=ax.transAxes,
            fontsize=22,
            va='top', ha='left',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    return sm

def plot_figures8c(fig, ax):
    SPEI_SSP585 = xr.open_dataset("/run/media/yue/Elements SE/008_Screening_data_CMIP6/Masks/MaxDryingDuration_STI_ssp585.nc")['ssp585_STI12']
    SPEI_HISTORICAL = xr.open_dataset("/run/media/yue/Elements SE/008_Screening_data_CMIP6/Masks/MaxDryingDuration_STI_historical.nc")['historical_STI12']

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
                    (lons[j] - d_lon/2, lats[i] - d_lat/2),
                    d_lon, d_lat,
                    edgecolor='none',
                    facecolor=cmap(norm(value)),
                    alpha=1,
                    boxstyle="round,pad=0.05,rounding_size=0.3",
                    transform=ccrs.PlateCarree(),
                    zorder = 1
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
    total_count = positive_count + negative_count

    pie_ax = ax.inset_axes([-0.05, 0.05, 0.4, 0.4])

    colors = ['#ff7f0e', '#1f77b4']
    pie_ax.pie(
        [positive_count, negative_count],
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops={'edgecolor': 'w', 'alpha':0.8, 'linewidth': 0.5, 'width': 0.65},
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

    pos3 = ax.get_position()
    ax.set_position([pos3.x0, pos3.y0+0.15, pos3.width, pos3.height])

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

def plot_figures8d(fig, ax):
    SPEI_SSP585 = xr.open_dataset("/run/media/yue/Elements SE/008_Screening_data_CMIP6/Masks/MaxDryingDuration_STI_ssp585.nc")['ssp585_STI12']
    SPEI_SSP126 = xr.open_dataset("/run/media/yue/Elements SE/008_Screening_data_CMIP6/Masks/MaxDryingDuration_STI_ssp126.nc")['ssp126_STI12']
    SPEI_HISTORICAL = xr.open_dataset("/run/media/yue/Elements SE/008_Screening_data_CMIP6/Masks/MaxDryingDuration_STI_historical.nc")['historical_STI12']

    SPEI_SSP585 = SPEI_SSP585.where(landmask == 1)
    SPEI_SSP126 = SPEI_SSP126.where(landmask == 1)
    SPEI_HISTORICAL = SPEI_HISTORICAL.where(landmask == 1)

    data_hist = SPEI_HISTORICAL.values.flatten()
    data_hist = data_hist[~np.isnan(data_hist)]

    data_ssp126 = SPEI_SSP126.values.flatten()
    data_ssp126 = data_ssp126[~np.isnan(data_ssp126)]

    data_ssp585 = SPEI_SSP585.values.flatten()
    data_ssp585 = data_ssp585[~np.isnan(data_ssp585)]

    data = [data_hist, data_ssp126, data_ssp585]
    labels = ['Historical', 'SSP1-2.6', 'SSP5-8.5']
    colors = ['#808080', '#1f77b4', '#d62728']

    parts = ax.violinplot(
        data,
        showmeans=True,
        showmedians=True,
        showextrema=False
    )

    for pc, color in zip(parts['bodies'], colors):
        pc.set_facecolor(color)
        pc.set_alpha(0.8)

    parts['cmeans'].set_edgecolor('green')
    parts['cmeans'].set_linewidth(2)

    parts['cmedians'].set_edgecolor('black')
    parts['cmedians'].set_linewidth(1.5)

    quartiles = [np.percentile(d, [25, 50, 75]) for d in data]
    whiskers = [np.array([
        np.percentile(d, 0),
        np.percentile(d, 100)
    ]) for d in data]

    for i, q in enumerate(quartiles):
        ax.vlines(i+1, q[0], q[2], color='k', linestyle='-', lw=5)
        ax.vlines(i+1, q[1], q[1], color='k', linestyle='-', lw=3)
        ax.hlines(q[0], i+0.9, i+1.1, color='k', linestyle='-', lw=1)
        ax.hlines(q[2], i+0.9, i+1.1, color='k', linestyle='-', lw=1)

    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(labels, fontsize=14)
    ax.set_ylabel('Maximum Drying Duration (months)', fontsize=14)

    ax.grid(True, linestyle='--', alpha=0.7, axis='y')

    ax.text(0, 1, '(d)',
            fontweight='bold',
            transform=ax.transAxes,
            fontsize=22,
            va='top', ha='left',)

    ax.set_title('Distribution of Maximum \nDrying Duration of STI', fontsize=16, pad=15)


def create_figures8():
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams['axes.edgecolor'] = 'black'
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Arial'],
        'font.sans-serif': ['Times New Roman'],
    })

    fig = plt.figure(figsize=(16, 20))

    gs = gridspec.GridSpec(2, 4, figure=fig, wspace=0.3, hspace=0.1, top=0.95, bottom=0.07, left=0.1, right=0.99)

    ax1 = fig.add_subplot(gs[0, :2], projection=ccrs.Robinson(central_longitude=10))
    mesh1 = plot_figures8a(fig, ax1)

    ax2 = fig.add_subplot(gs[0, 2:], projection=ccrs.Robinson(central_longitude=10))
    mesh2 = plot_figures8b(fig, ax2)

    ax3 = fig.add_subplot(gs[1, :-1], projection=ccrs.Robinson(central_longitude=10))
    mesh3 = plot_figures8c(fig, ax3)

    ax4 = fig.add_subplot(gs[1, -1])
    mesh4 = plot_figures8d(fig, ax4)

    pos4 = ax4.get_position()
    ax4.set_position([pos4.x0, pos4.y0+0.18, pos4.width, pos4.height * 0.7])

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    pdf_path = os.path.join(OUTPUT_DIR, "FigureS8.pdf")
    plt.savefig(pdf_path, dpi=600, bbox_inches='tight')
    png_path = os.path.join(OUTPUT_DIR, "FigureS8.png")
    plt.savefig(png_path, dpi=600, bbox_inches='tight')

    print(f"Figure saved to: {png_path}")
    plt.close()

if __name__ == '__main__':
    create_figures8()
