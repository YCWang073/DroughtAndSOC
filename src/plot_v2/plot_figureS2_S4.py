import os

import matplotlib.patches as patches
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import numpy as np
from matplotlib import gridspec
import matplotlib.lines as mlines
import geopandas as gpd

OUTPUT_DIR = "res/eiar_figs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

COMMON_MODEL = ['CMCC-ESM2', 'CESM2-WACCM', 'NorESM2-MM', 'TaiESM1',
                'EC-Earth3-Veg', 'CMCC-CM2-SR5', 'BCC-CSM2-MR']
OBSERVATION_INPUT_PATH = "/mnt/softwares/Drought_And_SOC/000_observasion_data_ERA5"
MODEL_INPUT_PATH = "/run/media/yue/Elements SE/007_CorrectAndRepair_data_CMIP6"
MMEM_INPUT_PATH = "/run/media/yue/Elements SE/007-1_MEM_data_CMIP6/raw"
MMWM_INPUT_PATH = "/run/media/yue/Elements SE/007-2_MMWM_data_CMIP6/raw"

MODEL_STYLES = {
    'MMEM': {'color': 'red', 'linewidth': 2, 'linestyle': '-', 'label': 'MMEM', 'zorder': 15},
    'MMWM': {'color': 'blue', 'linewidth': 2, 'linestyle': ':', 'label': 'MMWM', 'zorder': 20},
    'ERA5': {'color': 'black', 'linewidth': 3, 'linestyle': '--', 'label': 'BM', 'zorder': 10},
    'OTHER': {'color': 'gray', 'alpha': 0.5, 'linestyle': '-.', 'linewidth': 1.5, 'label': 'Other Models', 'zorder': 5}
}

CONTINENT_DICT = {
    'Asia': 0,
    'North America': 1,
    'Europe': 2,
    'Africa': 3,
    'South America': 4,
    'Oceania': 5
}


def plot_figureS2a(fig, ax, cal, continent):
    cal_MMEM = xr.open_dataset(f"{MMEM_INPUT_PATH}/{cal}_MMEM.nc")[f'ssp126_{cal}'].sel(time=slice('1985-01-01', '2014-12-31'))
    cal_MMWM = xr.open_dataset(f"{MMWM_INPUT_PATH}/{cal}_MMWM.nc")[f'ssp126_{cal}'].sel(time=slice('1985-01-01', '2014-12-31'))

    continent_index = CONTINENT_DICT[continent]
    shp_data = gpd.read_file(r"/mnt/softwares/Drought_And_SOC/001_shape_data_GIS/continent.shp")

    x_dim = 'lon'
    y_dim = 'lat'

    cal_MMEM.rio.set_spatial_dims(x_dim=x_dim, y_dim=y_dim, inplace=True)
    cal_MMWM.rio.set_spatial_dims(x_dim=x_dim, y_dim=y_dim, inplace=True)

    cal_MMEM.rio.write_crs(shp_data.crs, inplace=True)
    cal_MMWM.rio.write_crs(shp_data.crs, inplace=True)

    shp = shp_data.iloc[continent_index]['geometry']

    cal_MMEM = cal_MMEM.rio.clip([shp], shp_data.crs, drop=False)
    cal_MMWM = cal_MMWM.rio.clip([shp], shp_data.crs, drop=False)

    cal_MMEM = cal_MMEM.mean(dim=['lat', 'lon'])
    cal_MMWM = cal_MMWM.mean(dim=['lat', 'lon'])

    cal_model = {}
    for model in COMMON_MODEL:
        cal_tmp = xr.open_dataset(f"{MODEL_INPUT_PATH}/{model}/{model}_SeasonAndLand_corrected_{cal}.nc")[f'ssp126_{cal}'].sel(time=slice('1985-01-01', '2014-12-31'))
        if cal == 'rh':
            cal_tmp = cal_tmp * (60 * 60 * 24 * 365)
        cal_tmp.rio.set_spatial_dims(x_dim=x_dim, y_dim=y_dim, inplace=True)
        cal_tmp.rio.write_crs(shp_data.crs, inplace=True)
        cal_tmp = cal_tmp.rio.clip([shp], shp_data.crs, drop=False)
        cal_tmp = cal_tmp.mean(dim=['lat', 'lon'])
        cal_model[model] = cal_tmp

    print("绘制多模型集合和观测数据...")
    ax.plot(cal_MMEM.time, cal_MMEM.values, **MODEL_STYLES['MMEM'])
    ax.plot(cal_MMWM.time, cal_MMWM.values, **MODEL_STYLES['MMWM'])

    for model, data in cal_model.items():
        ax.plot(data.time, data.values, **MODEL_STYLES['OTHER'])

    if continent != 'Oceania':
        ax.set_title(f"{continent}", fontsize=20)
    else:
        ax.set_title(f"Australia", fontsize=20)

    YLABLE_TEXT = {
        'rh': "$R_h$ (kg C $m^{-2}$ $yr^{-1}$)",
        'soc': "$SOC$ (kg C $m^{-2}$)"
    }

    if continent == 'North America' or continent == 'Africa' or continent == 'Oceania':
        ax.set_ylabel("")
    else:
        ax.set_ylabel(YLABLE_TEXT[cal], fontsize=20)

    if continent == 'South America' or continent == 'Oceania':
        ax.set_xlabel('Year', fontsize=20)
    else:
        ax.set_xlabel("")

    ax.tick_params(axis='x', labelsize=16)
    ax.tick_params(axis='y', labelsize=16)


