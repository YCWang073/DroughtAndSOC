import matplotlib.patches as patches
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import numpy as np
from matplotlib import gridspec
import matplotlib as mpl
import os

COMMON_MODELS = ['CMCC-ESM2', 'CESM2-WACCM', 'NorESM2-MM', 'TaiESM1',
                 'EC-Earth3-Veg', 'CMCC-CM2-SR5', 'BCC-CSM2-MR']

OUTPUT_DIR = "res/eiar_figs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def add_unified_colorbar(fig, ax, mesh, label):
    pos = ax.get_position()

    cax_height = 0.01
    cax_width = pos.width * 0.7
    cax_y = pos.y0 - cax_height - 0.035
    cax_x = pos.x0 + pos.width * 0.15

    cax = fig.add_axes([cax_x, cax_y, cax_width, cax_height])

    cbar = fig.colorbar(mesh, cax=cax, orientation='horizontal', extend='both')
    if 'SSP' in label:
        cbar.ax.text(0, 1.2, "Decrease", ha='left', va='bottom', fontsize=16,
                     transform=cbar.ax.transAxes)
        cbar.ax.text(1, 1.2, "Increase", ha='right', va='bottom', fontsize=16,
                     transform=cbar.ax.transAxes)
    cbar.ax.tick_params(labelsize=18)
    cbar.set_label(label, fontsize=18)

    return cbar


cmap_obs = mpl.colors.ListedColormap(['#B8D0C9', '#92B6AA', '#699689',
                                     '#4F7A6F', '#3D6157', '#2F4F4F'])
cmap_obs.set_under('#DAE8E4')
cmap_obs.set_over('#23403A')
levels_obs = [1, 3, 7, 15, 30, 50, 80]


def draw_rectange_map(hotpoint, dd, fig=False, ax=None,
                      extent=[-180, 180, -60, 90], linewi=1, lines='-'):
    if fig is False:
        fig = plt.figure(figsize=(12.27, 6.69), dpi=100, facecolor='white')
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
        ax.set_extent(extent, crs=ccrs.PlateCarree())
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.LAND, facecolor='#FFE9B5')

    ax.plot([hotpoint[dd][2], hotpoint[dd][3]], [hotpoint[dd][1], hotpoint[dd][1]],
            transform=ccrs.PlateCarree(), linewidth=linewi, color='k', ls=lines)
    ax.plot([hotpoint[dd][2], hotpoint[dd][3]], [hotpoint[dd][0], hotpoint[dd][0]],
            transform=ccrs.PlateCarree(), linewidth=linewi, color='k', ls=lines)
    ax.plot([hotpoint[dd][2], hotpoint[dd][2]], [hotpoint[dd][0], hotpoint[dd][1]],
            transform=ccrs.PlateCarree(), linewidth=linewi, color='k', ls=lines)
    ax.plot([hotpoint[dd][3], hotpoint[dd][3]], [hotpoint[dd][0], hotpoint[dd][1]],
            transform=ccrs.PlateCarree(), linewidth=linewi, color='k', ls=lines)


def draw_hotpoint_labels(hotpoint_label, fig=None, ax=None, fontsize=16,
                         fontweight='bold', color='black'):
    for region_name, coords in hotpoint_label.items():
        lat, lon = coords
        ax.text(lon, lat, region_name,
                fontsize=fontsize, fontweight=fontweight, color=color,
                ha='center', va='center', transform=ccrs.PlateCarree())


