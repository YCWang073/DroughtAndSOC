import matplotlib.patches as patches
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import geopandas as gpd
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import numpy as np
from matplotlib import gridspec
import matplotlib as mpl
from matplotlib.offsetbox import AnnotationBbox, DrawingArea
from matplotlib.patches import Wedge
from shapely.geometry.geo import mapping
from matplotlib.colors import TwoSlopeNorm
from matplotlib import cm
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import math
import os
import warnings

from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.lines import Line2D

OUTPUT_DIR = "res/eiar_figs"
os.makedirs(OUTPUT_DIR, exist_ok=True)
warnings.filterwarnings("ignore")


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
    ax.plot([hotpoint[dd][2], hotpoint[dd][3]], [hotpoint[dd][1], hotpoint[dd][1]], transform=ccrs.PlateCarree(), linewidth=linewi, color='k', ls=lines)
    ax.plot([hotpoint[dd][2], hotpoint[dd][3]], [hotpoint[dd][0], hotpoint[dd][0]], transform=ccrs.PlateCarree(), linewidth=linewi, color='k', ls=lines)
    ax.plot([hotpoint[dd][2], hotpoint[dd][2]], [hotpoint[dd][0], hotpoint[dd][1]], transform=ccrs.PlateCarree(), linewidth=linewi, color='k', ls=lines)
    ax.plot([hotpoint[dd][3], hotpoint[dd][3]], [hotpoint[dd][0], hotpoint[dd][1]], transform=ccrs.PlateCarree(), linewidth=linewi, color='k', ls=lines)


def _parse_hist_fut_classes(da_change):
    v = da_change.values
    v = np.array(v, dtype=np.int16)
    hist = v // 10
    fut = v % 10
    return hist, fut


def _agg_by_hist_class(delta_arr, hist_cls, class_id):
    delta_arr_flat = delta_arr.values.ravel()
    hist_cls_flat = hist_cls.ravel()
    mask = (hist_cls_flat == class_id) & np.isfinite(delta_arr_flat)
    if mask.sum() == 0:
        return np.nan, 0, np.nan
    vals = delta_arr_flat[mask]
    med = np.nanmedian(vals)
    n = vals.size
    up = float(np.mean(vals > 0))
    return med, n, up


def _col_stats(vals_list):
    out = []
    for arr in vals_list:
        arr_flat = arr.values.ravel()
        arr_flat = arr_flat[np.isfinite(arr_flat)]
        if arr_flat.size == 0:
            out.append((np.nan, np.nan, np.nan))
        else:
            out.append((
                float(np.median(arr_flat)),
                float(np.percentile(arr_flat, 2.5)),
                float(np.percentile(arr_flat, 97.5))
            ))
    return out


