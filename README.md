# Expected R&D Spend Benchmark

Midterm project for the DataTalksClub [Machine Learning Zoomcamp 2026](https://github.com/DataTalksClub/machine-learning-zoomcamp).

> **Status:** work in progress. Sections marked _TODO_ are filled in as the project develops.

## Evaluation

The self-assessment against each of the course's evaluation criteria is in [docs/project-evaluation.md](docs/project-evaluation.md).

## Problem description

Companies in the UK can claim tax relief on qualifying research and development (R&D) spend. Advisers who prepare and review these claims, and HMRC when it checks them, often ask a simple sense-check question: **is this company's R&D figure in line with what we'd expect for a business of its size and type?**

Today that judgement is mostly based on experience. This project builds a model that answers it with data. Given a company's:

- size (net sales, employees, capital expenditure, market value)
- profitability (operating profit)
- sector and location
- age

the model predicts the R&D spend you'd **expect** for that profile. Comparing a company's actual R&D with the prediction shows whether it is typical, unusually high or unusually low, which flags figures worth a closer look.

The model is trained on the world's largest corporate R&D investors, so it is a proof of concept rather than a tool for small-company claims. The same approach could be applied to other company-level data.

_TODO: add a sentence or two on how you'd use this in practice._

## Dataset

The [EU Industrial R&D Investment Scoreboard](https://knowledge-for-policy.ec.europa.eu/publication/2025-eu-industrial-rd-investment-scoreboard-0_en), published annually by the European Commission's Joint Research Centre, ranks the companies investing most in R&D worldwide. This project uses the **2025 Scoreboard panel**, which tracks these companies from 2003 to 2024:

- about 97,000 company-year rows covering about 6,300 companies
- all money values converted to 2024 euros (€ million)

The original 41 MB spreadsheet has 57 columns. The project uses a trimmed copy with the 14 columns needed, committed at [`data/scoreboard_panel.csv`](data/scoreboard_panel.csv).

| Column | Meaning |
|---|---|
| `company`, `company_name` | Short and long company name |
| `year` | Financial year |
| `new_country`, `region_12_new` | Country and world region of headquarters |
| `icb3_short`, `icb3_name` | Sector: 11 broad groups and 39 detailed sectors |
| `rnd_24` | **Target:** R&D investment (€m) |
| `netsales_24`, `capex_24`, `profit_24`, `mcap_24` | Net sales, capital expenditure, operating profit, market capitalisation (€m) |
| `emp` | Number of employees |
| `year_inc_new` | Year of incorporation |

The ranking columns in the original file are left out on purpose. They are calculated from R&D spend, so using them as features would leak the answer into the model.

To rebuild the CSV from the original source:

```bash
uv run python prepare_data.py
```

If the download fails, download the "2025 Scoreboard Panel" file manually from the page linked above and run `uv run python prepare_data.py path/to/file.xlsx`.

## Exploratory data analysis

_TODO: key findings from [`notebook.ipynb`](notebook.ipynb)._

## Model training

_TODO: validation approach, models tried, tuning and results table._

## Running the project

### Requirements

- Python 3.11
- [uv](https://docs.astral.sh/uv/) for dependency and virtual environment management
- Docker (for the web service)

### Set up the environment

```bash
pip install uv          # if uv isn't installed already
uv sync                 # creates .venv and installs the exact versions in uv.lock
```

Commands need to run inside the virtual environment (`.venv`). There are two equivalent ways to do this.

**Option 1:** prefix each command with `uv run`:

```bash
uv run jupyter notebook
```

**Option 2:** activate the environment once per terminal session, then run commands as normal:

```bash
source .venv/bin/activate
jupyter notebook
```

When the environment is active, the terminal prompt starts with `(rd-spend-benchmark)`. Run `deactivate` to leave it.

If you're using GitHub Codespaces, VS Code forwards Jupyter's port 8888 automatically: open it from the **Ports** panel.

### Train the model

```bash
uv run python train.py
```

This cleans the data, splits it by company, reports the validation and test scores, and saves the trained model to `model.bin`. The cleaning and feature engineering code is shared with the web service in `features.py`. A trained `model.bin` is already committed, so this step is optional.

### Run the web service

The model is served with [FastAPI](https://fastapi.tiangolo.com/) on port 9696.

**With Docker (recommended):**

```bash
docker build -t rd-spend-benchmark .
docker run -it --rm -p 9696:9696 rd-spend-benchmark
```

**Without Docker:**

```bash
uv run uvicorn predict:app --host 0.0.0.0 --port 9696
```

### Use the web service

With the service running, send an example request from a second terminal:

```bash
uv run python test_predict.py
```

or with `curl`:

```bash
curl -X POST http://localhost:9696/predict \
  -H "Content-Type: application/json" \
  -d '{"net_sales": 250, "employees": 1200, "capex": 15, "operating_profit": 20,
       "year": 2024, "year_incorporated": 1998,
       "sector": "Software & Computer Services", "country": "UK",
       "reported_rnd": 30}'
```

Example response:

```json
{
  "expected_rnd": 43.63,
  "typical_range": [17.18, 110.8],
  "units": "€ million",
  "reported_rnd": 30.0,
  "reported_vs_expected": 0.69,
  "assessment": "typical"
}
```

| Field | Meaning |
|---|---|
| `expected_rnd` | The model's estimate of R&D spend for a company with this profile (€m) |
| `typical_range` | The range within which predictions are typically accurate (expected ÷ and × the model's typical error factor from the test set) |
| `reported_vs_expected` | Reported R&D divided by expected R&D (only if `reported_rnd` is given) |
| `assessment` | `typical` if the reported figure is within the typical range, otherwise `unusually high` or `unusually low` |

All money values are in € million. Only `year`, `sector` and `country` are required; missing figures are filled with typical values from the training data. Valid sectors and countries are listed at `GET /options`, and `GET /health` confirms the service is running. FastAPI also provides interactive documentation at http://localhost:9696/docs.

## Cloud deployment

_TODO (optional, bonus points)._

## Acknowledgements

Data: European Commission, Joint Research Centre, EU Industrial R&D Investment Scoreboard 2025.

Thanks to [DataTalksClub](https://github.com/DataTalksClub) and Alexey Grigorev for the Machine Learning Zoomcamp.