def plot_fig4a(fig, ax):
    MMWM_SOC = xr.open_dataset(
        "/run/media/yue/Elements SE/007-2_MMWM_data_CMIP6/raw/soc_MMWM.nc")
    MMWM_RH = xr.open_dataset(
        "/run/media/yue/Elements SE/007-2_MMWM_data_CMIP6/raw/rh_MMWM.nc")

    MMWM_SOC_HISTORICAL = MMWM_SOC['ssp126_soc'].sel(
        time=slice('1901-01-01', '2014-12-31')).mean(dim=['lat', 'lon']).groupby(
        'time.year').mean()
    MMWM_SOC_SSP126 = MMWM_SOC['ssp126_soc'].sel(
        time=slice('2014-01-01', '2100-12-31')).mean(dim=['lat', 'lon']).groupby(
        'time.year').mean()
    MMWM_SOC_SSP585 = MMWM_SOC['ssp585_soc'].sel(
        time=slice('2014-01-01', '2100-12-31')).mean(dim=['lat', 'lon']).groupby(
        'time.year').mean()

    MMWM_RH_HISTORICAL = MMWM_RH['ssp126_rh'].sel(
        time=slice('1901-01-01', '2014-12-31')).mean(dim=['lat', 'lon']).groupby(
        'time.year').mean()
    MMWM_RH_SSP126 = MMWM_RH['ssp126_rh'].sel(
        time=slice('2014-01-01', '2100-12-31')).mean(dim=['lat', 'lon']).groupby(
        'time.year').mean()
    MMWM_RH_SSP585 = MMWM_RH['ssp585_rh'].sel(
        time=slice('2014-01-01', '2100-12-31')).mean(dim=['lat', 'lon']).groupby(
        'time.year').mean()

    TIME_RANGE = np.arange(1901, 2100)

    SOC_HISTORICAL = MMWM_SOC_HISTORICAL.values
    SOC_SSP126 = MMWM_SOC_SSP126.values
    SOC_SSP585 = MMWM_SOC_SSP585.values

    RH_HISTORICAL = MMWM_RH_HISTORICAL.values
    RH_SSP126 = MMWM_RH_SSP126.values
    RH_SSP585 = MMWM_RH_SSP585.values

    ax2 = ax.twinx()

    HIST_BG_COLOR = '#e6f5ff'
    FUTURE_BG_COLOR = '#fff9e6'

    SOC_HIST_COLOR = '#2c3e50'
    SOC_SSP126_COLOR = '#3498db'
    SOC_SSP585_COLOR = '#e74c3c'

    RH_HIST_COLOR = '#7f8c8d'
    RH_SSP126_COLOR = '#2980b9'
    RH_SSP585_COLOR = '#c0392b'

    ERROR_ALPHA = 0.2

    ax.axvspan(1900, 2014, facecolor=HIST_BG_COLOR, alpha=0.5, zorder=0)
    ax.axvspan(2014, 2100, facecolor=FUTURE_BG_COLOR, alpha=0.5, zorder=0)

    ax.axvline(x=2014, color='#95a5a6', linestyle='-', linewidth=1.5,
               alpha=0.7, zorder=1)

    ax.text(0.45, 0.95, 'Historical period',
            fontsize=18, color='#0e9fff', ha='center', va='center',
            transform=ax.transAxes, fontweight='bold')
    ax.text(0.69, 0.95, 'Future Scenarios',
            fontsize=18, color='#ffc50e', ha='center', va='center',
            transform=ax.transAxes, fontweight='bold')

    soc_hist_line, = ax.plot(TIME_RANGE[:114], SOC_HISTORICAL,
                             color=SOC_HIST_COLOR, label='Historical $SOC$',
                             linewidth=2.5, zorder=5)
    soc_ssp126_line, = ax.plot(TIME_RANGE[113:], SOC_SSP126,
                               color=SOC_SSP126_COLOR, label='SSP1-2.6 $SOC$',
                               linewidth=2.5, zorder=5)
    soc_ssp585_line, = ax.plot(TIME_RANGE[113:], SOC_SSP585,
                               color=SOC_SSP585_COLOR, label='SSP5-8.5 $SOC$',
                               linewidth=2.5, zorder=5)

    rh_hist_line, = ax2.plot(TIME_RANGE[:114], RH_HISTORICAL,
                             color=RH_HIST_COLOR, linestyle='--',
                             label='Historical $R_h$', linewidth=2.5, zorder=5)
    rh_ssp126_line, = ax2.plot(TIME_RANGE[113:], RH_SSP126,
                               color=RH_SSP126_COLOR, linestyle='--',
                               label='SSP1-2.6 $R_h$', linewidth=2.5, zorder=5)
    rh_ssp585_line, = ax2.plot(TIME_RANGE[113:], RH_SSP585,
                               color=RH_SSP585_COLOR, linestyle='--',
                               label='SSP5-8.5 $R_h$', linewidth=2.5, zorder=5)

    ax.fill_between(TIME_RANGE[:114], SOC_HISTORICAL - SOC_HISTORICAL.std(),
                    SOC_HISTORICAL + SOC_HISTORICAL.std(),
                    color=SOC_HIST_COLOR, alpha=ERROR_ALPHA, zorder=2)
    ax.fill_between(TIME_RANGE[113:], SOC_SSP126 - SOC_SSP126.std(),
                    SOC_SSP126 + SOC_SSP126.std(),
                    color=SOC_SSP126_COLOR, alpha=ERROR_ALPHA, zorder=2)
    ax.fill_between(TIME_RANGE[113:], SOC_SSP585 - SOC_SSP585.std(),
                    SOC_SSP585 + SOC_SSP585.std(),
                    color=SOC_SSP585_COLOR, alpha=ERROR_ALPHA, zorder=2)

    ax2.fill_between(TIME_RANGE[:114], RH_HISTORICAL - RH_HISTORICAL.std(),
                     RH_HISTORICAL + RH_HISTORICAL.std(),
                     color=RH_HIST_COLOR, alpha=ERROR_ALPHA, zorder=2)
    ax2.fill_between(TIME_RANGE[113:], RH_SSP126 - RH_SSP126.std(),
                     RH_SSP126 + RH_SSP126.std(),
                     color=RH_SSP126_COLOR, alpha=ERROR_ALPHA, zorder=2)
    ax2.fill_between(TIME_RANGE[113:], RH_SSP585 - RH_SSP585.std(),
                     RH_SSP585 + RH_SSP585.std(),
                     color=RH_SSP585_COLOR, alpha=ERROR_ALPHA, zorder=2)

    HIST_PERIOD = (1985, 2014)
    FUTURE_PERIOD = (2070, 2099)

    hist_start_idx = np.where(TIME_RANGE == HIST_PERIOD[0])[0][0]
    hist_end_idx = np.where(TIME_RANGE == HIST_PERIOD[1])[0][0]

    future_start_idx = np.where(TIME_RANGE == FUTURE_PERIOD[0])[0][0]
    future_end_idx = np.where(TIME_RANGE == FUTURE_PERIOD[1])[0][0]

    # SOC historical trend
    soc_hist_trend = np.polyfit(
        TIME_RANGE[hist_start_idx:hist_end_idx],
        SOC_HISTORICAL[hist_start_idx:hist_end_idx], 1)
    soc_hist_trend_line = (soc_hist_trend[0] * TIME_RANGE[hist_start_idx:hist_end_idx]
                           + soc_hist_trend[1])
    ax.plot(TIME_RANGE[hist_start_idx:hist_end_idx], soc_hist_trend_line,
            color=SOC_HIST_COLOR, linestyle='-', linewidth=3, alpha=0.9, zorder=7)
    slope_value = soc_hist_trend[0]
    ax.text(TIME_RANGE[hist_end_idx] - 25, soc_hist_trend_line[-1] + 0.01,
            f"SOC slope: {slope_value:.4f}", color=SOC_HIST_COLOR,
            fontsize=14, va='center', zorder=8)

    # SOC SSP126 trend
    soc_ssp126_trend = np.polyfit(
        TIME_RANGE[future_start_idx:future_end_idx],
        SOC_SSP126[future_start_idx - 113:future_end_idx - 113], 1)
    soc_ssp126_trend_line = (soc_ssp126_trend[0] * TIME_RANGE[future_start_idx:future_end_idx]
                             + soc_ssp126_trend[1])
    ax.plot(TIME_RANGE[future_start_idx:future_end_idx], soc_ssp126_trend_line,
            color=SOC_SSP126_COLOR, linestyle='-', linewidth=3, alpha=0.9, zorder=7)

    # SOC SSP585 trend
    soc_ssp585_trend = np.polyfit(
        TIME_RANGE[future_start_idx:future_end_idx],
        SOC_SSP585[future_start_idx - 113:future_end_idx - 113], 1)
    soc_ssp585_trend_line = (soc_ssp585_trend[0] * TIME_RANGE[future_start_idx:future_end_idx]
                             + soc_ssp585_trend[1])
    ax.plot(TIME_RANGE[future_start_idx:future_end_idx], soc_ssp585_trend_line,
            color=SOC_SSP585_COLOR, linestyle='-', linewidth=3, alpha=0.9, zorder=7)
    slope_value = soc_ssp585_trend[0]
    ax.text(TIME_RANGE[future_end_idx] - 25, soc_ssp585_trend_line[-1] - 0.03,
            f"SOC slope: {slope_value:.4f}", color=SOC_SSP585_COLOR,
            fontsize=14, va='center', zorder=8)

    # Rh historical trend
    rh_hist_trend = np.polyfit(
        TIME_RANGE[hist_start_idx:hist_end_idx],
        RH_HISTORICAL[hist_start_idx:hist_end_idx], 1)
    rh_hist_trend_line = (rh_hist_trend[0] * TIME_RANGE[hist_start_idx:hist_end_idx]
                          + rh_hist_trend[1])
    ax2.plot(TIME_RANGE[hist_start_idx:hist_end_idx], rh_hist_trend_line,
             color=RH_HIST_COLOR, linestyle='-', linewidth=3, alpha=0.9, zorder=7)
    slope_value = rh_hist_trend[0]
    ax2.text(TIME_RANGE[hist_end_idx] - 25, rh_hist_trend_line[-1] + 0.01,
             f"Rh slope: {slope_value:.4f}", color=RH_HIST_COLOR,
             fontsize=14, va='center', zorder=8)

    # Rh SSP126 trend
    rh_ssp126_trend = np.polyfit(
        TIME_RANGE[future_start_idx:future_end_idx],
        RH_SSP126[future_start_idx - 113:future_end_idx - 113], 1)
    rh_ssp126_trend_line = (rh_ssp126_trend[0] * TIME_RANGE[future_start_idx:future_end_idx]
                            + rh_ssp126_trend[1])
    ax2.plot(TIME_RANGE[future_start_idx:future_end_idx], rh_ssp126_trend_line,
             color=RH_SSP126_COLOR, linestyle='-', linewidth=3, alpha=0.9, zorder=7)

    # Rh SSP585 trend
    rh_ssp585_trend = np.polyfit(
        TIME_RANGE[future_start_idx:future_end_idx],
        RH_SSP585[future_start_idx - 113:future_end_idx - 113], 1)
    rh_ssp585_trend_line = (rh_ssp585_trend[0] * TIME_RANGE[future_start_idx:future_end_idx]
                            + rh_ssp585_trend[1])
    ax2.plot(TIME_RANGE[future_start_idx:future_end_idx], rh_ssp585_trend_line,
             color=RH_SSP585_COLOR, linestyle='-', linewidth=3, alpha=0.9, zorder=7)
    slope_value = rh_ssp585_trend[0]
    ax2.text(TIME_RANGE[future_end_idx] - 25, rh_ssp585_trend_line[-1],
             f"Rh slope: {slope_value:.4f}", color=RH_SSP585_COLOR,
             fontsize=14, va='center', zorder=8)

    ax.axvspan(HIST_PERIOD[0], HIST_PERIOD[1], facecolor='none', edgecolor='black',
               linestyle='--', linewidth=1, alpha=0.7, zorder=4)
    ax.axvspan(FUTURE_PERIOD[0], FUTURE_PERIOD[1], facecolor='none',
               edgecolor='black', linestyle='--', linewidth=1, alpha=0.7, zorder=4)

    ax.text(np.mean(HIST_PERIOD),
            ax.get_ylim()[0] + 0.05 * (ax.get_ylim()[1] - ax.get_ylim()[0]),
            '1985-2014', fontsize=16, ha='center', va='bottom', color='black')
    ax.text(np.mean(FUTURE_PERIOD),
            ax.get_ylim()[0] + 0.05 * (ax.get_ylim()[1] - ax.get_ylim()[0]),
            '2070-2099', fontsize=16, ha='center', va='bottom', color='black')

    ax.set_xlabel('Year', fontsize=18)
    ax.set_ylabel('$SOC$ (kg C m$^{-2}$)',
                  fontsize=18, color=SOC_HIST_COLOR)
    ax.tick_params(axis='y', labelcolor=SOC_HIST_COLOR, labelsize=16)

    ax.set_title("Global mean SOC stocks and Rh fluxes from 1901 to 2100",
                 fontsize=20, pad=20)

    ax2.set_ylabel('$R_h$ (kg C m$^{-2}$ yr$^{-1}$)',
                   fontsize=18, color=SOC_HIST_COLOR)
    ax2.tick_params(axis='y', labelcolor=SOC_HIST_COLOR, labelsize=16)

    ax.tick_params(axis='x', labelsize=16)
    ax.set_xlim(1900, 2100)

    lines = [soc_hist_line, soc_ssp126_line, soc_ssp585_line,
             rh_hist_line, rh_ssp126_line, rh_ssp585_line]
    labels = [line.get_label() for line in lines]

    ax.legend(lines, labels, fontsize=16, loc='upper left',
              bbox_to_anchor=(0.02, 0.98),
              frameon=False, framealpha=0.9, edgecolor='none')

    ax.text(0, 1.10, '(a)', fontweight='bold', transform=ax.transAxes,
            fontsize=22, va='top', ha='left')

    ax.grid(False)
    ax.set_facecolor('white')
    ax2.set_facecolor('white')

    fig.tight_layout()