def _transition_stats(delta_da, lc_change_da):
    delta = np.asarray(delta_da.values)
    lcc = np.asarray(lc_change_da.values)
    valid = np.isfinite(delta) & np.isfinite(lcc)
    delta = delta[valid]
    lcc = lcc[valid].astype(np.int16)
    med = np.full((6, 6), np.nan, dtype=np.float64)
    cnt = np.zeros((6, 6), dtype=np.int64)
    hist_cls = (lcc // 10)
    futu_cls = (lcc % 10)
    for i in range(1, 7):
        for j in range(1, 7):
            m = (hist_cls == i) & (futu_cls == j)
            if np.any(m):
                vals = delta[m]
                cnt[i-1, j-1] = vals.size
                med[i-1, j-1] = np.nanmedian(vals)
    return med, cnt


def _draw_heatmap(ax, mat, counts, title, vmin, vmax, showY=False, ssp='ssp585'):
    classes = ["Cropland", "Forest", "Grassland", "Urban", "Barren", "Water"]
    norm = TwoSlopeNorm(vmin=vmin, vcenter=0.0, vmax=vmax)
    im = ax.imshow(mat, origin='upper', cmap=cm.get_cmap("BrBG"), norm=norm,
                   extent=(0.5, 6.5, 6.5, 0.5), aspect='equal', interpolation='nearest')
    if np.nanmax(counts) > 0:
        xs = np.arange(1, 7)
        ys = np.arange(1, 7)
        X, Y = np.meshgrid(xs, ys)
        s = (counts / np.nanmax(counts))
        s = np.sqrt(s)
        ax.scatter(X.ravel(), Y.ravel(), s=(s.ravel()*800),
                   facecolors='none', edgecolors='#FFFFFF',
                   linewidths=2.0, alpha=0.9, zorder=4)
        ax.scatter(X.ravel(), Y.ravel(), s=(s.ravel()*800),
                   facecolors='none', edgecolors='#1460F3',
                   linewidths=1.2, alpha=0.9, zorder=5)
    for k in range(1, 7):
        ax.axhline(k+0.5, color='white', lw=0.8, alpha=0.7)
        ax.axvline(k+0.5, color='white', lw=0.8, alpha=0.7)
    ax.set_xticks(np.arange(1, 7))
    ax.set_xticklabels(classes, rotation=35, ha='right', fontsize=16)
    if ssp == 'ssp585':
        ax.set_xlabel("SSP5-8.5 land-cover class", fontsize=16)
    elif ssp == 'ssp370':
        ax.set_xlabel("SSP3-7.0 land-cover class", fontsize=16)
    elif ssp == 'ssp245':
        ax.set_xlabel("SSP2-4.5 land-cover class", fontsize=16)
    elif ssp == 'ssp126':
        ax.set_xlabel("SSP1-2.6 land-cover class", fontsize=16)
    if showY:
        ax.text(-0.1, 1.07, '(a)',
                fontweight='bold',
                transform=ax.transAxes,
                fontsize=22,
                va='top', ha='left')
        ax.set_ylabel("Historical land-cover class", fontsize=16)
        ax.set_yticklabels(classes, fontsize=16)
        ax.set_yticks(np.arange(1, 7))
    else:
        ax.set_yticks([])
        ax.set_yticklabels([])
        ax.set_ylabel("")
    ax.set_title(title, fontsize=16)
    return im


def reshape(ds1, ds2):
    ds1['lon'] = (ds1['lon'] + 180) % 360 - 180
    ds1 = ds1.sortby('lon')
    ds2['lon'] = (ds2['lon'] + 180) % 360 - 180
    ds2 = ds2.sortby('lon')
    ds1 = ds1.roll(lon=len(ds1['lon']) // 2, roll_coords='lon')
    ds1 = ds1.interp(lat=ds2.lat, lon=ds2.lon, method='nearest')
    return ds1


def re_prj(ds):
    if 'grid_mapping' in ds.attrs:
        del ds.attrs['grid_mapping']
    shp = gpd.read_file(r"/mnt/softwares/Drought_And_SOC/001_shape_data_GIS/ne_50m_land.shp")
    ds.rio.set_spatial_dims(x_dim="lon", y_dim="lat", inplace=True)
    ds.rio.write_crs(shp.crs, inplace=True)
    dsre = ds.rio.clip(shp.geometry.apply(mapping), shp.crs, drop=False)
    mask_path = "/mnt/softwares/Drought_And_SOC/Pokhrel_NCC2021_ISIMIP_TWS_reshaped.nc"
    mask = xr.open_dataset(mask_path)['tws_ref'].isel(time=0).load()
    dsre = dsre.interp_like(mask, method='nearest')
    dsre = dsre.where(~np.isnan(mask))
    return dsre


def km_per_deg(lat_deg):
    k_lat = 110.574
    k_lon = 111.320 * math.cos(math.radians(lat_deg))
    return k_lat, k_lon


def wh_km(latmin, latmax, lonmin, lonmax):
    dlat = latmax - latmin
    dlon = lonmax - lonmin
    latc = 0.5*(latmin + latmax)
    k_lat, k_lon = km_per_deg(latc)
    W = abs(dlon) * k_lon
    H = abs(dlat) * k_lat
    return W, H, latc


def pad_extent_both(latmin, latmax, lonmin, lonmax, target_ratio, margin_frac=0.02):
    W, H, latc = wh_km(latmin, latmax, lonmin, lonmax)
    r = W/H
    k_lat, k_lon = km_per_deg(latc)
    dlat0 = (latmax - latmin)/2
    dlon0 = (lonmax - lonmin)/2
    if r < target_ratio:
        W_need = target_ratio * H
        dlon_need = (W_need / k_lon) / 2.0
        dlon = max(dlon0, dlon_need)
        dlat = dlat0
    else:
        H_need = W / target_ratio
        dlat_need = (H_need / k_lat) / 2.0
        dlat = max(dlat0, dlat_need)
        dlon = dlon0
    dlat *= (1 + margin_frac)
    dlon *= (1 + margin_frac)
    latc = 0.5*(latmin + latmax)
    lonc = 0.5*(lonmin + lonmax)
    latmin_p = max(-90.0,  latc - dlat)
    latmax_p = min( 90.0,  latc + dlat)
    lonmin_p = max(-180.0, lonc - dlon)
    lonmax_p = min( 180.0, lonc + dlon)
    return latmin_p, latmax_p, lonmin_p, lonmax_p


landmask = xr.open_dataset("/run/media/yue/Elements SE/008_Screening_data_CMIP6/Masks/landmask.nc")['mask']
base_proj_path = "/mnt/softwares/Drought_And_SOC/Pokhrel_NCC2021_ISIMIP_TWS_reshaped.nc"
base_proj_ds = xr.open_dataset(base_proj_path)
LANDCOVER_CHANGE = xr.open_dataset(f"/mnt/softwares/Drought_And_SOC/001-1_land_use_data_TIFF/result/ssp245_land_cover_change.nc")['land_cover_change']
LANDCOVER_CHANGE = reshape(LANDCOVER_CHANGE, base_proj_ds)
LANDCOVER_CHANGE = re_prj(LANDCOVER_CHANGE)

INDEX_COLORS = {"SPEI": "#fca525", "SSMI": "#27c5cd", "STI": "#eb4116"}
LC_LABELS = ["Cropland", "Forest", "Grassland", "Urban", "Barren", "Water"]


def _slice_region(da, bounds):
    return da.sel(lat=slice(bounds[0], bounds[1]), lon=slice(bounds[2], bounds[3]))


def _median_ci(a, q=(2.5, 97.5)):
    a = np.asarray(a).ravel()
    a = a[np.isfinite(a)]
    if a.size == 0:
        return np.nan, (np.nan, np.nan)
    return float(np.median(a)), (float(np.percentile(a, q[0])), float(np.percentile(a, q[1])))


def _add_three_axes_below(fig, host_ax, map_frac=0.62, dumbbell_frac=0.18, heatmap_frac=0.20, h_gap=0.05, w_gap=0.2):
    pos = host_ax.get_position()
    fig.canvas.draw_idle()
    host_ax.remove()
    H, W = pos.height, pos.width
    gapH = h_gap * H
    gapW = w_gap * W
    h_map = H * map_frac
    h_bottom = H * (dumbbell_frac + heatmap_frac)
    y_bottom = pos.y0
    y_map = y_bottom + h_bottom + gapH
    ax_map = fig.add_axes([pos.x0, y_map, W, h_map], projection=ccrs.PlateCarree())
    db_w = 0.50 * W - gapW / 2.0
    hm_w = 0.50 * W - gapW / 2.0
    x_db = pos.x0
    x_hm = pos.x0 + db_w + gapW
    ax_db = fig.add_axes([x_db, y_bottom, db_w, h_bottom])
    ax_hm = fig.add_axes([x_hm, y_bottom, hm_w, h_bottom])
    return ax_map, ax_db, ax_hm


def _plot_region_dumbbell(ax_db, bounds, spei_hist, ssmi_hist, sti_hist,
                          spei_fut, ssmi_fut, sti_fut, landmask):
    import sys
    from pathlib import Path

    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from src.review_check.land_cover_transition_plotting import (
        plot_region_magnitude_dumbbell,
    )

    return plot_region_magnitude_dumbbell(
        ax_db, bounds, spei_hist, ssmi_hist, sti_hist, spei_fut, ssmi_fut,
        sti_fut, landmask, _slice_region, INDEX_COLORS,
    )

def _plot_region_microheat(ax_hm, bounds, spei_hist, ssmi_hist, sti_hist,
                           spei_fut, ssmi_fut, sti_fut, lc_change, landmask):
    import sys
    from pathlib import Path

    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from src.review_check.land_cover_transition_plotting import (
        plot_region_transition_summary,
    )

    return plot_region_transition_summary(
        ax_hm, bounds, spei_hist, ssmi_hist, sti_hist, spei_fut, ssmi_fut,
        sti_fut, lc_change, landmask, _slice_region,
    )

def plot_figures23a(fig, ax):
    ssp = 'ssp245'
    var = 'rh'

    import sys
    from functools import partial
    from pathlib import Path

    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from src.review_check.land_cover_transition_plotting import (
        draw_transition_heatmap,
        transition_stats,
    )

    ssp_labels = {
        'ssp126': 'SSP1-2.6',
        'ssp245': 'SSP2-4.5',
        'ssp370': 'SSP3-7.0',
        'ssp585': 'SSP5-8.5',
    }
    draw_heatmap = partial(
        draw_transition_heatmap, future_label=ssp_labels[ssp]
    )

    SPEI_SOC_HISTORICAL_SEN = xr.open_dataset(
        f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/SPEI/"
        f"NORMALIZE_historical_Max_sensitivity_{var}&SPEI120.nc"
    )['max_correlation']
    SSMI_SOC_HISTORICAL_SEN = xr.open_dataset(
        f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/SSMI/"
        f"NORMALIZE_historical_Max_sensitivity_{var}&SSMI120.nc"
    )['max_correlation']
    STI_SOC_HISTORICAL_SEN = xr.open_dataset(
        f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/STI/"
        f"NORMALIZE_historical_Max_sensitivity_{var}&STI120.nc"
    )['max_correlation']
    SPEI_SOC_SSP585_SEN = xr.open_dataset(
        f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/SPEI/"
        f"NORMALIZE_{ssp}_Max_sensitivity_{var}&SPEI120.nc"
    )['max_correlation']
    SSMI_SOC_SSP585_SEN = xr.open_dataset(
        f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/SSMI/"
        f"NORMALIZE_{ssp}_Max_sensitivity_{var}&SSMI120.nc"
    )['max_correlation']
    STI_SOC_SSP585_SEN = xr.open_dataset(
        f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/STI/"
        f"NORMALIZE_{ssp}_Max_sensitivity_{var}&STI120.nc"
    )['max_correlation']

    # Compare the magnitude of the selected association, not its signed value.
    spei_delta = np.abs(SPEI_SOC_SSP585_SEN) - np.abs(SPEI_SOC_HISTORICAL_SEN)
    ssmi_delta = np.abs(SSMI_SOC_SSP585_SEN) - np.abs(SSMI_SOC_HISTORICAL_SEN)
    sti_delta = np.abs(STI_SOC_SSP585_SEN) - np.abs(STI_SOC_HISTORICAL_SEN)

    spei_mat, spei_count = transition_stats(spei_delta, LANDCOVER_CHANGE)
    ssmi_mat, ssmi_count = transition_stats(ssmi_delta, LANDCOVER_CHANGE)
    sti_mat, sti_count = transition_stats(sti_delta, LANDCOVER_CHANGE)

    values = np.concatenate([spei_mat.ravel(), ssmi_mat.ravel(), sti_mat.ravel()])
    values = values[np.isfinite(values)]
    vlim = np.nanpercentile(np.abs(values), 98) if values.size else 1.0
    if vlim == 0:
        vlim = np.nanmax(np.abs(values)) or 1.0

    position = ax.get_position()
    fig.canvas.draw_idle()
    ax.remove()

    gap = 0.03 * position.width
    width = (position.width - 2 * gap) / 3.0
    axes = [
        fig.add_axes([position.x0 + index * (width + gap), position.y0,
                      width, position.height])
        for index in range(3)
    ]

    display_var = 'SOC' if var == 'soc' else '$R_h$'
    im1 = draw_heatmap(
        axes[0], spei_mat, spei_count, f"Δ|r*|: {display_var}–SPEI",
        vmin=-vlim, vmax=vlim, showY=True,
    )
    im2 = draw_heatmap(
        axes[1], ssmi_mat, ssmi_count, f"Δ|r*|: {display_var}–SSMI",
        vmin=-vlim, vmax=vlim,
    )
    im3 = draw_heatmap(
        axes[2], sti_mat, sti_count, f"Δ|r*|: {display_var}–STI",
        vmin=-vlim, vmax=vlim,
    )

    colourbar = fig.colorbar(
        im3, ax=axes, orientation='vertical', fraction=0.025,
        pad=0.02, shrink=0.7,
    )
    colourbar.ax.tick_params(labelsize=14)
    colourbar.set_label(
        "Δ selected association magnitude (unitless)", fontsize=16
    )
    for panel_axis in axes:
        panel_axis.tick_params(axis='both', labelsize=14)
        panel_axis.set_xlim(0.5, 3.5)
        panel_axis.set_ylim(3.5, 0.5)

    return None

def plot_figures23b(fig, ax):
    ssp = 'ssp245'
    var = 'rh'
    ax_map, ax_db, ax_hm = _add_three_axes_below(fig, ax)
    SPEI_SOC_HISTORICAL_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/SPEI/NORMALIZE_historical_Max_sensitivity_{var}&SPEI120.nc")['max_correlation']
    SSMI_SOC_HISTORICAL_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/SSMI/NORMALIZE_historical_Max_sensitivity_{var}&SSMI120.nc")['max_correlation']
    STI_SOC_HISTORICAL_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/STI/NORMALIZE_historical_Max_sensitivity_{var}&STI120.nc")['max_correlation']
    SPEI_SOC_SSP585_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/SPEI/NORMALIZE_{ssp}_Max_sensitivity_{var}&SPEI120.nc")['max_correlation']
    SSMI_SOC_SSP585_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/SSMI/NORMALIZE_{ssp}_Max_sensitivity_{var}&SSMI120.nc")['max_correlation']
    STI_SOC_SSP585_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/STI/NORMALIZE_{ssp}_Max_sensitivity_{var}&STI120.nc")['max_correlation']
    NAMS = [18.3, 34.9, -119.9, -78.7]
    ADJUSTED_REGION = [14.326941783893824, 38.87305821610618, -120.31200000000001, -78.28800000000001]
    SPEI_clip = SPEI_SOC_SSP585_SEN.sel(lat=slice(NAMS[0], NAMS[1]), lon=slice(NAMS[2], NAMS[3])).where(landmask == 1).__abs__()
    SSMI_clip = SSMI_SOC_SSP585_SEN.sel(lat=slice(NAMS[0], NAMS[1]), lon=slice(NAMS[2], NAMS[3])).where(landmask == 1).__abs__()
    STI_clip = STI_SOC_SSP585_SEN.sel(lat=slice(NAMS[0], NAMS[1]), lon=slice(NAMS[2], NAMS[3])).where(landmask == 1).__abs__()
    combined = xr.concat([SPEI_clip, SSMI_clip, STI_clip], dim='variable')
    all_nan_mask = np.isnan(SPEI_clip) & np.isnan(SSMI_clip) & np.isnan(STI_clip)
    max_idx = combined.fillna(-9999).argmax(dim='variable')
    max_idx = xr.where(all_nan_mask, 3, max_idx)
    cmap = mcolors.ListedColormap(['#fca525', '#27c5cd', '#eb4116', 'white'])
    norm = mcolors.BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], cmap.N)
    ax_map.set_extent([ADJUSTED_REGION[2], ADJUSTED_REGION[3], ADJUSTED_REGION[0], ADJUSTED_REGION[1]], crs=ccrs.PlateCarree())
    ax_map.add_feature(cfeature.LAND, facecolor="white", edgecolor="black", linewidth=0.5)
    ax_map.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax_map.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.5)
    ax_map.add_patch(mpatches.Rectangle((NAMS[2], NAMS[0]), NAMS[3] - NAMS[2], NAMS[1] - NAMS[0],
                                        fill=False, lw=1.0, ls='--', color='k', transform=ccrs.PlateCarree(), zorder=10))
    ax_map.pcolormesh(max_idx.lon, max_idx.lat, max_idx, cmap=cmap, norm=norm,
                      transform=ccrs.PlateCarree(), shading='auto')
    ax_map.set_title('Dominant Factor in NAMS Region', fontsize=16, loc='center', pad=2)
    _plot_region_dumbbell(ax_db, NAMS, SPEI_SOC_HISTORICAL_SEN, SSMI_SOC_HISTORICAL_SEN, STI_SOC_HISTORICAL_SEN,
                          SPEI_SOC_SSP585_SEN, SSMI_SOC_SSP585_SEN, STI_SOC_SSP585_SEN, landmask)
    _plot_region_microheat(ax_hm, NAMS, SPEI_SOC_HISTORICAL_SEN, SSMI_SOC_HISTORICAL_SEN, STI_SOC_HISTORICAL_SEN,
                           SPEI_SOC_SSP585_SEN, SSMI_SOC_SSP585_SEN, STI_SOC_SSP585_SEN, LANDCOVER_CHANGE, landmask)
    ax_map.text(-0.12, 1.05, '(b)', fontweight="bold",
                transform=ax.transAxes, fontsize=22, va="top", ha="left",
                bbox=dict(facecolor="white", alpha=0.8, edgecolor="none"))
    return None