def create_figureS2():
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Arial'],
        'font.sans-serif': ['Times New Roman'],
    })

    fig = plt.figure(figsize=(15, 12))

    gs = gridspec.GridSpec(3, 2, figure=fig)
    for key, value in dict(CONTINENT_DICT).items():
        ax = fig.add_subplot(gs[value])
        plot_figureS2a(fig, ax, 'rh', key)

    handles = [
        mlines.Line2D([], [], **MODEL_STYLES['MMEM']),
        mlines.Line2D([], [], **MODEL_STYLES['MMWM']),
        mlines.Line2D([], [], **MODEL_STYLES['OTHER']),
        mlines.Line2D([], [], **MODEL_STYLES['OTHER']),
        mlines.Line2D([], [], **MODEL_STYLES['OTHER']),
        mlines.Line2D([], [], **MODEL_STYLES['OTHER']),
        mlines.Line2D([], [], **MODEL_STYLES['OTHER']),
        mlines.Line2D([], [], **MODEL_STYLES['OTHER']),
        mlines.Line2D([], [], **MODEL_STYLES['OTHER'])
    ]
    labels = ['Multi-model Ensemble Mean', 'Multi-model Weighted Mean',
              COMMON_MODEL[0], COMMON_MODEL[1], COMMON_MODEL[2], COMMON_MODEL[3],
              COMMON_MODEL[4], COMMON_MODEL[5], COMMON_MODEL[6]]
    fig.legend(handles, labels, loc='lower center', ncol=3, fontsize=20,
               frameon=True, bbox_to_anchor=(0.5, -0.07))

    plt.subplots_adjust(wspace=0.15, hspace=0.3)
    png_path = os.path.join(OUTPUT_DIR, "FigureS2.png")
    pdf_path = os.path.join(OUTPUT_DIR, "FigureS2.pdf")
    fig.savefig(png_path, dpi=600, bbox_inches='tight')
    fig.savefig(pdf_path, dpi=600, bbox_inches='tight')
    print(f"Figure saved to: {pdf_path}")

    plt.close()


def create_figureS4():
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Arial'],
        'font.sans-serif': ['Times New Roman'],
    })

    fig = plt.figure(figsize=(15, 12))

    gs = gridspec.GridSpec(3, 2, figure=fig)
    for key, value in dict(CONTINENT_DICT).items():
        ax = fig.add_subplot(gs[value])
        plot_figureS2a(fig, ax, 'soc', key)

    handles = [
        mlines.Line2D([], [], **MODEL_STYLES['MMEM']),
        mlines.Line2D([], [], **MODEL_STYLES['MMWM']),
        mlines.Line2D([], [], **MODEL_STYLES['OTHER']),
        mlines.Line2D([], [], **MODEL_STYLES['OTHER']),
        mlines.Line2D([], [], **MODEL_STYLES['OTHER']),
        mlines.Line2D([], [], **MODEL_STYLES['OTHER']),
        mlines.Line2D([], [], **MODEL_STYLES['OTHER']),
        mlines.Line2D([], [], **MODEL_STYLES['OTHER']),
        mlines.Line2D([], [], **MODEL_STYLES['OTHER'])
    ]
    labels = ['Multi-model Ensemble Mean', 'Multi-model Weighted Mean',
              COMMON_MODEL[0], COMMON_MODEL[1], COMMON_MODEL[2], COMMON_MODEL[3],
              COMMON_MODEL[4], COMMON_MODEL[5], COMMON_MODEL[6]]
    fig.legend(handles, labels, loc='lower center', ncol=3, fontsize=20,
               frameon=True, bbox_to_anchor=(0.5, -0.07))

    plt.subplots_adjust(wspace=0.15, hspace=0.3)
    png_path = os.path.join(OUTPUT_DIR, "FigureS4.png")
    pdf_path = os.path.join(OUTPUT_DIR, "FigureS4.pdf")
    fig.savefig(png_path, dpi=600, bbox_inches='tight')
    fig.savefig(pdf_path, dpi=600, bbox_inches='tight')
    print(f"Figure saved to: {pdf_path}")

    plt.close()


if __name__ == '__main__':
    create_figureS2()
    create_figureS4()