def plot_fig4b(fig, ax):
    Rh_data = xr.open_dataset(
        "/mnt/softwares/Drought_And_SOC/000_observasion_data_ERA5/"
        "01_preprocessed_data/merged_csoil_data.nc")['cSoil']

    ax.set_extent([-170, 180, -60, 90], crs=ccrs.PlateCarree())

    lons = Rh_data.lon.values
    lats = Rh_data.lat.values

    lon_min, lon_max = Rh_data.lon.min().values, Rh_data.lon.max().values
    lat_min, lat_max = Rh_data.lat.min().values, Rh_data.lat.max().values

    d_lon = (lon_max - lon_min) / len(Rh_data.lon)
    d_lat = (lat_max - lat_min) / len(Rh_data.lat)

    vmin = Rh_data.min().item()
    vmax = Rh_data.max().item()
    cmap = cmap_obs
    norm = mpl.colors.BoundaryNorm(levels_obs, cmap.N)

    for i in range(len(lats)):
        for j in range(len(lons)):
            if np.isnan(Rh_data[i, j].item()):
                continue

            value = Rh_data[i, j].item()

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

    ax.add_feature(cfeature.LAND, facecolor='white', edgecolor='black',
                   linewidth=0.5)
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
    sm.set_array(levels_obs)
    cbar = add_unified_colorbar(fig, ax, sm, "SOC benchmark (kg C $m^{-2}$)")

    ax.text(-0.05, 1.05, '(b)',
            fontweight='bold',
            transform=ax.transAxes,
            fontsize=22,
            va='top', ha='left',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    return sm


def plot_fig4c(fig, ax):
    Rh_hist = xr.open_dataset(
        "/run/media/yue/Elements SE/008_Screening_data_CMIP6/"
        "soc/soc_historical_1985-2014.nc")['soc'].sel(
        time=slice('1985-01-01', '2014-12-31')).mean(dim='time')
    Rh_ssp126_future = xr.open_dataset(
        "/run/media/yue/Elements SE/008_Screening_data_CMIP6/"
        "soc/soc_ssp126_2070-2099.nc")['soc'].sel(
        time=slice('2070-01-01', '2099-12-31')).mean(dim='time')
    Rh_data = (Rh_ssp126_future - Rh_hist) / Rh_hist * 100
    Rh_data = xr.where(Rh_data > 100, 100, Rh_data)
    Rh_data_change = Rh_ssp126_future - Rh_hist
    Rh_data_change = xr.where(Rh_data_change > 0, 1,
                              xr.where(Rh_data_change < 0, -1, 0))
    model_change = {}
    model_change['MMWM'] = Rh_data_change
    for model in COMMON_MODELS:
        model_hist = xr.open_dataset(
            f"/run/media/yue/Elements SE/007_CorrectAndRepair_data_CMIP6/"
            f"{model}/{model}_SeasonAndLand_corrected_soc.nc")['ssp126_soc'].sel(
            time=slice('1985-01-01', '2014-12-31')).mean(dim='time')
        model_future = xr.open_dataset(
            f"/run/media/yue/Elements SE/007_CorrectAndRepair_data_CMIP6/"
            f"{model}/{model}_SeasonAndLand_corrected_soc.nc")['ssp126_soc'].sel(
            time=slice('2070-01-01', '2099-12-31')).mean(dim='time')
        model_change_data = model_future - model_hist
        model_change_data = xr.where(model_change_data > 0, 1,
                                     xr.where(model_change_data < 0, -1, 0))
        model_change[model] = model_change_data

    agreement_increase = xr.zeros_like(model_change['MMWM'])
    agreement_decrease = xr.zeros_like(model_change['MMWM'])

    for model in COMMON_MODELS:
        if model != 'MMWM':
            agreement_increase += (model_change['MMWM'] == 1) & (
                model_change[model] == 1)
            agreement_decrease += (model_change['MMWM'] == -1) & (
                model_change[model] == -1)

    total_others = len(COMMON_MODELS)
    agreement_mask_increase = (agreement_increase / total_others) >= 5 / 7
    agreement_mask_decrease = (agreement_decrease / total_others) >= 5 / 7

    mask_increase = xr.where(agreement_mask_increase & (model_change['MMWM'] == 1),
                             1, np.nan)
    mask_decrease = xr.where(agreement_mask_decrease & (model_change['MMWM'] == -1),
                             -1, np.nan)

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
    norm = plt.Normalize(-50, 51)

    for i in range(len(lats)):
        for j in range(len(lons)):
            if np.isnan(Rh_data[i, j].item()):
                continue

            value = Rh_data[i, j].item()

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

    mask_points = np.where(np.isfinite(final_mask.values))
    final_mask_lons = final_mask.lon.values[mask_points[1]]
    final_mask_lats = final_mask.lat.values[mask_points[0]]
    ax.scatter(final_mask_lons, final_mask_lats, color='black', s=0.3,
               alpha=0.7, transform=ccrs.PlateCarree(), zorder=3)

    ax.add_feature(cfeature.LAND, facecolor='white', edgecolor='black',
                   linewidth=0.5)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)

    hotpoint = {
        '(a)': [-24.1, 1.5, -60.5, -34.5],
        '(b)': [18.3, 34.9, -119.9, -78.7],
        '(c)': [-38.8, -10.2, 114.1, 154.5],
        '(d)': [21.0, 34.0, 99.4, 123.1],
        '(e)': [-35.0, -12.8, 9.7, 50.6],
        '(f)': [35.2, 56.1, -12.5, 70.3]
    }
    for dd in hotpoint.keys():
        draw_rectange_map(hotpoint, dd, fig=fig, ax=ax,
                          extent=[-180, 180, -60, 90])

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

    ax.text(0, 1, '(c)',
            fontweight='bold',
            transform=ax.transAxes,
            fontsize=22,
            va='top', ha='left',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    return sm


def plot_fig4d(fig, ax):
    Rh_hist = xr.open_dataset(
        "/run/media/yue/Elements SE/008_Screening_data_CMIP6/"
        "soc/soc_historical_1985-2014.nc")['soc'].sel(
        time=slice('1985-01-01', '2014-12-31')).mean(dim='time')
    Rh_ssp585_future = xr.open_dataset(
        "/run/media/yue/Elements SE/008_Screening_data_CMIP6/"
        "soc/soc_ssp585_2070-2099.nc")['soc'].sel(
        time=slice('2070-01-01', '2099-12-31')).mean(dim='time')
    Rh_data = (Rh_ssp585_future - Rh_hist) / Rh_hist * 100
    Rh_data = xr.where(Rh_data > 100, 100, Rh_data)
    Rh_data_change = Rh_ssp585_future - Rh_hist
    Rh_data_change = xr.where(Rh_data_change > 0, 1,
                              xr.where(Rh_data_change < 0, -1, 0))
    model_change = {}
    model_change['MMWM'] = Rh_data_change
    for model in COMMON_MODELS:
        model_hist = xr.open_dataset(
            f"/run/media/yue/Elements SE/007_CorrectAndRepair_data_CMIP6/"
            f"{model}/{model}_SeasonAndLand_corrected_soc.nc")['ssp585_soc'].sel(
            time=slice('1985-01-01', '2014-12-31')).mean(dim='time')
        model_future = xr.open_dataset(
            f"/run/media/yue/Elements SE/007_CorrectAndRepair_data_CMIP6/"
            f"{model}/{model}_SeasonAndLand_corrected_soc.nc")['ssp585_soc'].sel(
            time=slice('2070-01-01', '2099-12-31')).mean(dim='time')
        model_change_data = model_future - model_hist
        model_change_data = xr.where(model_change_data > 0, 1,
                                     xr.where(model_change_data < 0, -1, 0))
        model_change[model] = model_change_data

    agreement_increase = xr.zeros_like(model_change['MMWM'])
    agreement_decrease = xr.zeros_like(model_change['MMWM'])

    for model in COMMON_MODELS:
        if model != 'MMWM':
            agreement_increase += (model_change['MMWM'] == 1) & (
                model_change[model] == 1)
            agreement_decrease += (model_change['MMWM'] == -1) & (
                model_change[model] == -1)

    total_others = len(COMMON_MODELS)
    agreement_mask_increase = (agreement_increase / total_others) >= 5 / 7
    agreement_mask_decrease = (agreement_decrease / total_others) >= 5 / 7

    mask_increase = xr.where(agreement_mask_increase & (model_change['MMWM'] == 1),
                             1, np.nan)
    mask_decrease = xr.where(agreement_mask_decrease & (model_change['MMWM'] == -1),
                             -1, np.nan)

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
    norm = plt.Normalize(-50, 51)

    for i in range(len(lats)):
        for j in range(len(lons)):
            if np.isnan(Rh_data[i, j].item()):
                continue

            value = Rh_data[i, j].item()

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

    mask_points = np.where(np.isfinite(final_mask.values))
    final_mask_lons = final_mask.lon.values[mask_points[1]]
    final_mask_lats = final_mask.lat.values[mask_points[0]]
    ax.scatter(final_mask_lons, final_mask_lats, color='black', s=0.3,
               alpha=0.7, transform=ccrs.PlateCarree(), zorder=3)

    ax.add_feature(cfeature.LAND, facecolor='white', edgecolor='black',
                   linewidth=0.5)
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
    cbar = add_unified_colorbar(fig, ax, sm, "Future $SOC$ Change SSP5-8.5 (%)")
    cbar.set_ticks(np.arange(-50, 51, 20))

    ax.text(-0.05, 1.05, '(c)',
            fontweight='bold',
            transform=ax.transAxes,
            fontsize=22,
            va='top', ha='left',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    return sm


def plot_fig4e(fig, ax):
    MMEMean_data = xr.open_dataset(
        "/run/media/yue/Elements SE/007-1_MEM_data_CMIP6/raw/soc_MMEM.nc")['ssp126_soc'].sel(
        time=slice('1985-01-01', '2014-12-31')).mean(dim='time')
    MMWMean_data = xr.open_dataset(
        "/run/media/yue/Elements SE/007-2_MMWM_data_CMIP6/raw/soc_MMWM.nc")['ssp126_soc'].sel(
        time=slice('1985-01-01', '2014-12-31')).mean(dim='time')
    Rh_data = xr.open_dataset(
        "/mnt/softwares/Drought_And_SOC/000_observasion_data_ERA5/"
        "01_preprocessed_data/merged_csoil_data.nc")

    latitudes = Rh_data.lat.values

    MMEMean_relative_mean = MMEMean_data.mean(dim='lon')
    MMEMean_relative_std = MMEMean_data.std(dim='lon')

    MMWMean_relative_mean = MMWMean_data.mean(dim='lon')
    MMWMean_relative_std = MMWMean_data.std(dim='lon')

    Obs_median_mean = Rh_data['cSoil'].mean(dim='lon')
    Obs_median_std = Rh_data['cSoil'].std(dim='lon')

    mean_line1, = ax.plot(MMEMean_relative_mean, latitudes, color='darkred',
                          linewidth=2, linestyle='-', label='MMEM')

    ax.fill_betweenx(latitudes, MMEMean_relative_mean - MMEMean_relative_std,
                     MMEMean_relative_mean + MMEMean_relative_std,
                     color='lightcoral', alpha=0.5)

    mean_line2, = ax.plot(MMWMean_relative_mean, latitudes,
                          color='darkblue',
                          linewidth=2,
                          linestyle='--',
                          label='MMWM')

    ax.fill_betweenx(latitudes,
                     MMWMean_relative_mean - MMWMean_relative_std,
                     MMWMean_relative_mean + MMWMean_relative_std,
                     color='skyblue',
                     alpha=0.5)

    median_line, = ax.plot(Obs_median_mean, latitudes,
                           color='black',
                           linewidth=2,
                           label='SOC benchmark')

    ax.fill_betweenx(latitudes,
                     Obs_median_mean - Obs_median_std,
                     Obs_median_mean + Obs_median_std,
                     facecolor='none',
                     edgecolor='black',
                     hatch='.',
                     alpha=0.7,
                     linewidth=1,
                     zorder=2)

    ax.set_xlabel("$SOC$ (kg C $m^{-2}$)", fontsize=20)
    ax.set_ylabel("Latitude(°N)", fontsize=20)

    ax.grid(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)

    ax.legend(fontsize=15, loc='lower center',
              bbox_to_anchor=(0.5, -0.42))

    ax.set_yticks(np.arange(-60, 91, 30))
    ax.set_xlim(auto=True)

    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.tick_params(axis='both', which='minor', labelsize=12)

    ax.axvline(x=0, color='gray', linestyle='--', alpha=0.7)

    ax.text(-0.4, 1, '(d)',
            fontweight='bold',
            transform=ax.transAxes,
            fontsize=22,
            va='top', ha='left',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))


def plot_fig4f(fig, ax):
    MMEMean_historical = xr.open_dataset(
        "/run/media/yue/Elements SE/007-1_MEM_data_CMIP6/raw/soc_MMEM.nc")['ssp126_soc'].sel(
        time=slice('1985-01-01', '2014-12-31')).mean(dim='time')
    MMEMean_future = xr.open_dataset(
        "/run/media/yue/Elements SE/007-1_MEM_data_CMIP6/raw/soc_MMEM.nc")['ssp126_soc'].sel(
        time=slice('2070-01-01', '2099-12-31')).mean(dim='time')
    MMWMean_historical = xr.open_dataset(
        "/run/media/yue/Elements SE/007-2_MMWM_data_CMIP6/raw/soc_MMWM.nc")['ssp126_soc'].sel(
        time=slice('1985-01-01', '2014-12-31')).mean(dim='time')
    MMWMean_future = xr.open_dataset(
        "/run/media/yue/Elements SE/007-2_MMWM_data_CMIP6/raw/soc_MMWM.nc")['ssp126_soc'].sel(
        time=slice('2070-01-01', '2099-12-31')).mean(dim='time')
    Rh_data = xr.open_dataset(
        "/mnt/softwares/Drought_And_SOC/000_observasion_data_ERA5/"
        "01_preprocessed_data/merged_csoil_data.nc")

    latitudes = Rh_data.lat.values

    MMEMean_relative = MMEMean_future - MMEMean_historical
    MMEMean_relative_mean = MMEMean_relative.mean(dim='lon')
    MMEMean_relative_std = MMEMean_relative.std(dim='lon')

    MMWMean_relative = MMWMean_future - MMWMean_historical
    MMWMean_relative_mean = MMWMean_relative.mean(dim='lon')
    MMWMean_relative_std = MMWMean_relative.std(dim='lon')

    mean_line1, = ax.plot(MMEMean_relative_mean, latitudes, color='darkred',
                          linewidth=2, linestyle='-', label='MMEM')

    ax.fill_betweenx(latitudes, MMEMean_relative_mean - MMEMean_relative_std,
                     MMEMean_relative_mean + MMEMean_relative_std,
                     color='lightcoral', alpha=0.5)

    mean_line2, = ax.plot(MMWMean_relative_mean, latitudes,
                          color='darkblue',
                          linewidth=2,
                          linestyle='--',
                          label='MMWM')

    ax.fill_betweenx(latitudes,
                     MMWMean_relative_mean - MMWMean_relative_std,
                     MMWMean_relative_mean + MMWMean_relative_std,
                     color='skyblue',
                     alpha=0.5)

    ax.set_xlabel("$SOC$ change\nSSP1-2.6\n(kg C $m^{-2}$)", fontsize=20)
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

    ax.text(-0.4, 1, '(e)',
            fontweight='bold',
            transform=ax.transAxes,
            fontsize=22,
            va='top', ha='left',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))


