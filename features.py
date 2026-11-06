"""Data cleaning and feature engineering shared by train.py and predict.py.

The logic matches sections 2 and 4 of notebook.ipynb, so the web service
prepares a company's data exactly as the model saw it during training.
"""
import numpy as np
import pandas as pd

NUMERICAL = ['log_netsales_24', 'log_emp', 'log_capex_24', 'profit_margin', 'age', 'year']
CATEGORICAL = ['sector', 'country']


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the cleaning rules from section 2 of the notebook."""
    # Keep only rows with a positive R&D figure (this also drops missing values)
    df = df[df['rnd_24'] > 0].copy()

    # Negative sales and capex, and zero employees, aren't possible: treat them as missing
    for col in ['netsales_24', 'capex_24']:
        df.loc[df[col] < 0, col] = np.nan
    df.loc[df['emp'] == 0, 'emp'] = np.nan

    # Drop rows where R&D per employee is implausible (over €5m per head)
    rnd_per_emp = df['rnd_24'] / df['emp']
    return df[~(rnd_per_emp > 5)]


def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """Turn raw company data into model features (section 4 of the notebook)."""
    X = pd.DataFrame(index=df.index)
    for col in ['netsales_24', 'emp', 'capex_24']:
        X['log_' + col] = np.log1p(df[col])
    X['profit_margin'] = (df['profit_24'] / df['netsales_24']).clip(-1, 1)
    X['age'] = (df['year'] - df['year_inc_new']).clip(lower=0)
    X['year'] = df['year']
    X['sector'] = df['icb3_name']
    X['country'] = df['new_country']
    return X


def fill_missing(X: pd.DataFrame, medians: dict) -> pd.DataFrame:
    """Fill gaps with the training set's medians, and 'unknown' for categories."""
    X = X.copy()
    X[NUMERICAL] = X[NUMERICAL].fillna(medians)
    X[CATEGORICAL] = X[CATEGORICAL].fillna('unknown')
    return X
