"""
TransLuxPop / CivitasGrid-TLP: Consolidated Experiments
=======================================================

This file consolidates all experiments from 7 original notebooks into one
well-organized, clean codebase. All comments are in English, and shared
utilities are defined once and reused across all experiments.

Experiments included:
  1. Baseline Models (XGBoost, RandomForest) with Contrastive Learning objectives
  2. Weight-Based Contrastive Learning for RandomForest
  3. Mixture of Experts (Two-Expert MoE with Gating)
  4. Multi-Baselines with Affine Calibration (7 baselines × 3 variants each)
  5. Mix-Weight Sweep (RMSE vs CL weight exploration)

Author: Consolidated from 7 original notebooks
"""

# consolidated_experiments.py — Single unified script combining all 7 original notebooks
# Usage: python consolidated_experiments.py    (requires grids_set_4_HQ.xlsx in CWD)

import os, re, sys, time, random, warnings
from dataclasses import dataclass
from typing import Dict, Tuple, Optional, List, Callable

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from IPython.display import display

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split, GroupShuffleSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import Ridge, ElasticNet
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.neural_network import MLPRegressor

import sklearn, xgboost
warnings.filterwarnings('ignore')

SEED = 42
random.seed(SEED); np.random.seed(SEED); os.environ['PYTHONHASHSEED'] = str(SEED)
print(f'pandas={pd.__version__} numpy={np.__version__} '
      f'sklearn={sklearn.__version__} xgboost={xgboost.__version__}')

CL_BATCH_SIZE = 128
CL_EPOCHS = 40
CL_LR = 0.05
CL_TEMP_FACTOR = 1.0
CL_EPS = 1e-12

OUTDIR = 'outputs'; os.makedirs(OUTDIR, exist_ok=True)
FIGDIR = os.path.join(OUTDIR, 'figures'); os.makedirs(FIGDIR, exist_ok=True)

def safe_filename(s: str) -> str:
    """Convert a string to a safe filename by replacing problematic characters."""
    return re.sub(r"[^a-zA-Z0-9._-]+", "_", s)

# =========================================================================
# §2  DATA LOADING & PREPROCESSING
# =========================================================================

DATA_PATH = 'grids_set_4_HQ.xlsx'

def load_data(data_path: str = DATA_PATH) -> pd.DataFrame:
    """
    Load the CivitasGrid-TLP / TransLuxPop dataset.
    
    Checks multiple possible paths for flexibility.
    """
    paths_to_check = [
        data_path,
        '/mnt/data/grids_set_4_HQ.xlsx',
    ]
    
    resolved_path = None
    for p in paths_to_check:
        if os.path.exists(p):
            resolved_path = p
            break
    
    if resolved_path is None:
        raise FileNotFoundError(
            f'Data file not found. Checked: {paths_to_check}'
        )
    
    df = pd.read_excel(resolved_path)
    df.columns = df.columns.str.strip()
    return df


def preprocess_data(df: pd.DataFrame, jitter: bool = True) -> pd.DataFrame:
    """
    Preprocess the dataset: add COVID intensity features, apply tiny jitter.
    
    Parameters
    ----------
    df : pd.DataFrame
        Raw data
    jitter : bool
        If True, add tiny uniform noise to _use features and last_year targets
        to prevent unstable splits in tree-based models.
    
    Returns
    -------
    pd.DataFrame with additional features
    """
    # COVID intensity map (rule-based, no missing values)
    covid_map = {
        2015: 0.0, 2016: 0.0, 2017: 0.0, 2018: 0.0,
        2019: 0.05, 2020: 0.8, 2021: 1.0, 2022: 0.6,
        2023: 0.4, 2024: 0.2,
    }
    
    # Drop rows with missing year (cannot construct covid_intensity)
    df = df.dropna(subset=['year']).copy()
    df['year'] = df['year'].astype(int)
    df['covid_intensity'] = df['year'].map(covid_map).fillna(0.0)
    
    # Tiny jitter for tree model stability
    if jitter:
        use_cols = [c for c in df.columns if c.endswith('_use')] + \
                   ["VIIRS_last_year", "WorldPop_last_year"]
        use_cols = [c for c in use_cols if c in df.columns]
        if use_cols:
            jitter_values = np.random.uniform(-0.01, 0.01, size=(len(df), len(use_cols)))
            df[use_cols] = df[use_cols].values + jitter_values
            print(f'Applied tiny jitter to {len(use_cols)} feature(s)')
    
    return df


# -------------------------------------------------------------------------
# Feature / target column definitions
# -------------------------------------------------------------------------
NUMERIC_COLS = [
    'mot_use', 'tru_use', 'pri_use', 'sec_use', 'ter_use', 'urb_use',
    'VIIRS_last_year', 'WorldPop_last_year', 'covid_intensity'
]

CATEGORICAL_COLS = ['region_type', 'city_type']

FEATURE_COLS = NUMERIC_COLS + CATEGORICAL_COLS

TARGET_COLS = ['dVIIRS', 'dWorldPop']


def build_preprocessor(
    numeric_features: List[str] = None,
    categorical_features: List[str] = None
) -> ColumnTransformer:
    """
    Build a ColumnTransformer with:
    - Numerical: median imputation + StandardScaler
    - Categorical: 'Unknown' imputation + OneHotEncoder
    """
    if numeric_features is None:
        numeric_features = NUMERIC_COLS
    if categorical_features is None:
        categorical_features = CATEGORICAL_COLS
    
    # Handle sklearn API change for sparse_output parameter
    try:
        ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    except TypeError:
        ohe = OneHotEncoder(handle_unknown='ignore', sparse=False)
    
    numeric_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    categorical_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='Unknown')),
        ('onehot', ohe)
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_pipeline, numeric_features),
            ('cat', categorical_pipeline, categorical_features)
        ],
        remainder='drop',
        verbose_feature_names_out=False
    )
    return preprocessor


# Load and preprocess data
print(f'\nLoading data from {DATA_PATH}...')
df_raw = load_data(DATA_PATH)
print(f'  Shape: {df_raw.shape}')
print(f'  Columns: grid_id={{{"grid_id" in df_raw.columns}}, year={{{"year" in df_raw.columns}}}')
print(f'  Targets: dVIIRS={{{"dVIIRS" in df_raw.columns}}, dWorldPop={{{"dWorldPop" in df_raw.columns}}}')

df = preprocess_data(df_raw)
display(df.head(3))

# Validate required columns
required_cols = FEATURE_COLS + TARGET_COLS + ['grid_id', 'year']
missing_cols = [c for c in required_cols if c not in df.columns]
assert len(missing_cols) == 0, f'Missing columns: {missing_cols}'

print(f'\nFeature columns ({len(FEATURE_COLS)}): {FEATURE_COLS}')
print(f'Target columns ({len(TARGET_COLS)}): {TARGET_COLS}')
print(f'Unique region_type: {df["region_type"].nunique()}, city_type: {df["city_type"].nunique()}')

# Missing data summary
missing_summary = df[FEATURE_COLS + TARGET_COLS].isna().mean().sort_values(ascending=False)
print(f'\nMissing data (top features):')
display(missing_summary.to_frame('missing_ratio').head(12))

# Build the preprocessor (shared across all experiments)
preprocessor = build_preprocessor()