def plot_fig4g(fig, ax):
    MMEMean_historical = xr.open_dataset(
        "/run/media/yue/Elements SE/007-1_MEM_data_CMIP6/raw/soc_MMEM.nc")['ssp585_soc'].sel(
        time=slice('1985-01-01', '2014-12-31')).mean(dim='time')
    MMEMean_future = xr.open_dataset(
        "/run/media/yue/Elements SE/007-1_MEM_data_CMIP6/raw/soc_MMEM.nc")['ssp585_soc'].sel(
        time=slice('2070-01-01', '2099-12-31')).mean(dim='time')
    MMWMean_historical = xr.open_dataset(
        "/run/media/yue/Elements SE/007-2_MMWM_data_CMIP6/raw/soc_MMWM.nc")['ssp585_soc'].sel(
        time=slice('1985-01-01', '2014-12-31')).mean(dim='time')
    MMWMean_future = xr.open_dataset(
        "/run/media/yue/Elements SE/007-2_MMWM_data_CMIP6/raw/soc_MMWM.nc")['ssp585_soc'].sel(
        time=slice('2070-01-01', '2099-12-31')).mean(dim='time')
    Rh_data = xr.open_dataset(
        "/mnt/softwares/Drought_And_SOC/000_observasion_data_ERA5/"
        "01_preprocessed_data/merged_csoil_data.nc")

    latitudes = Rh_data.lat.values

    MMEMean_relative = MMEMean_future - MMEMean_historical
    MMEMean_relative_mean = MMEMean_relative.mean(dim='lon')
    MMEMean_relative_std = MMEMean_relative.std(dim='lon')

    MMWMean_relative = MMWMean_future - MMWMean_historical
    MMWMean_relative_mean = MMWMean_relative.mean(dim='lon')
    MMWMean_relative_std = MMWMean_relative.std(dim='lon')

    mean_line1, = ax.plot(MMEMean_relative_mean, latitudes, color='darkred',
                          linewidth=2, linestyle='-', label='MMEM')

    ax.fill_betweenx(latitudes, MMEMean_relative_mean - MMEMean_relative_std,
                     MMEMean_relative_mean + MMEMean_relative_std,
                     color='lightcoral', alpha=0.5)

    mean_line2, = ax.plot(MMWMean_relative_mean, latitudes,
                          color='darkblue',
                          linewidth=2,
                          linestyle='--',
                          label='MMWM')

    ax.fill_betweenx(latitudes,
                     MMWMean_relative_mean - MMWMean_relative_std,
                     MMWMean_relative_mean + MMWMean_relative_std,
                     color='skyblue',
                     alpha=0.5)

    ax.set_xlabel("$SOC$ change\nSSP5-8.5\n(kg C $m^{-2}$)", fontsize=20)
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

    ax.text(-0.4, 1, '(e)',
            fontweight='bold',
            transform=ax.transAxes,
            fontsize=22,
            va='top', ha='left',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))


