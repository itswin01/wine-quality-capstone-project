# Wine Quality FastAPI + Docker

A FastAPI service that serves the **registered** wine-quality regression model from the
**MLflow Model Registry**. The model is fetched from the registry and baked into the
Docker image, so the container runs offline.

> These steps assume an **Ubuntu** host with Docker installed.

## Prerequisite

The best model must already be registered in the MLflow Model Registry (done by the
`MLFlow` module's notebook, which registers it as `wine-quality-model`).

## MLflow Registry credentials

`fetch_model.py` reads these from the environment:

| Variable | Meaning |
|----------|---------|
| `MLFLOW_TRACKING_URI` | e.g. `https://dagshub.com/<user>/<repo>.mlflow` |
| `MLFLOW_TRACKING_USERNAME` | DagsHub username |
| `MLFLOW_TRACKING_PASSWORD` | DagsHub access token |
| `MLFLOW_MODEL_NAME` | registered model name (default `wine-quality-model`) |
| `MLFLOW_MODEL_VERSION` | version to pull, or `latest` (default `latest`) |

---

## Run Locally (without Docker)

```bash
pip install -r requirements.txt

export MLFLOW_TRACKING_URI="https://dagshub.com/<user>/<repo>.mlflow"
export MLFLOW_TRACKING_USERNAME="<user>"
export MLFLOW_TRACKING_PASSWORD="<token>"

python fetch_model.py
uvicorn app:app --host 0.0.0.0 --port 8000
```

---

## 1. Build the Docker Image

Credentials are passed as build args and used only to fetch the model — they are not
persisted in the final image.

```bash
docker build \
  --build-arg MLFLOW_TRACKING_URI="https://dagshub.com/<user>/<repo>.mlflow" \
  --build-arg MLFLOW_TRACKING_USERNAME="<user>" \
  --build-arg MLFLOW_TRACKING_PASSWORD="<token>" \
  -t YOUR_DOCKERHUB_USERNAME/wine-quality-fastapi:latest .
```

---

## 2. Run the Docker Container

```bash
docker run -p 8000:8000 YOUR_DOCKERHUB_USERNAME/wine-quality-fastapi:latest
```

The API will be available at `http://localhost:8000` (interactive docs at `/docs`).

---

## 3. Push / Pull (optional)

```bash
docker login
docker push YOUR_DOCKERHUB_USERNAME/wine-quality-fastapi:latest
docker pull YOUR_DOCKERHUB_USERNAME/wine-quality-fastapi:latest
```

---

# API Endpoints

## Home — `GET /`
## Health Check — `GET /health`

```json
{ "status": "ok" }
```

## Prediction — `POST /predict`

The `features` array must contain the 11 values **in this exact order**:

```
fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides,
free_sulfur_dioxide, total_sulfur_dioxide, density, ph, sulphates, alcohol
```

Request

```json
{
    "features": [
        7.4, 0.7, 0.0, 1.9, 0.076,
        11.0, 34.0, 0.9978, 3.51, 0.56, 9.4
    ]
}
```

Example Response

```json
{
    "predicted_quality": 5.32,
    "feature_order": [
        "fixed_acidity", "volatile_acidity", "citric_acid", "residual_sugar",
        "chlorides", "free_sulfur_dioxide", "total_sulfur_dioxide", "density",
        "ph", "sulphates", "alcohol"
    ]
}
```

---