def plot_figures23c(fig, ax):
    ssp = 'ssp245'
    var = 'rh'
    ax_map, ax_db, ax_hm = _add_three_axes_below(fig, ax)
    SPEI_SOC_HISTORICAL_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/SPEI/NORMALIZE_historical_Max_sensitivity_{var}&SPEI120.nc")['max_correlation']
    SSMI_SOC_HISTORICAL_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/SSMI/NORMALIZE_historical_Max_sensitivity_{var}&SSMI120.nc")['max_correlation']
    STI_SOC_HISTORICAL_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/STI/NORMALIZE_historical_Max_sensitivity_{var}&STI120.nc")['max_correlation']
    SPEI_SOC_SSP585_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/SPEI/NORMALIZE_{ssp}_Max_sensitivity_{var}&SPEI120.nc")['max_correlation']
    SSMI_SOC_SSP585_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/SSMI/NORMALIZE_{ssp}_Max_sensitivity_{var}&SSMI120.nc")['max_correlation']
    STI_SOC_SSP585_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/STI/NORMALIZE_{ssp}_Max_sensitivity_{var}&STI120.nc")['max_correlation']
    AMZ_SE = [-24.1, 1.5, -60.5, -34.5]
    ADJUSTED_REGION = [-24.356, 1.7560000000000002, -69.68961880527392, -25.31038119472608]
    SPEI_clip = SPEI_SOC_SSP585_SEN.sel(lat=slice(AMZ_SE[0], AMZ_SE[1]), lon=slice(AMZ_SE[2], AMZ_SE[3])).where(landmask == 1).__abs__()
    SSMI_clip = SSMI_SOC_SSP585_SEN.sel(lat=slice(AMZ_SE[0], AMZ_SE[1]), lon=slice(AMZ_SE[2], AMZ_SE[3])).where(landmask == 1).__abs__()
    STI_clip = STI_SOC_SSP585_SEN.sel(lat=slice(AMZ_SE[0], AMZ_SE[1]), lon=slice(AMZ_SE[2], AMZ_SE[3])).where(landmask == 1).__abs__()
    combined = xr.concat([SPEI_clip, SSMI_clip, STI_clip], dim='variable')
    all_nan_mask = np.isnan(SPEI_clip) & np.isnan(SSMI_clip) & np.isnan(STI_clip)
    max_idx = combined.fillna(-9999).argmax(dim='variable')
    max_idx = xr.where(all_nan_mask, 3, max_idx)
    cmap = mcolors.ListedColormap(['#fca525', '#27c5cd', '#eb4116', 'white'])
    norm = mcolors.BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], cmap.N)
    ax_map.set_extent([ADJUSTED_REGION[2], ADJUSTED_REGION[3], ADJUSTED_REGION[0], ADJUSTED_REGION[1]], crs=ccrs.PlateCarree())
    ax_map.add_feature(cfeature.LAND, facecolor="white", edgecolor="black", linewidth=0.5)
    ax_map.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax_map.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.5)
    ax_map.add_patch(mpatches.Rectangle((AMZ_SE[2], AMZ_SE[0]), AMZ_SE[3]-AMZ_SE[2], AMZ_SE[1]-AMZ_SE[0],
                                        fill=False, lw=1.0, ls='--', color='k', transform=ccrs.PlateCarree(), zorder=10))
    ax_map.pcolormesh(max_idx.lon, max_idx.lat, max_idx, cmap=cmap, norm=norm,
                      transform=ccrs.PlateCarree(), shading='auto')
    ax_map.set_title('Dominant Factor in AMZ-SE Region', fontsize=16, loc='center', pad=2)
    _plot_region_dumbbell(ax_db, AMZ_SE, SPEI_SOC_HISTORICAL_SEN, SSMI_SOC_HISTORICAL_SEN, STI_SOC_HISTORICAL_SEN,
                          SPEI_SOC_SSP585_SEN, SSMI_SOC_SSP585_SEN, STI_SOC_SSP585_SEN, landmask)
    _plot_region_microheat(ax_hm, AMZ_SE, SPEI_SOC_HISTORICAL_SEN, SSMI_SOC_HISTORICAL_SEN, STI_SOC_HISTORICAL_SEN,
                           SPEI_SOC_SSP585_SEN, SSMI_SOC_SSP585_SEN, STI_SOC_SSP585_SEN, LANDCOVER_CHANGE, landmask)
    ax_map.text(-0.12, 1.05, '(c)', fontweight="bold",
                transform=ax.transAxes, fontsize=22, va="top", ha="left",
                bbox=dict(facecolor="white", alpha=0.8, edgecolor="none"))
    return None