def create_figure4():
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams['axes.edgecolor'] = 'black'
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Arial'],
        'font.sans-serif': ['Times New Roman'],
    })

    fig = plt.figure(figsize=(16, 20))
    gs = gridspec.GridSpec(3, 2, width_ratios=[6, 1], height_ratios=[3, 4, 4],
                           figure=fig, wspace=0.15, hspace=0.45,
                           top=0.95, bottom=0.07, left=0.1, right=0.99)

    ax1 = fig.add_subplot(gs[0, :])
    plot_fig4a(fig, ax1)

    ax2 = fig.add_subplot(gs[2], projection=ccrs.Robinson(central_longitude=10))
    plot_fig4b(fig, ax2)

    ax3 = fig.add_subplot(gs[3])
    plot_fig4e(fig, ax3)

    ax4 = fig.add_subplot(gs[4], projection=ccrs.Robinson(central_longitude=10))
    plot_fig4d(fig, ax4)

    ax5 = fig.add_subplot(gs[5])
    plot_fig4g(fig, ax5)

    ax1_position = ax1.get_position()
    new_ax1_position = [ax1_position.x0, ax1_position.y0 - 0.05,
                        ax1_position.width, ax1_position.height]
    ax1.set_position(new_ax1_position)

    fig.canvas.draw()

    png_path = os.path.join(OUTPUT_DIR, "Figure4.png")
    fig.savefig(png_path, dpi=600, bbox_inches='tight')
    pdf_path = os.path.join(OUTPUT_DIR, "Figure4.pdf")
    fig.savefig(pdf_path, dpi=600, bbox_inches='tight')
    print(f"Figure saved to: {pdf_path}")

    plt.close()


if __name__ == '__main__':
    create_figure4()
