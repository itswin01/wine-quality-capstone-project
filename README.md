# Wine Quality Capstone Project — MLOps Pipeline

An end-to-end MLOps capstone built around the **Wine Quality (red)** dataset,
demonstrating the complete machine learning lifecycle — from data versioning and
experiment tracking to containerization, CI/CD automation, and model deployment.

The task throughout is **regression**: predicting a wine's `quality` score from 11
physicochemical measurements (acidity, sugar, chlorides, sulphates, alcohol, etc.).

---

## Project Links

| Resource | Link |
|----------|------|
| GitHub Repository | _add your repo URL_ |
| DagsHub Experiments (MLFlow) | _add your DagsHub experiments URL_ |
| MLflow Model Registry (MLFlow) | _add your DagsHub Models URL_ |
| Hugging Face Model (CICD) | _add your Hugging Face model URL_ |
| Docker Hub (FastAPI-Docker) | _add your Docker Hub image URL_ |

---

## Repository Structure

```
.
├── DVC-ML-Pipeline
├── MLFlow
├── FastAPI-Docker
├── CICD
├── .github/workflows/ci-cd.yaml
└── README.md
```

---

## Modules

### 📁 DVC-ML-Pipeline — Data Version Control (DVC)

A reproducible five-stage ML pipeline built with **DVC**: data ingestion →
preprocessing → feature engineering → model building → model evaluation. The dataset is
pulled directly from the UCI repository; each stage's inputs, outputs, and metrics are
tracked so the whole pipeline reproduces with a single `dvc repro`.

**Tools:** Python, DVC, Git, Scikit-learn

---

### 📁 MLFlow — Experiment Tracking with DagsHub

Experiment tracking with **MLflow**, using **DagsHub** as the remote tracking server.
Three regressors (Linear Regression, Random Forest, XGBoost) are trained and their
parameters, metrics (MAE, RMSE, R²), and model artifacts are logged for comparison. The
best model is registered in the **MLflow Model Registry** as `wine-quality-model`.

**Tools:** Python, MLflow, MLflow Model Registry, DagsHub, Scikit-learn, XGBoost

---

### 📁 FastAPI-Docker — Dockerized Inference API

A **FastAPI** service that serves the **registered** model pulled from the MLflow Model
Registry, containerized with **Docker**. The model is fetched and baked into the image at
build time so the container runs offline. Intended to be built and run on **Ubuntu**.

**Tools:** FastAPI, Docker, Uvicorn, MLflow, Python

---

### 📁 CICD — CI/CD Pipeline with GitHub Actions

An automated **GitHub Actions** workflow that runs on every push/PR to `main`: checkout →
set up Python → install dependencies → run tests → train + evaluate (R² quality gate) →
**deploy to Hugging Face Hub** → **build the FastAPI Docker image**.

**Tools:** GitHub Actions, PyTest, Docker, Hugging Face Hub, Scikit-learn, Python

---

## Technologies Used

- Python
- Git & GitHub
- DVC
- MLflow (+ Model Registry)
- DagsHub
- FastAPI
- Docker
- GitHub Actions
- Hugging Face Hub
- Scikit-learn
- XGBoost
- PyTest

---

## Dataset

**Wine Quality (Red)** — UCI Machine Learning Repository. 1,599 samples, 11
physicochemical input features, and an integer `quality` target (0–10, observed range
3–8).