def plot_figures23d(fig, ax):
    ssp = 'ssp245'
    var = 'rh'
    ax_map, ax_db, ax_hm = _add_three_axes_below(fig, ax)
    SPEI_SOC_HISTORICAL_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/SPEI/NORMALIZE_historical_Max_sensitivity_{var}&SPEI120.nc")['max_correlation']
    SSMI_SOC_HISTORICAL_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/SSMI/NORMALIZE_historical_Max_sensitivity_{var}&SSMI120.nc")['max_correlation']
    STI_SOC_HISTORICAL_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/STI/NORMALIZE_historical_Max_sensitivity_{var}&STI120.nc")['max_correlation']
    SPEI_SOC_SSP585_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/SPEI/NORMALIZE_{ssp}_Max_sensitivity_{var}&SPEI120.nc")['max_correlation']
    SSMI_SOC_SSP585_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/SSMI/NORMALIZE_{ssp}_Max_sensitivity_{var}&SSMI120.nc")['max_correlation']
    STI_SOC_SSP585_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/STI/NORMALIZE_{ssp}_Max_sensitivity_{var}&STI120.nc")['max_correlation']
    MED = [35.2, 56.1, -12.5, 70.3]
    ADJUSTED_REGION = [20.938138901172, 70.361861098828015, -13.328000000000003, 71.128]
    SPEI_clip = SPEI_SOC_SSP585_SEN.sel(lat=slice(MED[0], MED[1]), lon=slice(MED[2], MED[3])).where(landmask == 1).__abs__()
    SSMI_clip = SSMI_SOC_SSP585_SEN.sel(lat=slice(MED[0], MED[1]), lon=slice(MED[2], MED[3])).where(landmask == 1).__abs__()
    STI_clip = STI_SOC_SSP585_SEN.sel(lat=slice(MED[0], MED[1]), lon=slice(MED[2], MED[3])).where(landmask == 1).__abs__()
    combined = xr.concat([SPEI_clip, SSMI_clip, STI_clip], dim='variable')
    all_nan_mask = np.isnan(SPEI_clip) & np.isnan(SSMI_clip) & np.isnan(STI_clip)
    max_idx = combined.fillna(-9999).argmax(dim='variable')
    max_idx = xr.where(all_nan_mask, 3, max_idx)
    cmap = mcolors.ListedColormap(['#fca525', '#27c5cd', '#eb4116', 'white'])
    norm = mcolors.BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], cmap.N)
    ax_map.set_extent([ADJUSTED_REGION[2], ADJUSTED_REGION[3], ADJUSTED_REGION[0], ADJUSTED_REGION[1]], crs=ccrs.PlateCarree())
    ax_map.add_feature(cfeature.LAND, facecolor="white", edgecolor="black", linewidth=0.5)
    ax_map.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax_map.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.5)
    ax_map.add_patch(mpatches.Rectangle((MED[2], MED[0]), MED[3]-MED[2], MED[1]-MED[0],
                                        fill=False, lw=1.0, ls='--', color='k', transform=ccrs.PlateCarree(), zorder=10))
    ax_map.pcolormesh(max_idx.lon, max_idx.lat, max_idx, cmap=cmap, norm=norm,
                      transform=ccrs.PlateCarree(), shading='auto')
    ax_map.set_title('Dominant Factor in MED Region', fontsize=16, loc='center', pad=2)
    _plot_region_dumbbell(ax_db, MED, SPEI_SOC_HISTORICAL_SEN, SSMI_SOC_HISTORICAL_SEN, STI_SOC_HISTORICAL_SEN,
                          SPEI_SOC_SSP585_SEN, SSMI_SOC_SSP585_SEN, STI_SOC_SSP585_SEN, landmask)
    _plot_region_microheat(ax_hm, MED, SPEI_SOC_HISTORICAL_SEN, SSMI_SOC_HISTORICAL_SEN, STI_SOC_HISTORICAL_SEN,
                           SPEI_SOC_SSP585_SEN, SSMI_SOC_SSP585_SEN, STI_SOC_SSP585_SEN, LANDCOVER_CHANGE, landmask)
    ax_map.text(-0.12, 1.05, '(d)', fontweight="bold",
                transform=ax.transAxes, fontsize=22, va="top", ha="left",
                bbox=dict(facecolor="white", alpha=0.8, edgecolor="none"))
    return None


