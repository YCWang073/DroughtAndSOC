"""Create manuscript Supplementary Figure S6.

Converted from PlotExtendedFig1.ipynb. Only complete figures are saved
to res/eiar_figs.
"""

import os

import matplotlib.patches as patches
import xarray as xr
import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import numpy as np
from matplotlib import gridspec

OUTPUT_DIR = "res/eiar_figs"

COMMON_MODELS = ['CMCC-ESM2', 'CESM2-WACCM','NorESM2-MM', 'TaiESM1', 'EC-Earth3-Veg','CMCC-CM2-SR5', 'BCC-CSM2-MR']

def add_unified_colorbar(fig, ax, mesh, label):
    pos = ax.get_position()

    cax_height = 0.01
    cax_width = pos.width * 0.7
    cax_y = pos.y0 - cax_height - 0.035
    cax_x = pos.x0 + pos.width * 0.15

    cax = fig.add_axes([cax_x, cax_y, cax_width, cax_height])

    cbar = fig.colorbar(mesh, cax=cax, orientation='horizontal', extend='both')
    if 'SSP' in label:
        cbar.ax.text(0, 1.2, "Decrease", ha='left', va='bottom', fontsize=16, transform=cbar.ax.transAxes)
        cbar.ax.text(1, 1.2, "Increase", ha='right', va='bottom', fontsize=16, transform=cbar.ax.transAxes)
    cbar.ax.tick_params(labelsize=18)
    cbar.set_label(label, fontsize=18)

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

