"""Train the R&D spend model and save it to model.bin.

Usage:
    uv run python train.py

The steps match notebook.ipynb: clean the data, split by company
(60% train, 20% validation, 20% test), check the model on the validation
set, then retrain on train + validation and evaluate once on the test set.
"""
import pickle

import numpy as np
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from xgboost import XGBRegressor

from features import NUMERICAL, clean_data, fill_missing, prepare_features

DATA_PATH = 'data/scoreboard_panel.csv'
MODEL_PATH = 'model.bin'
MODEL_NAME = 'XGBoost (eta=0.1, max_depth=6, min_child_weight=1, 240 rounds)'
SEED = 1


def build_model():
    # Best settings from section 5.4 of the notebook
    xgb_model = XGBRegressor(
        n_estimators=240,
        learning_rate=0.1,
        max_depth=6,
        min_child_weight=1,
        objective='reg:squarederror',
        random_state=SEED,
    )
    return make_pipeline(DictVectorizer(sparse=False), xgb_model)


def rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred) ** 2))


def to_records(X):
    return X.to_dict(orient='records')


def main():
    print('Loading and cleaning data...')
    df = clean_data(pd.read_csv(DATA_PATH))

    # Split by company, so no company appears in more than one set
    companies = df['company'].unique()
    companies_full_train, companies_test = train_test_split(companies, test_size=0.2, random_state=SEED)
    companies_train, companies_val = train_test_split(companies_full_train, test_size=0.25, random_state=SEED)

    df_train = df[df['company'].isin(companies_train)]
    df_val = df[df['company'].isin(companies_val)]
    df_full_train = df[df['company'].isin(companies_full_train)]
    df_test = df[df['company'].isin(companies_test)]

    # 1. Validation check: train on the training set, score on the validation set
    X_train = prepare_features(df_train)
    medians = X_train[NUMERICAL].median().to_dict()
    model = build_model()
    model.fit(to_records(fill_missing(X_train, medians)), np.log1p(df_train['rnd_24']))
    X_val = fill_missing(prepare_features(df_val), medians)
    val_rmse = rmse(np.log1p(df_val['rnd_24']), model.predict(to_records(X_val)))
    print(f'Validation RMSE: {val_rmse:.3f} (typically off by a factor of {np.exp(val_rmse):.2f})')

    # 2. Final model: train on train + validation, score once on the test set
    X_full_train = prepare_features(df_full_train)
    medians = X_full_train[NUMERICAL].median().to_dict()
    model = build_model()
    model.fit(to_records(fill_missing(X_full_train, medians)), np.log1p(df_full_train['rnd_24']))
    X_test = fill_missing(prepare_features(df_test), medians)
    test_rmse = rmse(np.log1p(df_test['rnd_24']), model.predict(to_records(X_test)))
    print(f'Test RMSE:       {test_rmse:.3f} (typically off by a factor of {np.exp(test_rmse):.2f})')

    # Save everything predict.py needs
    bundle = {
        'model': model,
        'medians': medians,
        'model_name': MODEL_NAME,
        'test_rmse': float(test_rmse),
        'sectors': sorted(df['icb3_name'].dropna().unique()),
        'countries': sorted(df['new_country'].dropna().unique()),
    }
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(bundle, f)
    print(f'Saved model to {MODEL_PATH}')


if __name__ == '__main__':
    main()
