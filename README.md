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
| GitHub Repository | https://github.com/itswin01/wine-quality-capstone-project |
| DagsHub Experiments (MLFlow) | https://dagshub.com/itswin01/wine-quality-capstone-project.mlflow |
| MLflow Model Registry (MLFlow) | https://dagshub.com/itswin01/wine-quality-capstone-project.mlflow/#/models/wine-quality-model |
| Hugging Face Model (CICD) | https://huggingface.co/itswin01/wine-quality-model |
| Docker Hub (FastAPI-Docker) | https://hub.docker.com/r/itswin01/wine-quality-fastapi |

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

### DVC-ML-Pipeline — Data Version Control (DVC)

A reproducible five-stage ML pipeline built with **DVC**: data ingestion →
preprocessing → feature engineering → model building → model evaluation. The dataset is
pulled directly from the UCI repository; each stage's inputs, outputs, and metrics are
tracked so the whole pipeline reproduces with a single `dvc repro`.

**Tools:** Python, DVC, Git, Scikit-learn

---

### MLFlow — Experiment Tracking with DagsHub

Experiment tracking with **MLflow**, using **DagsHub** as the remote tracking server.
Three regressors (Linear Regression, Random Forest, XGBoost) are trained and their
parameters, metrics (MAE, RMSE, R²), and model artifacts are logged for comparison. The
best model is registered in the **MLflow Model Registry** as `wine-quality-model`.

**Tools:** Python, MLflow, MLflow Model Registry, DagsHub, Scikit-learn, XGBoost

---

### FastAPI-Docker — Dockerized Inference API

A **FastAPI** service that serves the **registered** model pulled from the MLflow Model
Registry, containerized with **Docker**. The model is fetched and baked into the image at
build time so the container runs offline. Intended to be built and run on **Ubuntu**.

**Tools:** FastAPI, Docker, Uvicorn, MLflow, Python

---

### CICD — CI/CD Pipeline with GitHub Actions

An automated **GitHub Actions** workflow that runs on every push/PR to `main`: checkout →
set up Python → install dependencies → run tests → train + evaluate (R² quality gate) →
**deploy to Hugging Face Hub** → **build the FastAPI Docker image**.

**Tools:** GitHub Actions, PyTest, Docker, Hugging Face Hub, Scikit-learn, Python

---

## Using the Application (Docker Hub)

The FastAPI service is published as a ready-to-run image on Docker Hub:

**https://hub.docker.com/r/itswin01/wine-quality-fastapi**

An external user does **not** need to clone this repository or hold any DagsHub
credentials — the trained MLflow model is **baked into the image at build time**. The
only requirement is Docker.

### Quick start

**1. Pull the published image:**

```bash
docker pull itswin01/wine-quality-fastapi:latest
```

**2. Run the container:**

```bash
docker run -p 8000:8000 itswin01/wine-quality-fastapi:latest
```

**3. Open the app:**

- Prediction UI → http://localhost:8000
- API docs (Swagger) → http://localhost:8000/docs

### End-to-end flow

```text
Docker Hub → pull image → run container → FastAPI starts
  → open localhost:8000 → enter 11 wine characteristics
  → "Predict Wine Quality" → /predict endpoint → MLflow model
  → predicted quality score (/10) + plain-language interpretation
```

> **Why it just works:** the MLflow-registered model is packaged inside the Docker image
> during the build, so the external user never downloads the model separately or
> configures DagsHub. Pull → run → predict.

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

---

## Author

**Tejaswin Bhola**
SSN College of Engineering
