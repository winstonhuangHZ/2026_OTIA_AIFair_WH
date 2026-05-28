# TransLuxPop / CivitasGrid-TLP: Consolidated Experiments

This directory contains the consolidated and cleaned-up version of all experiments originally spread across 7 notebooks in `notebooks/`.

## Structure

| File | Description |
|:-----|:------------|
| `consolidated_experiments.py` | **Main consolidated script** — all experiments in one clean, well-organized file |
| `consolidated_experiments.ipynb` | Jupyter notebook version of the above (exported) |

## What Changed

### 1. Consolidation
All 7 original notebooks have been merged into a single, unified codebase:

| Original Notebooks | Merged Into |
|:-------------------|:------------|
| `Baseline_vs_Contrastive.ipynb` | §5.1 Contrastive Learning (XGB + RF) |
| `Baseline_vs_ContrastiveLearning.ipynb` | §5.2 Contrastive Learning (weight-based RF) |
| `Baseline_vs_MoE.ipynb` | §6 Mixture of Experts |
| `Baseline_vs_MoE_gating_vis.ipynb` | §6 Mixture of Experts (with gating vis) |
| `MultiBaselines_CL .ipynb` | §7 Multi-Baselines (6 models, no XGB) |
| `MultiBaselines_CL_XGB.ipynb` | §7 Multi-Baselines (7 models incl. XGB) |
| `MultiBaselines_CL_weight_sweep_FIXED2.ipynb` | §8 Weight Sweep |

### 2. Cleanup
- **Chinese comments → English**: All comments and docstrings are now in English
- **Removed dead code**: Deprecated/spoof functions, unreachable branches, redundant imports
- **Standardized naming**: Consistent variable names, singular/plural conventions
- **DRY principle**: Shared utilities (splits, metrics, tail computation) defined once
- **Type hints**: Added/improved type annotations

### 3. Organization

```
§1. Imports & Setup
§2. Data Loading & Preprocessing
§3. Utility Functions (splits, metrics, tail computation)
§4. Contrastive Learning Losses & Utilities
§5. Baseline Models
   §5.1 XGBoost + RandomForest (with CL custom objective)
   §5.2 RandomForest with Weight-Based CL
§6. Mixture of Experts (Two-Expert MoE)
§7. Multi-Baselines with Affine Calibration
   §7.1 Affine Calibrator (CL / RMSE_CL)
   §7.2 Seven Baselines (XGB, Ridge, ElasticNet, SVR, RF, ET, MLP)
§8. Weight Sweep Experiment
§9. Results Compilation & Visualization
```

### 4. Code Quality
- All random seeds are set in one place (`SEED = 42`)
- Pipeline architecture is standardized across all experiments
- Evaluation metrics (All / Tail / Worst-case) are computed identically
- Temperature computation is unified
- Output paths are configurable

## Running

```bash
# Install dependencies
pip install pandas numpy scikit-learn xgboost matplotlib openpyxl

# Run the consolidated script
python consolidated_experiments.py
```

Or open `consolidated_experiments.ipynb` in Jupyter and run cell by cell.

## Outputs

Results are saved to the `consolidated/outputs/` directory:
- `results_tail_tables.xlsx` — Summary tables
- `results_contrastive.csv` — Contrastive learning results
- `results_multibaselines.csv` — Multi-baseline results
- `results_moe.csv` — MoE results
- `paper_figs_*/` — Figures organized by experiment
