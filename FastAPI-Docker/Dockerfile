FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# MLflow Model Registry credentials, supplied at build time via --build-arg.
# They are consumed only by the fetch step below and are NOT persisted as ENV,
# so the token does not leak into the final image layers.
ARG MLFLOW_TRACKING_URI
ARG MLFLOW_TRACKING_USERNAME
ARG MLFLOW_TRACKING_PASSWORD
ARG MLFLOW_MODEL_NAME=wine-quality-model
ARG MLFLOW_MODEL_VERSION=latest

# Fetch the registered model and bake it into the image (./mlflow_model)
RUN MLFLOW_TRACKING_URI="$MLFLOW_TRACKING_URI" \
    MLFLOW_TRACKING_USERNAME="$MLFLOW_TRACKING_USERNAME" \
    MLFLOW_TRACKING_PASSWORD="$MLFLOW_TRACKING_PASSWORD" \
    MLFLOW_MODEL_NAME="$MLFLOW_MODEL_NAME" \
    MLFLOW_MODEL_VERSION="$MLFLOW_MODEL_VERSION" \
    python fetch_model.py

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