def plot_figures23e(fig, ax):
    ssp = 'ssp245'
    var = 'rh'
    ax_map, ax_db, ax_hm = _add_three_axes_below(fig, ax)
    SPEI_SOC_HISTORICAL_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/SPEI/NORMALIZE_historical_Max_sensitivity_{var}&SPEI120.nc")['max_correlation']
    SSMI_SOC_HISTORICAL_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/SSMI/NORMALIZE_historical_Max_sensitivity_{var}&SSMI120.nc")['max_correlation']
    STI_SOC_HISTORICAL_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/STI/NORMALIZE_historical_Max_sensitivity_{var}&STI120.nc")['max_correlation']
    SPEI_SOC_SSP585_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/SPEI/NORMALIZE_{ssp}_Max_sensitivity_{var}&SPEI120.nc")['max_correlation']
    SSMI_SOC_SSP585_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/SSMI/NORMALIZE_{ssp}_Max_sensitivity_{var}&SSMI120.nc")['max_correlation']
    STI_SOC_SSP585_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/STI/NORMALIZE_{ssp}_Max_sensitivity_{var}&STI120.nc")['max_correlation']
    S_AF = [-35.0, -12.8, 9.7, 50.6]
    ADJUSTED_REGION = [-35.34253503594309, -12.45746496405691, 9.290999999999997, 51.009]
    SPEI_clip = SPEI_SOC_SSP585_SEN.sel(lat=slice(S_AF[0], S_AF[1]), lon=slice(S_AF[2], S_AF[3])).where(landmask == 1).__abs__()
    SSMI_clip = SSMI_SOC_SSP585_SEN.sel(lat=slice(S_AF[0], S_AF[1]), lon=slice(S_AF[2], S_AF[3])).where(landmask == 1).__abs__()
    STI_clip = STI_SOC_SSP585_SEN.sel(lat=slice(S_AF[0], S_AF[1]), lon=slice(S_AF[2], S_AF[3])).where(landmask == 1).__abs__()
    combined = xr.concat([SPEI_clip, SSMI_clip, STI_clip], dim='variable')
    all_nan_mask = np.isnan(SPEI_clip) & np.isnan(SSMI_clip) & np.isnan(STI_clip)
    max_idx = combined.fillna(-9999).argmax(dim='variable')
    max_idx = xr.where(all_nan_mask, 3, max_idx)
    cmap = mcolors.ListedColormap(['#fca525', '#27c5cd', '#eb4116', 'white'])
    norm = mcolors.BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], cmap.N)
    ax_map.set_extent([ADJUSTED_REGION[2], ADJUSTED_REGION[3], ADJUSTED_REGION[0], ADJUSTED_REGION[1]], crs=ccrs.PlateCarree())
    ax_map.add_feature(cfeature.LAND, facecolor="white", edgecolor="black", linewidth=0.5)
    ax_map.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax_map.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.5)
    ax_map.add_patch(mpatches.Rectangle((S_AF[2], S_AF[0]), S_AF[3]-S_AF[2], S_AF[1]-S_AF[0],
                                        fill=False, lw=1.0, ls='--', color='k', transform=ccrs.PlateCarree(), zorder=10))
    ax_map.pcolormesh(max_idx.lon, max_idx.lat, max_idx, cmap=cmap, norm=norm,
                      transform=ccrs.PlateCarree(), shading='auto')
    ax_map.set_title('Dominant Factor in S-AF Region', fontsize=16, loc='center', pad=2)
    _plot_region_dumbbell(ax_db, S_AF, SPEI_SOC_HISTORICAL_SEN, SSMI_SOC_HISTORICAL_SEN, STI_SOC_HISTORICAL_SEN,
                          SPEI_SOC_SSP585_SEN, SSMI_SOC_SSP585_SEN, STI_SOC_SSP585_SEN, landmask)
    _plot_region_microheat(ax_hm, S_AF, SPEI_SOC_HISTORICAL_SEN, SSMI_SOC_HISTORICAL_SEN, STI_SOC_HISTORICAL_SEN,
                           SPEI_SOC_SSP585_SEN, SSMI_SOC_SSP585_SEN, STI_SOC_SSP585_SEN, LANDCOVER_CHANGE, landmask)
    ax_map.text(-0.12, 1.05, '(e)', fontweight="bold",
                transform=ax.transAxes, fontsize=22, va="top", ha="left",
                bbox=dict(facecolor="white", alpha=0.8, edgecolor="none"))
    return None


