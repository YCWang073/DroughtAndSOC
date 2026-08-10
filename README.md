# DroughtAndSOC

> 面向 EIAR 论文的主图与补充图绘图仓库：使用整理后的 Python 脚本重绘 SOC、异养呼吸（Rh）及干旱敏感性分析结果，并归档当前 PNG/PDF 成果。
>
> A plotting repository for the main and supplementary figures of the EIAR paper. It contains reorganized Python scripts for SOC, heterotrophic respiration (Rh), and drought-sensitivity analyses, together with the current PNG/PDF figure outputs.

本仓库适合需要查看论文图件、复核绘图逻辑，或在已有 ERA5/CMIP6 派生结果基础上重新生成图件的研究者。仓库只负责绘图和结果归档。

This repository is intended for researchers who need to inspect the manuscript figures, review the plotting logic, or regenerate figures from prepared ERA5/CMIP6-derived results. It focuses on plotting and result archiving.

项目地址 / Project: [github.com/YCWang073/DroughtAndSOC](https://github.com/YCWang073/DroughtAndSOC)

## 仓库内容 / Repository Contents

当前整理后的绘图版本包括：

The reorganized plotting version contains:

- `src/plot_v2/`：35 个独立 Python 绘图脚本，取代原先的 Jupyter notebook。
- `src/plot_v2/`: 35 standalone Python plotting scripts replacing the former Jupyter notebooks.
- `res/eiar_figs/`：77 个已生成图件，包括 Figure 1、Figure 2–8 以及 Figure S1–S31 的 PNG/PDF 结果。
- `res/eiar_figs/`: 77 generated figures, including Figure 1, Figures 2–8, and Figures S1–S31 in PNG/PDF format.
- `README.md`：项目说明、图件映射、运行方式和质量检查。
- `README.md`: project description, figure mapping, execution instructions, and quality checks.

Figure 1 当前只有已归档的 `Figure1.png`，`src/plot_v2/` 中没有对应的 `plot_figure1.py`。其余图件通常同时提供 PNG 和 PDF；S27–S31 的脚本在重新运行时还会额外生成 SVG。

Figure 1 is currently archived only as `Figure1.png`; there is no corresponding `plot_figure1.py` in `src/plot_v2/`. The other figures generally have both PNG and PDF versions. When rerun, the S27–S31 scripts additionally generate SVG files.

## 图件与脚本对应关系 / Figure–Script Mapping

### 主图 / Main Figures

| 图件 / Figure | 绘图脚本 / Script | 内容概览 / Description |
|---|---|---|
| Figure 1 | — | 研究框架图；本仓库只保存结果图。<br>Study framework; only the generated figure is archived here. |
| Figure 2 | `plot_figure2.py` | ERA5 与 CMIP6 的降水、地表温度、蒸发和土壤水分校正结果对比。<br>Comparison of ERA5 and CMIP6 bias-corrected precipitation, surface temperature, evaporation, and soil moisture. |
| Figure 3 | `plot_figure3.py` | 各大洲模型 skill weight、independence weight 及模型权重信息。<br>Continental model skill weights, independence weights, and model-weight information. |
| Figure 4 | `plot_figure4.py` | 1901–2100 年 SOC 与 Rh 全球变化、空间分布、情景差异及纬向统计。<br>Global SOC and Rh changes from 1901–2100, spatial patterns, scenario differences, and zonal statistics. |
| Figure 5 | `plot_figure5.py` | SPEI/SSMI 干旱持续时间、连续变干趋势及未来变化。<br>SPEI/SSMI drought duration, continuous-drying trends, and future changes. |
| Figure 6 | `plot_figure6.py` | SOC/Rh 对 SPEI、SSMI、STI 的最大关联强度、响应时间尺度及其变化。<br>Maximum association strength, response timescales, and changes in SOC/Rh responses to SPEI, SSMI, and STI. |
| Figure 7 | `plot_figure7.py` | 六个重点区域的干旱敏感性结果及土地覆盖转移统计。<br>Drought-sensitivity results for six hotspot regions and land-cover transition statistics. |
| Figure 8 | `plot_figure8.py` | reviewer-ready SEM 效应、MMWM 与基准数据差异及 SOC 对比分析。<br>Reviewer-ready SEM effects, MMWM–benchmark differences, and SOC comparison analyses. |

### 补充图 / Supplementary Figures

| 图件 / Figure | 绘图脚本 / Script | 内容概览 / Description |
|---|---|---|
| Figure S1、S3 / Figures S1, S3 | `plot_figureS1_S3.py` | Rh 与 SOC 的洲际模型距离矩阵。<br>Continental model-distance matrices for Rh and SOC. |
| Figure S2、S4 / Figures S2, S4 | `plot_figureS2_S4.py` | 模型加权/等权集成及相关评估结果。<br>Weighted/equal-weighted model ensembles and related evaluation results. |
| Figure S5、S7 / Figures S5, S7 | `plot_figureS5_S7.py` | SOC/Rh 的观测—模型、情景和集成结果对比。<br>Observation–model, scenario, and ensemble comparisons for SOC/Rh. |
| Figure S6 | `plot_figureS6.py` | 扩展干旱与 SOC/Rh 分析面板。<br>Extended drought and SOC/Rh analysis panels. |
| Figure S8 | `plot_figureS8.py` | 扩展情景变化与区域分析面板。<br>Extended scenario-change and regional-analysis panels. |
| Figure S9 | `plot_figureS9.py` | 补充干旱持续时间及变化结果。<br>Supplementary drought-duration results and changes. |
| Figure S10–S12 | `plot_figureS10.py`–`plot_figureS12.py` | SOC/Rh 干旱敏感性空间和区域分析。<br>Spatial and regional analyses of SOC/Rh drought sensitivity. |
| Figure S13–S15 | `plot_figureS13.py`–`plot_figureS15.py` | 不同干旱指标下的敏感性变化。<br>Sensitivity changes under different drought indices. |
| Figure S16–S18 | `plot_figureS16.py`–`plot_figureS18.py` | 补充敏感性空间分布及情景对比。<br>Supplementary sensitivity patterns and scenario comparisons. |
| Figure S19–S25 | 对应编号的 `plot_figureS*.py` / corresponding `plot_figureS*.py` | 土地覆盖变化、敏感性变化及区域统计面板。<br>Land-cover changes, sensitivity changes, and regional-statistics panels. |
| Figure S26 | `plot_figureS26.py` | reviewer-ready Rh SEM 结果及 SOC→Rh/土壤水分效应。<br>Reviewer-ready Rh SEM results and SOC→Rh/soil-moisture effects. |
| Figure S27 | `plot_figureS27.py` | 带符号的 selected partial-Spearman 系数分布。<br>Distributions of signed selected partial-Spearman coefficients. |
| Figure S28 | `plot_figureS28.py` | 单模型、MMEM 和 MMWM 的 SOC/Rh 全球轨迹。<br>Global SOC/Rh trajectories for individual models, MMEM, and MMWM. |
| Figure S29 | `plot_figureS29.py` | SPEI、SSMI、STI 的 VIF 与 condition index 共线性诊断。<br>VIF and condition-index diagnostics for SPEI, SSMI, and STI. |
| Figure S30 | `plot_figureS30.py` | 单指标结果与 partial-map 结果的一致性。<br>Correspondence between single-index and partial-map results. |
| Figure S31 | `plot_figureS31.py` | 空间 block bootstrap 下不同干旱指标的成对差异。<br>Pairwise differences among drought indices based on spatial block bootstrap results. |

编号与输出文件名保持一致。例如，`plot_figureS23.py` 生成 `res/eiar_figs/FigureS23.png` 和 `res/eiar_figs/FigureS23.pdf`。

Figure numbers match the output filenames. For example, `plot_figureS23.py` generates `res/eiar_figs/FigureS23.png` and `res/eiar_figs/FigureS23.pdf`.

## 目录结构 / Directory Structure

```text
DroughtAndSOC/
├── README.md
├── src/
│   └── plot_v2/
│       ├── plot_figure2.py
│       ├── plot_figure3.py
│       ├── ...
│       └── plot_figureS31.py
└── res/
    └── eiar_figs/
        ├── Figure1.png
        ├── Figure2.png
        ├── Figure2.pdf
        └── ...
```

脚本按“一个图件一个入口”组织；`plot_figureS1_S3.py`、`plot_figureS2_S4.py` 和 `plot_figureS5_S7.py` 是少数一个脚本生成两个图件的例外。脚本内部仍保留用于绘制地图、统一色标、区域标注和统计汇总的辅助函数，但没有额外的公共 Python 包接口。

The scripts are organized as one entry point per figure. The exceptions are `plot_figureS1_S3.py`, `plot_figureS2_S4.py`, and `plot_figureS5_S7.py`, each of which generates two figures. The scripts retain helper functions for maps, unified color scales, regional labels, and statistical summaries, but do not expose an additional public Python package API.

## 运行方式 / Running the Scripts

### 运行单个图件 / Run an Individual Figure

```bash
cd /path/to/DroughtAndSOC
python src/plot_v2/plot_figure4.py
python src/plot_v2/plot_figureS1_S3.py
```

脚本通常会在 `res/eiar_figs/` 中创建或覆盖同名 PNG/PDF。执行前请确认本地输入数据、变量名、时间范围和网格坐标与脚本假设一致。

The scripts normally create or overwrite PNG/PDF files with matching names in `res/eiar_figs/`. Before running them, make sure that the local input data, variable names, time ranges, and grid coordinates match the assumptions in the scripts.

### 批量运行 / Run All Scripts

在所有输入准备完成后，可以按脚本顺序批量执行：

After all inputs have been prepared, the scripts can be executed in sequence:

```bash
cd /path/to/DroughtAndSOC
for script in src/plot_v2/plot_figure*.py; do
  python "$script"
done
```

批量运行会重新生成并覆盖已有结果，不建议在没有备份结果的情况下直接执行。若某个输入文件缺失，脚本会在对应位置报错；推荐先单独运行目标图件，确认路径和变量后再批量运行。

Batch execution regenerates and overwrites existing outputs, so it should not be run without backing up the archived figures. If an input file is missing, the corresponding script will fail; running the target figure individually first is recommended.

### S27–S31 的 CSV 参数 / CSV Arguments for S27–S31

这五个脚本支持显式指定输入文件和输出目录。例如：

These five scripts support explicit input-file and output-directory arguments. For example:

```bash
python src/plot_v2/plot_figureS28.py \
  --trajectory-csv /path/to/annual_model_trajectories.csv \
  --output-dir res/eiar_figs

python src/plot_v2/plot_figureS29.py \
  --diagnostics-csv /path/to/collinearity_diagnostics.csv \
  --output-dir res/eiar_figs

python src/plot_v2/plot_figureS30.py \
  --robustness-csv /path/to/single_vs_partial_summary.csv \
  --output-dir res/eiar_figs

python src/plot_v2/plot_figureS31.py \
  --bootstrap-csv /path/to/pairwise_selected_sensitivity_bootstrap.csv \
  --output-dir res/eiar_figs
```

`plot_figureS27.py` 使用 `--data-root` 指定 selected-sensitivity NetCDF 根目录；五个脚本均支持 `--output-dir`。可通过 `python src/plot_v2/<脚本名>.py --help` 查看参数。

`plot_figureS27.py` uses `--data-root` to specify the root directory of the selected-sensitivity NetCDF files. All five scripts support `--output-dir`. Use `python src/plot_v2/<script_name>.py --help` to inspect the available arguments.

## 结果格式与质量检查 / Output Format and Quality Checks

- 归档结果以 600 dpi 导出，PNG 适合快速查看，PDF 适合论文排版和矢量输出。
- Archived figures are exported at 600 dpi. PNG is convenient for inspection, while PDF is suitable for manuscript layout and vector output.
- 重新运行前应检查 `res/eiar_figs/` 中的文件数量、文件大小和修改时间，避免把失败或不完整的图件覆盖到归档结果中。
- Before rerunning a script, check the file count, file sizes, and modification times in `res/eiar_figs/` so that failed or incomplete figures do not replace the archived outputs.
- 代码语法检查可在不读取数据的情况下执行：
- Syntax can be checked without loading the data:

  ```bash
  python -m compileall -q src/plot_v2
  ```

- 真正的结果验证应至少检查图件是否完整、坐标范围和单位是否正确，以及输出中的时间段、情景和区域是否与输入数据一致。
- Result validation should at least confirm figure completeness, coordinate ranges, units, and consistency between the plotted periods, scenarios, regions, and the input data.
