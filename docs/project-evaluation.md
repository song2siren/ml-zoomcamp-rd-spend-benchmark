# Project Evaluation

Reference: the [evaluation criteria](https://github.com/DataTalksClub/machine-learning-zoomcamp/tree/main/projects#evaluation-criteria) of the [Machine Learning Zoomcamp](https://github.com/DataTalksClub/machine-learning-zoomcamp) midterm project (as of 30/10/2026).

Key: ✅ criterion fully met · 🟨 partly met · ⬜ not started

- ✅ Problem description
  - [ ] 0 points: Problem is not described
  - [ ] 1 point: Problem is described in README briefly without much details
  - [x] 2 points: Problem is described in README with enough context, so it's clear what the problem is and how the solution will be used

  **Evidence:** the [Problem description](../README.md#problem-description) in the README explains the R&D tax context, what the model predicts and how an adviser would use the results, and the [Limitations](../README.md#limitations-and-next-steps) section sets out what it should and shouldn't be used for.

- ✅ EDA
  - [ ] 0 points: No EDA
  - [ ] 1 point: Basic EDA (looking at min-max values, checking for missing values)
  - [x] 2 points: Extensive EDA (ranges of values, missing values, analysis of target variable, feature importance analysis)
    - For images: analysing the content of the images
    - For texts: frequent words, word clouds, etc

  **Evidence:** [`notebook.ipynb`](../notebook.ipynb) sections 2 and 3: missing values and value ranges, with data errors traced to their cause (section 2); target distribution and log transform (3.1); feature distributions (3.2); R&D intensity by sector (3.3); correlation and mutual information (3.4). Summarised in the README's [EDA section](../README.md#exploratory-data-analysis).

- ✅ Model training
  - [ ] 0 points: No model training
  - [ ] 1 point: Trained only one model, no parameter tuning
  - [ ] 2 points: Trained multiple models (linear and tree-based)
    - For neural networks: tried multiple variations - with dropout or without, with extra inner layers or without
  - [x] 3 points: Trained multiple models and tuned their parameters
    - For neural networks: same as previous, but also with tuning: adjusting learning rate, dropout rate, size of the inner layer, etc.

  **Evidence:** [`notebook.ipynb`](../notebook.ipynb) section 5: Ridge regression (tuned `alpha`), decision tree (`max_depth`, `min_samples_leaf`), random forest (`n_estimators`, `max_depth`, `min_samples_leaf`) and XGBoost (`eta`, number of rounds, `max_depth`, `min_child_weight`), compared in section 5.5 and evaluated on the test set in section 6. Results table in the README's [Model training section](../README.md#model-training).

- ✅ Exporting notebook to script
  - [ ] 0 points: No script for training a model
  - [x] 1 point: The logic for training the model is exported to a separate script

  **Evidence:** [`train.py`](../train.py) trains the final XGBoost model and saves `model.bin`, using the cleaning and feature code in [`features.py`](../features.py).

- ✅ Reproducibility
  - [ ] 0 points: Not possible to execute the notebook and the training script. Data is missing or it's not easily accessible
  - [x] 1 point: It's possible to re-execute the notebook and the training script without errors. The dataset is committed in the project repository or there are clear instructions on how to download the data

  **Evidence:** the dataset is committed at [`data/scoreboard_panel.csv`](../data/scoreboard_panel.csv), and [`prepare_data.py`](../prepare_data.py) rebuilds it from the original EU source. Tested from a fresh clone: the notebook runs without errors, and `train.py` reproduces the committed model exactly.

- ✅ Model deployment
  - [ ] 0 points: Model is not deployed
  - [x] 1 point: Model is deployed (with Flask, BentoML or a similar framework)

  **Evidence:** [`predict.py`](../predict.py) serves the model with FastAPI (`/predict`, `/options`, `/health`). See the README's [Use the web service](../README.md#use-the-web-service) section for example requests and responses.

- ✅ Dependency and environment management
  - [ ] 0 points: No dependency management
  - [ ] 1 point: Provided a file with dependencies (requirements.txt, pipfile, bentofile.yaml with dependencies, etc)
  - [x] 2 points: Provided a file with dependencies and used virtual environment. README says how to install the dependencies and how to activate the env

  **Evidence:** dependencies are managed with uv in [`pyproject.toml`](../pyproject.toml) and [`uv.lock`](../uv.lock). The README's [Set up the environment](../README.md#set-up-the-environment) section explains how to install them and how to activate the virtual environment.

- ✅ Containerization
  - [ ] 0 points: No containerization
  - [ ] 1 point: Dockerfile is provided or a tool that creates a docker image is used (e.g. BentoML)
  - [x] 2 points: The application is containerized and the README describes how to build a container and how to run it

  **Evidence:** [`Dockerfile`](../Dockerfile). The README's [Run the web service](../README.md#run-the-web-service) section gives the `docker build` and `docker run` commands.

- ✅ Cloud deployment (bonus)
  - [ ] 0 points: No deployment to the cloud
  - [ ] 1 point: Docs describe clearly (with code) how to deploy the service to cloud or kubernetes cluster (local or remote)
  - [x] 2 points: There's code for deployment to cloud or kubernetes cluster (local or remote). There's a URL for testing - or video/screenshot of testing it

  **Evidence:** deployed to Fly.io using [`fly.toml`](../fly.toml). The URL, a screenshot of a successful test and step-by-step deployment instructions are in the README's [Cloud deployment section](../README.md#cloud-deployment).

**Self-assessed total: 16 / 16**