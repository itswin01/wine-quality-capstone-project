# MLflow Experiment Tracking with DagsHub

## Overview

This module demonstrates **MLflow** experiment tracking for a **Wine Quality (red)**
regression task, with **DagsHub** used as the remote MLflow tracking server. The
workflow logs model parameters, evaluation metrics, and model artifacts for three
regressors (Linear Regression, Random Forest, XGBoost) so their performance can be
compared centrally. The **best-performing model is then registered in the MLflow Model
Registry** as `wine-quality-model`, which the FastAPI-Docker module later loads.

## Objectives

- Predict wine `quality` from 11 physicochemical measurements.
- Track machine learning experiments using MLflow.
- Log hyperparameters, evaluation metrics (MAE, RMSE, R²), models, and artifacts.
- Compare the three runs and register the best model in the MLflow Model Registry.
- Integrate MLflow with DagsHub for centralized experiment tracking and reproducibility.

## Repository Contents

| File | Description |
|------|-------------|
| `mlflow_dagshub.ipynb` | Main notebook implementing MLflow with DagsHub integration. |
| `winequality-red.csv` | Dataset used for model training and evaluation. |
| `requirements.txt` | Python dependencies. |

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

In the **DagsHub + MLflow Setup** cell of the notebook, set your DagsHub username and
repository name:

```python
dagshub.init(
    repo_owner="YOUR_DAGSHUB_USERNAME",
    repo_name="YOUR_REPO_NAME",
    mlflow=True,
)
```

Then run the notebook top to bottom. The runs, parameters, metrics, and artifacts will
appear on your DagsHub experiments page.

## Technologies Used

- Python
- Scikit-learn
- XGBoost
- MLflow
- DagsHub
- Pandas
- NumPy
