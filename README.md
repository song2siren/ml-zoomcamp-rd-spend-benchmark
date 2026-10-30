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

Run any command inside the environment with `uv run`, for example:

```bash
uv run jupyter notebook notebook.ipynb
```

### Train the model

_TODO: `train.py`._

### Run the web service

_TODO: `predict.py`, Docker build and run, example request._

## Cloud deployment

_TODO (optional, bonus points)._

## Acknowledgements

Data: European Commission, Joint Research Centre, EU Industrial R&D Investment Scoreboard 2025.

Thanks to [DataTalksClub](https://github.com/DataTalksClub) and Alexey Grigorev for the Machine Learning Zoomcamp.