def plot_figures23f(fig, ax):
    ssp = 'ssp245'
    var = 'rh'
    ax_map, ax_db, ax_hm = _add_three_axes_below(fig, ax)
    SPEI_SOC_HISTORICAL_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/SPEI/NORMALIZE_historical_Max_sensitivity_{var}&SPEI120.nc")['max_correlation']
    SSMI_SOC_HISTORICAL_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/SSMI/NORMALIZE_historical_Max_sensitivity_{var}&SSMI120.nc")['max_correlation']
    STI_SOC_HISTORICAL_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/STI/NORMALIZE_historical_Max_sensitivity_{var}&STI120.nc")['max_correlation']
    SPEI_SOC_SSP585_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/SPEI/NORMALIZE_{ssp}_Max_sensitivity_{var}&SPEI120.nc")['max_correlation']
    SSMI_SOC_SSP585_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/SSMI/NORMALIZE_{ssp}_Max_sensitivity_{var}&SSMI120.nc")['max_correlation']
    STI_SOC_SSP585_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/STI/NORMALIZE_{ssp}_Max_sensitivity_{var}&STI120.nc")['max_correlation']
    SE_CHN = [21.0, 34.0, 99.4, 123.1]
    ADJUSTED_REGION = [20.77, 34.23, 98.79273550596503, 123.70726449403497]
    SPEI_clip = SPEI_SOC_SSP585_SEN.sel(lat=slice(SE_CHN[0], SE_CHN[1]), lon=slice(SE_CHN[2], SE_CHN[3])).where(landmask == 1).__abs__()
    SSMI_clip = SSMI_SOC_SSP585_SEN.sel(lat=slice(SE_CHN[0], SE_CHN[1]), lon=slice(SE_CHN[2], SE_CHN[3])).where(landmask == 1).__abs__()
    STI_clip = STI_SOC_SSP585_SEN.sel(lat=slice(SE_CHN[0], SE_CHN[1]), lon=slice(SE_CHN[2], SE_CHN[3])).where(landmask == 1).__abs__()
    combined = xr.concat([SPEI_clip, SSMI_clip, STI_clip], dim='variable')
    all_nan_mask = np.isnan(SPEI_clip) & np.isnan(SSMI_clip) & np.isnan(STI_clip)
    max_idx = combined.fillna(-9999).argmax(dim='variable')
    max_idx = xr.where(all_nan_mask, 3, max_idx)
    cmap = mcolors.ListedColormap(['#fca525', '#27c5cd', '#eb4116', 'white'])
    norm = mcolors.BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], cmap.N)
    ax_map.set_extent([ADJUSTED_REGION[2], ADJUSTED_REGION[3], ADJUSTED_REGION[0], ADJUSTED_REGION[1]], crs=ccrs.PlateCarree())
    ax_map.add_feature(cfeature.LAND, facecolor="white", edgecolor="black", linewidth=0.5)
    ax_map.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax_map.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.5)
    ax_map.add_patch(mpatches.Rectangle((SE_CHN[2], SE_CHN[0]), SE_CHN[3]-SE_CHN[2], SE_CHN[1]-SE_CHN[0],
                                        fill=False, lw=1.0, ls='--', color='k', transform=ccrs.PlateCarree(), zorder=10))
    ax_map.pcolormesh(max_idx.lon, max_idx.lat, max_idx, cmap=cmap, norm=norm,
                      transform=ccrs.PlateCarree(), shading='auto')
    ax_map.set_title('Dominant Factor in SE-CHN Region', fontsize=16, loc='center', pad=2)
    _plot_region_dumbbell(ax_db, SE_CHN, SPEI_SOC_HISTORICAL_SEN, SSMI_SOC_HISTORICAL_SEN, STI_SOC_HISTORICAL_SEN,
                          SPEI_SOC_SSP585_SEN, SSMI_SOC_SSP585_SEN, STI_SOC_SSP585_SEN, landmask)
    _plot_region_microheat(ax_hm, SE_CHN, SPEI_SOC_HISTORICAL_SEN, SSMI_SOC_HISTORICAL_SEN, STI_SOC_HISTORICAL_SEN,
                           SPEI_SOC_SSP585_SEN, SSMI_SOC_SSP585_SEN, STI_SOC_SSP585_SEN, LANDCOVER_CHANGE, landmask)
    ax_map.text(-0.12, 1.05, '(f)', fontweight="bold",
                transform=ax.transAxes, fontsize=22, va="top", ha="left",
                bbox=dict(facecolor="white", alpha=0.8, edgecolor="none"))
    return None


