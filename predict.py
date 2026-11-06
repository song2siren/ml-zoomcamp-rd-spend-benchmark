"""Web service that returns the expected R&D spend for a company.

Run locally:
    uv run uvicorn predict:app --host 0.0.0.0 --port 9696

Then open http://localhost:9696/docs to try it in the browser.
"""
import pickle

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from features import fill_missing, prepare_features

with open('model.bin', 'rb') as f:
    bundle = pickle.load(f)

model = bundle['model']
medians = bundle['medians']
# Predictions are typically off by this factor (from the test set).
# A reported figure outside expected ÷ factor to expected × factor is flagged as unusual.
TYPICAL_FACTOR = float(np.exp(bundle['test_rmse']))

app = FastAPI(title='Expected R&D Spend Benchmark')


class Company(BaseModel):
    net_sales: float | None = Field(None, description='Net sales, € million', examples=[250.0])
    employees: float | None = Field(None, description='Number of employees', examples=[1200])
    capex: float | None = Field(None, description='Capital expenditure, € million', examples=[15.0])
    operating_profit: float | None = Field(None, description='Operating profit (negative for a loss), € million', examples=[20.0])
    year: int = Field(..., description='Financial year', examples=[2024])
    year_incorporated: int | None = Field(None, description='Year the company was incorporated', examples=[1998])
    sector: str = Field(..., description='Sector name, as listed at /options', examples=['Software & Computer Services'])
    country: str = Field(..., description='Country, as listed at /options', examples=['UK'])
    reported_rnd: float | None = Field(None, description='Optional: the R&D spend to check, € million', examples=[30.0])


def to_raw(company: Company) -> pd.DataFrame:
    """Map the API field names to the dataset's column names."""
    raw = {
        'netsales_24': company.net_sales,
        'emp': company.employees,
        'capex_24': company.capex,
        'profit_24': company.operating_profit,
        'year': company.year,
        'year_inc_new': company.year_incorporated,
        'icb3_name': company.sector,
        'new_country': company.country,
    }
    df = pd.DataFrame([raw]).astype({'netsales_24': float, 'emp': float, 'capex_24': float,
                                    'profit_24': float, 'year_inc_new': float})
    # Same cleaning rules as training: impossible values are treated as missing
    for col in ['netsales_24', 'capex_24']:
        df.loc[df[col] < 0, col] = np.nan
    df.loc[df['emp'] == 0, 'emp'] = np.nan
    return df


@app.get('/health')
def health():
    return {'status': 'ok', 'model': bundle['model_name']}


@app.get('/options')
def options():
    return {'sectors': bundle['sectors'], 'countries': bundle['countries']}


@app.post('/predict')
def predict(company: Company):
    if company.sector not in bundle['sectors']:
        raise HTTPException(status_code=422, detail=f"Unknown sector '{company.sector}'. See /options for valid values.")
    if company.country not in bundle['countries']:
        raise HTTPException(status_code=422, detail=f"Unknown country '{company.country}'. See /options for valid values.")

    X = fill_missing(prepare_features(to_raw(company)), medians)
    expected = float(np.expm1(model.predict(X.to_dict(orient='records'))[0]))

    result = {
        'expected_rnd': round(expected, 2),
        'typical_range': [round(expected / TYPICAL_FACTOR, 2), round(expected * TYPICAL_FACTOR, 2)],
        'units': '€ million',
    }

    if company.reported_rnd is not None:
        ratio = company.reported_rnd / expected
        if ratio > TYPICAL_FACTOR:
            assessment = 'unusually high'
        elif ratio < 1 / TYPICAL_FACTOR:
            assessment = 'unusually low'
        else:
            assessment = 'typical'
        result['reported_rnd'] = company.reported_rnd
        result['reported_vs_expected'] = round(ratio, 2)
        result['assessment'] = assessment

    return result
