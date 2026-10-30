"""Download the EU Industrial R&D Investment Scoreboard panel and save a trimmed CSV.

The trimmed CSV is already committed in data/, so you only need this script
if you want to rebuild it from the original source.

Usage:
    uv run python prepare_data.py                      # download from the EU site
    uv run python prepare_data.py path/to/panel.xlsx   # use a file you downloaded yourself
"""
import sys
import urllib.request
from pathlib import Path

import pandas as pd

URL = ("https://knowledge-for-policy.ec.europa.eu/sites/default/files/"
       "2025%20Scoreboard%20Panel.xlsx")
SOURCE_PAGE = ("https://knowledge-for-policy.ec.europa.eu/publication/"
               "2025-eu-industrial-rd-investment-scoreboard-0_en")
DATA_DIR = Path(__file__).parent / "data"
XLSX_PATH = DATA_DIR / "2025_Scoreboard_Panel.xlsx"
CSV_PATH = DATA_DIR / "scoreboard_panel.csv"

# Columns kept for the project. Ranking columns are deliberately left out:
# they are calculated from R&D spend, so using them would leak the target.
COLUMNS = [
    "company", "company_name", "year", "new_country", "region_12_new",
    "icb3_short", "icb3_name",
    "rnd_24", "netsales_24", "emp", "capex_24", "profit_24", "mcap_24",
    "year_inc_new",
]


def main():
    DATA_DIR.mkdir(exist_ok=True)
    if len(sys.argv) > 1:
        xlsx = Path(sys.argv[1])
    else:
        xlsx = XLSX_PATH
        if not xlsx.exists():
            print(f"Downloading {URL} ...")
            try:
                urllib.request.urlretrieve(URL, xlsx)
            except Exception as e:
                sys.exit(f"Download failed ({e}).\nDownload the '2025 Scoreboard Panel' file "
                         f"manually from {SOURCE_PAGE}\nand run: "
                         f"uv run python prepare_data.py path/to/file.xlsx")

    print(f"Reading {xlsx} (this takes a minute or two)...")
    df = pd.read_excel(xlsx, sheet_name="data", usecols=COLUMNS)
    df[COLUMNS].to_csv(CSV_PATH, index=False)
    print(f"Saved {len(df):,} rows to {CSV_PATH}")


if __name__ == "__main__":
    main()