def plot_figures23g(fig, ax):
    ssp = 'ssp245'
    var = 'rh'
    ax_map, ax_db, ax_hm = _add_three_axes_below(fig, ax)
    SPEI_SOC_HISTORICAL_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/SPEI/NORMALIZE_historical_Max_sensitivity_{var}&SPEI120.nc")['max_correlation']
    SSMI_SOC_HISTORICAL_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/SSMI/NORMALIZE_historical_Max_sensitivity_{var}&SSMI120.nc")['max_correlation']
    STI_SOC_HISTORICAL_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/STI/NORMALIZE_historical_Max_sensitivity_{var}&STI120.nc")['max_correlation']
    SPEI_SOC_SSP585_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/SPEI/NORMALIZE_{ssp}_Max_sensitivity_{var}&SPEI120.nc")['max_correlation']
    SSMI_SOC_SSP585_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/SSMI/NORMALIZE_{ssp}_Max_sensitivity_{var}&SSMI120.nc")['max_correlation']
    STI_SOC_SSP585_SEN = xr.open_dataset(f"/run/media/yue/Elements SE/009_PreSeasonN_data_CMIP6/{var}/STI/NORMALIZE_{ssp}_Max_sensitivity_{var}&STI120.nc")['max_correlation']
    AUS = [-38.8, -10.2, 114.1, 154.5]
    ADJUSTED_REGION = [-39.086, -9.914000000000001, 107.5852335527101, 161.01476644728993]
    SPEI_clip = SPEI_SOC_SSP585_SEN.sel(lat=slice(AUS[0], AUS[1]), lon=slice(AUS[2], AUS[3])).where(landmask == 1).__abs__()
    SSMI_clip = SSMI_SOC_SSP585_SEN.sel(lat=slice(AUS[0], AUS[1]), lon=slice(AUS[2], AUS[3])).where(landmask == 1).__abs__()
    STI_clip = STI_SOC_SSP585_SEN.sel(lat=slice(AUS[0], AUS[1]), lon=slice(AUS[2], AUS[3])).where(landmask == 1).__abs__()
    combined = xr.concat([SPEI_clip, SSMI_clip, STI_clip], dim='variable')
    all_nan_mask = np.isnan(SPEI_clip) & np.isnan(SSMI_clip) & np.isnan(STI_clip)
    max_idx = combined.fillna(-9999).argmax(dim='variable')
    max_idx = xr.where(all_nan_mask, 3, max_idx)
    cmap = mcolors.ListedColormap(['#fca525', '#27c5cd', '#eb4116', 'white'])
    norm = mcolors.BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], cmap.N)
    ax_map.set_extent([ADJUSTED_REGION[2], ADJUSTED_REGION[3], ADJUSTED_REGION[0], ADJUSTED_REGION[1]], crs=ccrs.PlateCarree())
    ax_map.add_feature(cfeature.LAND, facecolor="white", edgecolor="black", linewidth=0.5)
    ax_map.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax_map.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.5)
    ax_map.add_patch(mpatches.Rectangle((AUS[2], AUS[0]), AUS[3]-AUS[2], AUS[1]-AUS[0],
                                        fill=False, lw=1.0, ls='--', color='k', transform=ccrs.PlateCarree(), zorder=10))
    ax_map.pcolormesh(max_idx.lon, max_idx.lat, max_idx, cmap=cmap, norm=norm,
                      transform=ccrs.PlateCarree(), shading='auto')
    ax_map.set_title('Dominant Factor in AUS Region', fontsize=16, loc='center', pad=2)
    _plot_region_dumbbell(ax_db, AUS, SPEI_SOC_HISTORICAL_SEN, SSMI_SOC_HISTORICAL_SEN, STI_SOC_HISTORICAL_SEN,
                          SPEI_SOC_SSP585_SEN, SSMI_SOC_SSP585_SEN, STI_SOC_SSP585_SEN, landmask)
    _plot_region_microheat(ax_hm, AUS, SPEI_SOC_HISTORICAL_SEN, SSMI_SOC_HISTORICAL_SEN, STI_SOC_HISTORICAL_SEN,
                           SPEI_SOC_SSP585_SEN, SSMI_SOC_SSP585_SEN, STI_SOC_SSP585_SEN, LANDCOVER_CHANGE, landmask)
    ax_map.text(-0.12, 1.05, '(g)', fontweight="bold",
                transform=ax.transAxes, fontsize=22, va="top", ha="left",
                bbox=dict(facecolor="white", alpha=0.8, edgecolor="none"))
    return None