def plot_figures6a(fig, ax):
    Rh_data = xr.open_dataset("/mnt/softwares/Drought_And_SOC/000_observasion_data_ERA5/01_preprocessed_data/merged_rh_data.nc")['Rh']
    Uncertainty_landMask = xr.open_dataset("/mnt/softwares/Drought_And_SOC/000_observasion_data_ERA5/01_preprocessed_data/merged_rh_data.nc")['Uncertainty']

    ax.set_extent([-170, 180, -60, 90], crs=ccrs.PlateCarree())

    lons = Rh_data.lon.values
    lats = Rh_data.lat.values

    lon_min, lon_max = Rh_data.lon.min().values, Rh_data.lon.max().values
    lat_min, lat_max = Rh_data.lat.min().values, Rh_data.lat.max().values

    d_lon = (lon_max - lon_min) / len(Rh_data.lon)
    d_lat = (lat_max - lat_min) / len(Rh_data.lat)

    cmap = plt.get_cmap("YlGn")
    vmin = Rh_data.min().item()
    vmax = Rh_data.max().item()
    norm = plt.Normalize(vmin, vmax)

    for i in range(len(lats)):
        for j in range(len(lons)):
            if np.isnan(Rh_data[i, j].item()):
                continue

            value = Rh_data[i, j].item()

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

    mask_lons, mask_lats = np.meshgrid(Uncertainty_landMask.lon, Uncertainty_landMask.lat)
    ax.contourf(
        mask_lons, mask_lats, Uncertainty_landMask,
        levels=[0.5, 1],
        colors='none',
        hatches=['\\\\\\\\\\\\'],
        alpha=0.1,
        transform=ccrs.PlateCarree(),
        zorder=3
    )

    ax.contour(
        mask_lons, mask_lats, Uncertainty_landMask,
        levels=[0.5],
        colors='black',
        linewidths=0.8,
        linestyles='-',
        zorder=3,
        transform=ccrs.PlateCarree()
    )

    ax.add_feature(cfeature.LAND, facecolor='white', edgecolor='black', linewidth=0.5)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)

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
    cbar = add_unified_colorbar(fig, ax, sm, "Benchmark $R_h$ (kgC $m^{-2}$ $yr^{-1}$)")
    cbar.set_ticks(np.arange(0.1, 1.1, 0.1))

    ax.text(-0.05, 1.05, '(a)',
            fontweight='bold',
            transform=ax.transAxes,
            fontsize=22,
            va='top', ha='left',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    return sm

def plot_figures6b(fig, ax):
    Rh_hist = xr.open_dataset("/run/media/yue/Elements SE/008_Screening_data_CMIP6/rh/rh_historical_1985-2014.nc")['rh'].sel(time=slice('1985-01-01', '2014-12-31')).mean(dim='time')
    Rh_ssp126_future = xr.open_dataset("/run/media/yue/Elements SE/008_Screening_data_CMIP6/rh/rh_ssp126_2070-2099.nc")['rh'].sel(time=slice('2070-01-01', '2099-12-31')).mean(dim='time')
    Rh_data = (Rh_ssp126_future - Rh_hist) / Rh_hist * 100
    Rh_data = xr.where(Rh_data > 100, 100, Rh_data)
    Rh_data_change = Rh_ssp126_future - Rh_hist
    Rh_data_change = xr.where(Rh_data_change > 0, 1, xr.where(Rh_data_change < 0, -1, 0))
    model_change = {}
    model_change['MMWM'] = Rh_data_change
    for model in COMMON_MODELS:
        model_hist = xr.open_dataset(f"/run/media/yue/Elements SE/007_CorrectAndRepair_data_CMIP6/{model}/{model}_SeasonAndLand_corrected_rh.nc")['ssp126_rh'].sel(time=slice('1985-01-01', '2014-12-31')).mean(dim='time')
        model_future = xr.open_dataset(f"/run/media/yue/Elements SE/007_CorrectAndRepair_data_CMIP6/{model}/{model}_SeasonAndLand_corrected_rh.nc")['ssp126_rh'].sel(time=slice('2070-01-01', '2099-12-31')).mean(dim='time')
        model_change_data = model_future - model_hist
        model_change_data = xr.where(model_change_data > 0, 1, xr.where(model_change_data < 0, -1, 0))
        model_change[model] = model_change_data

    agreement_increase = xr.zeros_like(model_change['MMWM'])
    agreement_decrease = xr.zeros_like(model_change['MMWM'])

    for model in COMMON_MODELS:
        if model != 'MMWM':
            agreement_increase += (model_change['MMWM'] == 1) & (model_change[model] == 1)
            agreement_decrease += (model_change['MMWM'] == -1) & (model_change[model] == -1)

    total_others = len(COMMON_MODELS)
    agreement_mask_increase = (agreement_increase / total_others) >= 5/7
    agreement_mask_decrease = (agreement_decrease / total_others) >= 5/7

    mask_increase = xr.where(agreement_mask_increase & (model_change['MMWM'] == 1), 1, np.nan)
    mask_decrease = xr.where(agreement_mask_decrease & (model_change['MMWM'] == -1), -1, np.nan)

    final_mask = mask_increase.fillna(0) + mask_decrease.fillna(0)
    final_mask = final_mask.where(final_mask != 0)

    ax.set_extent([-170, 180, -60, 90], crs=ccrs.PlateCarree())

    lons = Rh_data.lon.values
    lats = Rh_data.lat.values

    lon_min, lon_max = Rh_data.lon.min().values, Rh_data.lon.max().values
    lat_min, lat_max = Rh_data.lat.min().values, Rh_data.lat.max().values

    d_lon = (lon_max - lon_min) / len(Rh_data.lon)
    d_lat = (lat_max - lat_min) / len(Rh_data.lat)

    cmap = plt.get_cmap("seismic")
    vmin = Rh_data.min().item()
    vmax = Rh_data.max().item()
    norm = plt.Normalize(-100, 100)

    for i in range(len(lats)):
        for j in range(len(lons)):
            if np.isnan(Rh_data[i, j].item()):
                continue

            value = Rh_data[i, j].item()

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

    mask_points = np.where(np.isfinite(final_mask.values))
    final_mask_lons = final_mask.lon.values[mask_points[1]]
    final_mask_lats = final_mask.lat.values[mask_points[0]]
    ax.scatter(final_mask_lons, final_mask_lats, color='black', s=0.3, alpha=0.7, transform=ccrs.PlateCarree(), zorder=3)

    ax.add_feature(cfeature.LAND, facecolor='white', edgecolor='black', linewidth=0.5)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)

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
    cbar = add_unified_colorbar(fig, ax, sm, "Future $R_h$ Change SSP1-2.6 (%)")
    cbar.set_ticks(np.arange(-100, 100, 20))

    ax.text(-0.05, 1.05, '(b)',
            fontweight='bold',
            transform=ax.transAxes,
            fontsize=22,
            va='top', ha='left',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    return sm

def plot_figures6c(fig, ax):
    Rh_hist = xr.open_dataset("/run/media/yue/Elements SE/008_Screening_data_CMIP6/rh/rh_historical_1985-2014.nc")['rh'].sel(time=slice('1985-01-01', '2014-12-31')).mean(dim='time')
    Rh_ssp126_future = xr.open_dataset("/run/media/yue/Elements SE/008_Screening_data_CMIP6/rh/rh_ssp585_2070-2099.nc")['rh'].sel(time=slice('2070-01-01', '2099-12-31')).mean(dim='time')
    Rh_data = (Rh_ssp126_future - Rh_hist) / Rh_hist * 100
    Rh_data = xr.where(Rh_data > 100, 100, Rh_data)
    Rh_data_change = Rh_ssp126_future - Rh_hist
    Rh_data_change = xr.where(Rh_data_change > 0, 1, xr.where(Rh_data_change < 0, -1, 0))
    model_change = {}
    model_change['MMWM'] = Rh_data_change
    for model in COMMON_MODELS:
        model_hist = xr.open_dataset(f"/run/media/yue/Elements SE/007_CorrectAndRepair_data_CMIP6/{model}/{model}_SeasonAndLand_corrected_rh.nc")['ssp585_rh'].sel(time=slice('1985-01-01', '2014-12-31')).mean(dim='time')
        model_future = xr.open_dataset(f"/run/media/yue/Elements SE/007_CorrectAndRepair_data_CMIP6/{model}/{model}_SeasonAndLand_corrected_rh.nc")['ssp585_rh'].sel(time=slice('2070-01-01', '2099-12-31')).mean(dim='time')
        model_change_data = model_future - model_hist
        model_change_data = xr.where(model_change_data > 0, 1, xr.where(model_change_data < 0, -1, 0))
        model_change[model] = model_change_data

    agreement_increase = xr.zeros_like(model_change['MMWM'])
    agreement_decrease = xr.zeros_like(model_change['MMWM'])

    for model in COMMON_MODELS:
        if model != 'MMWM':
            agreement_increase += (model_change['MMWM'] == 1) & (model_change[model] == 1)
            agreement_decrease += (model_change['MMWM'] == -1) & (model_change[model] == -1)

    total_others = len(COMMON_MODELS)
    agreement_mask_increase = (agreement_increase / total_others) >= 5/7
    agreement_mask_decrease = (agreement_decrease / total_others) >= 5/7

    mask_increase = xr.where(agreement_mask_increase & (model_change['MMWM'] == 1), 1, np.nan)
    mask_decrease = xr.where(agreement_mask_decrease & (model_change['MMWM'] == -1), -1, np.nan)

    final_mask = mask_increase.fillna(0) + mask_decrease.fillna(0)
    final_mask = final_mask.where(final_mask != 0)

    ax.set_extent([-170, 180, -60, 90], crs=ccrs.PlateCarree())

    lons = Rh_data.lon.values
    lats = Rh_data.lat.values

    lon_min, lon_max = Rh_data.lon.min().values, Rh_data.lon.max().values
    lat_min, lat_max = Rh_data.lat.min().values, Rh_data.lat.max().values

    d_lon = (lon_max - lon_min) / len(Rh_data.lon)
    d_lat = (lat_max - lat_min) / len(Rh_data.lat)

    cmap = plt.get_cmap("seismic")
    vmin = Rh_data.min().item()
    vmax = Rh_data.max().item()
    norm = plt.Normalize(-100, 100)

    for i in range(len(lats)):
        for j in range(len(lons)):
            if np.isnan(Rh_data[i, j].item()):
                continue

            value = Rh_data[i, j].item()

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

    mask_points = np.where(np.isfinite(final_mask.values))
    final_mask_lons = final_mask.lon.values[mask_points[1]]
    final_mask_lats = final_mask.lat.values[mask_points[0]]
    ax.scatter(final_mask_lons, final_mask_lats, color='black', s=0.3, alpha=0.7, transform=ccrs.PlateCarree(), zorder=3)

    ax.add_feature(cfeature.LAND, facecolor='white', edgecolor='black', linewidth=0.5)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)

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
    cbar = add_unified_colorbar(fig, ax, sm, "Future $R_h$ Change SSP5-8.5 (%)")
    cbar.set_ticks(np.arange(-100, 100, 20))

    ax.text(-0.05, 1.05, '(c)',
            fontweight='bold',
            transform=ax.transAxes,
            fontsize=22,
            va='top', ha='left',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    return sm

def plot_figures6d(fig, ax):
    Rh_data = xr.open_dataset("/mnt/softwares/Drought_And_SOC/000_observasion_data_ERA5/01_preprocessed_data/merged_rh_data.nc")

    latitudes = Rh_data.lat.values

    Obs_median_mean = Rh_data['Medium'].mean(dim='lon')
    Obs_median_std = Rh_data['Medium'].std(dim='lon')

    median_line, = ax.plot(Obs_median_mean, latitudes,
                        color='black',
                        linewidth=2,
                        label='Benchmark')

    ax.fill_betweenx(latitudes,
                    Obs_median_mean - Obs_median_std,
                    Obs_median_mean + Obs_median_std,
                    facecolor='none',
                    edgecolor='black',
                    hatch='.',
                    alpha=0.7,
                    linewidth=1,
                    zorder=2
                    )

    MMEMean_historical = xr.open_dataset("/run/media/yue/Elements SE/007-1_MEM_data_CMIP6/raw/rh_MMEM.nc")['ssp126_rh'].sel(time=slice('1985-01-01', '2014-12-31')).mean(dim='time')
    MMEMean_data = MMEMean_historical
    MMEMean_relative_mean = MMEMean_data.mean(dim='lon')
    MMEMean_relative_std = MMEMean_data.std(dim='lon')

    MMWMean_historical = xr.open_dataset("/run/media/yue/Elements SE/007-2_MMWM_data_CMIP6/raw/rh_MMWM.nc")['ssp126_rh'].sel(time=slice('1985-01-01', '2014-12-31')).mean(dim='time')
    MMWMean_data = MMWMean_historical
    MMWMean_relative_mean = MMWMean_data.mean(dim='lon')
    MMWMean_relative_std = MMWMean_data.std(dim='lon')

    ax.plot(MMEMean_relative_mean, latitudes, color='darkred', linewidth=2, linestyle='-', label='MMEM Mean')
    ax.fill_betweenx(latitudes, MMEMean_relative_mean - MMEMean_relative_std, MMEMean_relative_mean + MMEMean_relative_std, color='lightcoral', alpha=0.5)

    ax.plot(MMWMean_relative_mean, latitudes, color='darkblue', linewidth=2, linestyle='--', label='MMWM Mean')
    ax.fill_betweenx(latitudes, MMWMean_relative_mean - MMWMean_relative_std, MMWMean_relative_mean + MMWMean_relative_std, color='skyblue', alpha=0.5)

    ax.set_xlabel("$R_h$ (kgC $m^{-2}$ $yr^{-1}$)", fontsize=20)
    ax.set_ylabel("Latitude(°N)", fontsize=20)

    ax.grid(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)

    ax.legend(fontsize=15, loc='lower center',bbox_to_anchor=(0.5, -0.42),)

    ax.set_yticks(np.arange(-60, 91, 30))
    ax.set_xlim(auto=True)

    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.tick_params(axis='both', which='minor', labelsize=12)

    ax.axvline(x=0, color='gray', linestyle='--', alpha=0.7)

    ax.text(-0.4, 1, '(e)',
            fontweight='bold',
            transform=ax.transAxes,
            fontsize=22,
            va='top', ha='left',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

def plot_figures6e(fig, ax):
    Rh_data = xr.open_dataset("/mnt/softwares/Drought_And_SOC/000_observasion_data_ERA5/01_preprocessed_data/merged_rh_data.nc")

    latitudes = Rh_data.lat.values

    MMEMean_historical = xr.open_dataset("/run/media/yue/Elements SE/007-1_MEM_data_CMIP6/raw/rh_MMEM.nc")['ssp126_rh'].sel(time=slice('1985-01-01', '2014-12-31')).mean(dim='time')
    MMEMean_future = xr.open_dataset("/run/media/yue/Elements SE/007-1_MEM_data_CMIP6/raw/rh_MMEM.nc")['ssp126_rh'].sel(time=slice('2070-01-01', '2099-12-31')).mean(dim='time')
    MMEMean_relative = MMEMean_future - MMEMean_historical
    MMEMean_relative_mean = MMEMean_relative.mean(dim='lon')
    MMEMean_relative_std = MMEMean_relative.std(dim='lon')

    MMWMean_historical = xr.open_dataset("/run/media/yue/Elements SE/007-2_MMWM_data_CMIP6/raw/rh_MMWM.nc")['ssp126_rh'].sel(time=slice('1985-01-01', '2014-12-31')).mean(dim='time')
    MMWMean_future = xr.open_dataset("/run/media/yue/Elements SE/007-2_MMWM_data_CMIP6/raw/rh_MMWM.nc")['ssp126_rh'].sel(time=slice('2070-01-01', '2099-12-31')).mean(dim='time')
    MMWMean_relative = MMWMean_future - MMWMean_historical
    MMWMean_relative_mean = MMWMean_relative.mean(dim='lon')
    MMWMean_relative_std = MMWMean_relative.std(dim='lon')

    ax.plot(MMEMean_relative_mean, latitudes, color='darkred', linewidth=2, linestyle='-', label='MMEM Mean')
    ax.fill_betweenx(latitudes, MMEMean_relative_mean - MMEMean_relative_std, MMEMean_relative_mean + MMEMean_relative_std, color='lightcoral', alpha=0.5)

    ax.plot(MMWMean_relative_mean, latitudes, color='darkblue', linewidth=2, linestyle='--', label='MMWM Mean')
    ax.fill_betweenx(latitudes, MMWMean_relative_mean - MMWMean_relative_std, MMWMean_relative_mean + MMWMean_relative_std, color='skyblue', alpha=0.5)

    ax.set_xlabel("$R_h$ change\nSSP1-2.6\n(kgC $m^{-2}$ $yr^{-1}$)", fontsize=20)
    ax.set_ylabel("Latitude(°N)", fontsize=20)

    ax.grid(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)

    ax.set_yticks(np.arange(-60, 91, 30))
    ax.set_xlim(auto=True)

    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.tick_params(axis='both', which='minor', labelsize=12)

    ax.axvline(x=0, color='gray', linestyle='--', alpha=0.7)

    ax.text(-0.4, 1, '(f)',
            fontweight='bold',
            transform=ax.transAxes,
            fontsize=22,
            va='top', ha='left',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

def plot_figures6f(fig, ax):
    Rh_data = xr.open_dataset("/mnt/softwares/Drought_And_SOC/000_observasion_data_ERA5/01_preprocessed_data/merged_rh_data.nc")

    latitudes = Rh_data.lat.values

    MMEMean_historical = xr.open_dataset("/run/media/yue/Elements SE/007-1_MEM_data_CMIP6/raw/rh_MMEM.nc")['ssp585_rh'].sel(time=slice('1985-01-01', '2014-12-31')).mean(dim='time')
    MMEMean_future = xr.open_dataset("/run/media/yue/Elements SE/007-1_MEM_data_CMIP6/raw/rh_MMEM.nc")['ssp585_rh'].sel(time=slice('2070-01-01', '2099-12-31')).mean(dim='time')
    MMEMean_relative = MMEMean_future - MMEMean_historical
    MMEMean_relative_mean = MMEMean_relative.mean(dim='lon')
    MMEMean_relative_std = MMEMean_relative.std(dim='lon')

    MMWMean_historical = xr.open_dataset("/run/media/yue/Elements SE/007-2_MMWM_data_CMIP6/raw/rh_MMWM.nc")['ssp585_rh'].sel(time=slice('1985-01-01', '2014-12-31')).mean(dim='time')
    MMWMean_future = xr.open_dataset("/run/media/yue/Elements SE/007-2_MMWM_data_CMIP6/raw/rh_MMWM.nc")['ssp585_rh'].sel(time=slice('2070-01-01', '2099-12-31')).mean(dim='time')
    MMWMean_relative = MMWMean_future - MMWMean_historical
    MMWMean_relative_mean = MMWMean_relative.mean(dim='lon')
    MMWMean_relative_std = MMWMean_relative.std(dim='lon')

    ax.plot(MMEMean_relative_mean, latitudes, color='darkred', linewidth=2, linestyle='-', label='MMEM Mean')
    ax.fill_betweenx(latitudes, MMEMean_relative_mean - MMEMean_relative_std, MMEMean_relative_mean + MMEMean_relative_std, color='lightcoral', alpha=0.5)

    ax.plot(MMWMean_relative_mean, latitudes, color='darkblue', linewidth=2, linestyle='--', label='MMWM Mean')
    ax.fill_betweenx(latitudes, MMWMean_relative_mean - MMWMean_relative_std, MMWMean_relative_mean + MMWMean_relative_std, color='skyblue', alpha=0.5)

    ax.set_xlabel("$R_h$ change\nSSP5-8.5\n(kgC $m^{-2}$ $yr^{-1}$)", fontsize=20)
    ax.set_ylabel("Latitude(°N)", fontsize=20)

    ax.grid(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)

    ax.set_yticks(np.arange(-60, 91, 30))
    ax.set_xlim(auto=True)

    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.tick_params(axis='both', which='minor', labelsize=12)

    ax.axvline(x=0, color='gray', linestyle='--', alpha=0.7)

    ax.text(-0.4, 1, '(g)',
            fontweight='bold',
            transform=ax.transAxes,
            fontsize=22,
            va='top', ha='left',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

def plot_figures6g(fig, ax):
    Rh_hist = xr.open_dataset("/run/media/yue/Elements SE/008_Screening_data_CMIP6/soc/soc_historical_1985-2014.nc")['soc'].sel(time=slice('1985-01-01', '2014-12-31')).mean(dim='time')
    Rh_ssp126_future = xr.open_dataset("/run/media/yue/Elements SE/008_Screening_data_CMIP6/soc/soc_ssp126_2070-2099.nc")['soc'].sel(time=slice('2070-01-01', '2099-12-31')).mean(dim='time')
    Rh_data = (Rh_ssp126_future - Rh_hist) / Rh_hist * 100
    Rh_data = xr.where(Rh_data > 100, 100, Rh_data)
    Rh_data_change = Rh_ssp126_future - Rh_hist
    Rh_data_change = xr.where(Rh_data_change > 0, 1, xr.where(Rh_data_change < 0, -1, 0))
    model_change = {}
    model_change['MMWM'] = Rh_data_change
    for model in COMMON_MODELS:
        model_hist = xr.open_dataset(f"/run/media/yue/Elements SE/007_CorrectAndRepair_data_CMIP6/{model}/{model}_SeasonAndLand_corrected_soc.nc")['ssp126_soc'].sel(time=slice('1985-01-01', '2014-12-31')).mean(dim='time')
        model_future = xr.open_dataset(f"/run/media/yue/Elements SE/007_CorrectAndRepair_data_CMIP6/{model}/{model}_SeasonAndLand_corrected_soc.nc")['ssp126_soc'].sel(time=slice('2070-01-01', '2099-12-31')).mean(dim='time')
        model_change_data = model_future - model_hist
        model_change_data = xr.where(model_change_data > 0, 1, xr.where(model_change_data < 0, -1, 0))
        model_change[model] = model_change_data

    agreement_increase = xr.zeros_like(model_change['MMWM'])
    agreement_decrease = xr.zeros_like(model_change['MMWM'])

    for model in COMMON_MODELS:
        if model != 'MMWM':
            agreement_increase += (model_change['MMWM'] == 1) & (model_change[model] == 1)
            agreement_decrease += (model_change['MMWM'] == -1) & (model_change[model] == -1)

    total_others = len(COMMON_MODELS)
    agreement_mask_increase = (agreement_increase / total_others) >= 5/7
    agreement_mask_decrease = (agreement_decrease / total_others) >= 5/7

    mask_increase = xr.where(agreement_mask_increase & (model_change['MMWM'] == 1), 1, np.nan)
    mask_decrease = xr.where(agreement_mask_decrease & (model_change['MMWM'] == -1), -1, np.nan)

    final_mask = mask_increase.fillna(0) + mask_decrease.fillna(0)
    final_mask = final_mask.where(final_mask != 0)

    ax.set_extent([-170, 180, -60, 90], crs=ccrs.PlateCarree())

    lons = Rh_data.lon.values
    lats = Rh_data.lat.values

    lon_min, lon_max = Rh_data.lon.min().values, Rh_data.lon.max().values
    lat_min, lat_max = Rh_data.lat.min().values, Rh_data.lat.max().values

    d_lon = (lon_max - lon_min) / len(Rh_data.lon)
    d_lat = (lat_max - lat_min) / len(Rh_data.lat)

    cmap = plt.get_cmap("seismic")
    vmin = Rh_data.min().item()
    vmax = Rh_data.max().item()
    norm = plt.Normalize(-50, 51)

    for i in range(len(lats)):
        for j in range(len(lons)):
            if np.isnan(Rh_data[i, j].item()):
                continue

            value = Rh_data[i, j].item()

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

    mask_points = np.where(np.isfinite(final_mask.values))
    final_mask_lons = final_mask.lon.values[mask_points[1]]
    final_mask_lats = final_mask.lat.values[mask_points[0]]
    ax.scatter(final_mask_lons, final_mask_lats, color='black', s=0.3, alpha=0.7, transform=ccrs.PlateCarree(), zorder=3)

    ax.add_feature(cfeature.LAND, facecolor='white', edgecolor='black', linewidth=0.5)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)

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
    cbar = add_unified_colorbar(fig, ax, sm, "Future $SOC$ Change SSP1-2.6 (%)")
    cbar.set_ticks(np.arange(-50, 51, 20))

    ax.text(-0.05, 1.05, '(d)',
            fontweight='bold',
            transform=ax.transAxes,
            fontsize=22,
            va='top', ha='left',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    return sm

def plot_figures6h(fig, ax):
    Rh_data = xr.open_dataset("/mnt/softwares/Drought_And_SOC/000_observasion_data_ERA5/01_preprocessed_data/merged_csoil_data.nc")

    latitudes = Rh_data.lat.values

    MMEMean_historical = xr.open_dataset("/run/media/yue/Elements SE/007-1_MEM_data_CMIP6/raw/soc_MMEM.nc")['ssp126_soc'].sel(time=slice('1985-01-01', '2014-12-31')).mean(dim='time')
    MMEMean_future = xr.open_dataset("/run/media/yue/Elements SE/007-1_MEM_data_CMIP6/raw/soc_MMEM.nc")['ssp126_soc'].sel(time=slice('2070-01-01', '2099-12-31')).mean(dim='time')
    MMEMean_relative = MMEMean_future - MMEMean_historical
    MMEMean_relative_mean = MMEMean_relative.mean(dim='lon')
    MMEMean_relative_std = MMEMean_relative.std(dim='lon')

    MMWMean_historical = xr.open_dataset("/run/media/yue/Elements SE/007-2_MMWM_data_CMIP6/raw/soc_MMWM.nc")['ssp126_soc'].sel(time=slice('1985-01-01', '2014-12-31')).mean(dim='time')
    MMWMean_future = xr.open_dataset("/run/media/yue/Elements SE/007-2_MMWM_data_CMIP6/raw/soc_MMWM.nc")['ssp126_soc'].sel(time=slice('2070-01-01', '2099-12-31')).mean(dim='time')
    MMWMean_relative = MMWMean_future - MMWMean_historical
    MMWMean_relative_mean = MMWMean_relative.mean(dim='lon')
    MMWMean_relative_std = MMWMean_relative.std(dim='lon')

    ax.plot(MMEMean_relative_mean, latitudes, color='darkred', linewidth=2, linestyle='-', label='MMEM Mean')
    ax.fill_betweenx(latitudes, MMEMean_relative_mean - MMEMean_relative_std, MMEMean_relative_mean + MMEMean_relative_std, color='lightcoral', alpha=0.5)

    ax.plot(MMWMean_relative_mean, latitudes, color='darkblue', linewidth=2, linestyle='--', label='MMWM Mean')
    ax.fill_betweenx(latitudes, MMWMean_relative_mean - MMWMean_relative_std, MMWMean_relative_mean + MMWMean_relative_std, color='skyblue', alpha=0.5)

    ax.set_xlabel("$SOC$ change\nSSP1-2.6\n(kgC $m^{-2}$)", fontsize=20)
    ax.set_ylabel("Latitude(°N)", fontsize=20)

    ax.grid(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)

    ax.set_yticks(np.arange(-60, 91, 30))
    ax.set_xlim(auto=True)

    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.tick_params(axis='both', which='minor', labelsize=12)

    ax.axvline(x=0, color='gray', linestyle='--', alpha=0.7)

    ax.text(-0.4, 1, '(h)',
            fontweight='bold',
            transform=ax.transAxes,
            fontsize=22,
            va='top', ha='left',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))


def create_figures6():
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams['axes.edgecolor'] = 'black'
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Arial'],
        'font.sans-serif': ['Times New Roman'],
    })

    fig = plt.figure(figsize=(16, 30))

    gs = gridspec.GridSpec(4, 2, width_ratios=[6, 1], figure=fig, wspace=0.15, hspace=0.45, top=0.95, bottom=0.07, left=0.1, right=0.99)

    ax1 = fig.add_subplot(gs[0], projection=ccrs.Robinson(central_longitude=10))
    mesh1 = plot_figures6a(fig, ax1)

    ax2 = fig.add_subplot(gs[1])
    mesh2 = plot_figures6d(fig, ax2)

    ax3 = fig.add_subplot(gs[2], projection=ccrs.Robinson(central_longitude=10))
    mesh3 = plot_figures6b(fig, ax3)

    ax4 = fig.add_subplot(gs[3])
    mesh4 = plot_figures6e(fig, ax4)

    ax5 = fig.add_subplot(gs[4], projection=ccrs.Robinson(central_longitude=10))
    mesh5 = plot_figures6c(fig, ax5)

    ax6 = fig.add_subplot(gs[5])
    mesh6 = plot_figures6f(fig, ax6)

    ax7 = fig.add_subplot(gs[6], projection=ccrs.Robinson(central_longitude=10))
    mesh7 = plot_figures6g(fig, ax7)

    ax8 = fig.add_subplot(gs[7])
    mesh8 = plot_figures6h(fig, ax8)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    pdf_path = os.path.join(OUTPUT_DIR, "FigureS6.pdf")
    plt.savefig(pdf_path, dpi=600, bbox_inches='tight')
    png_path = os.path.join(OUTPUT_DIR, "FigureS6.png")
    plt.savefig(png_path, dpi=600, bbox_inches='tight')

    print(f"Figure saved to: {png_path}")
    plt.close()

if __name__ == '__main__':
    create_figures6()
