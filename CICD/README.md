# CI/CD Pipeline for Wine Quality Regression using GitHub Actions

## Overview

This module provides the **GitHub Actions CI/CD workflow** for the project. On every push
or pull request to `main`, it checks out the repository, sets up Python, installs
dependencies, runs tests, runs the training pipeline (with an R² quality gate), deploys
the trained model to **Hugging Face Hub**, and builds the FastAPI Docker image. A
successful run is visible in the repository's **Actions** tab.

> The *best* model is also registered in the **MLflow Model Registry** by the `MLFlow`
> module. Hugging Face here is an additional deployment target.

---

## CI/CD Pipeline

```
Push / PR to main
      │
      ▼
Run tests (pytest)
      │
      ├────────────────────────────┐
      ▼                            ▼
Prepare → Train → Evaluate     Build FastAPI
(R² quality gate)              Docker image
      │
      ▼
Deploy to Hugging Face Hub
(push to main only)
```

The workflow file lives at the **repository root**: `.github/workflows/ci-cd.yaml`.

---

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── ci-cd.yaml          # lives at the repository root
├── CICD/
│   ├── src/
│   │   ├── prepare.py
│   │   ├── train.py
│   │   ├── evaluate.py
│   │   └── register.py         # pushes model to Hugging Face Hub
│   ├── tests/
│   │   └── test_pipeline.py
│   ├── winequality-red.csv
│   ├── params.yaml
│   ├── requirements.txt
│   └── README.md
```

---

## Pipeline Stages

### 1. Data Preparation (`prepare.py`)
- Loads the Wine Quality (red) dataset and splits it into train/test sets.

### 2. Model Training (`train.py`)
- Trains a Random Forest Regressor and saves the model and feature metadata.

### 3. Model Evaluation (`evaluate.py`)
- Evaluates using MAE, RMSE, R². Exits non-zero if R² is below the `min_r2` gate in
  `params.yaml`, so a poor model fails the pipeline before deployment.

### 4. Model Registration (`register.py`)
- After the quality gate passes, uploads the model, feature metadata, and a model card to
  Hugging Face Hub.

---

## Required Secrets / Variables

Add these in **Settings → Secrets and variables → Actions**:

**Repository secrets**
- `HF_TOKEN` — Hugging Face access token (write).
- `MLFLOW_TRACKING_URI` — e.g. `https://dagshub.com/<user>/<repo>.mlflow` (used by the Docker build).
- `MLFLOW_TRACKING_USERNAME` — DagsHub username.
- `MLFLOW_TRACKING_PASSWORD` — DagsHub access token.

**Repository variable**
- `HF_REPO_ID` — target HF repo, e.g. `your-username/wine-quality-cicd`.

---

## Running Locally

```bash
pip install -r requirements.txt

python src/prepare.py
python src/train.py
python src/evaluate.py

pytest
```

---

## Learning Outcomes

- Build an automated CI/CD pipeline with GitHub Actions.
- Checkout, environment setup, dependency install, testing, and Docker build in CI.
- Implement a quality gate for a regression model.
- Deploy a trained model to Hugging Face Hub.