def create_figures23():
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams['axes.edgecolor'] = 'black'
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Arial'],
        'font.sans-serif': ['Times New Roman'],
    })
    fig = plt.figure(figsize=(16, 20))
    gs = gridspec.GridSpec(3, 3, figure=fig, height_ratios=[4, 3, 3], wspace=0.15, hspace=0.1, top=0.95, bottom=0.07, left=0.1, right=0.99)
    ax1 = fig.add_subplot(gs[0, :])
    plot_figures23a(fig, ax1)
    ax2 = fig.add_subplot(gs[3], projection=ccrs.PlateCarree())
    plot_figures23b(fig, ax2)
    ax3 = fig.add_subplot(gs[4], projection=ccrs.PlateCarree())
    plot_figures23c(fig, ax3)
    ax4 = fig.add_subplot(gs[5], projection=ccrs.PlateCarree())
    plot_figures23d(fig, ax4)
    ax5 = fig.add_subplot(gs[6], projection=ccrs.PlateCarree())
    plot_figures23e(fig, ax5)
    ax6 = fig.add_subplot(gs[7], projection=ccrs.PlateCarree())
    plot_figures23f(fig, ax6)
    ax7 = fig.add_subplot(gs[8], projection=ccrs.PlateCarree())
    plot_figures23g(fig, ax7)
    fig.canvas.draw()
    png_path = os.path.join(OUTPUT_DIR, "FigureS23.png")
    fig.savefig(png_path, dpi=600, bbox_inches='tight')
    pdf_path = os.path.join(OUTPUT_DIR, "FigureS23.pdf")
    fig.savefig(pdf_path, dpi=600, bbox_inches='tight')
    print(f"Figure saved to: {pdf_path}")
    plt.close()


if __name__ == '__main__':
    create_figures23()
