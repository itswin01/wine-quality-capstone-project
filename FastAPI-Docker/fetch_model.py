"""
Download the registered model from the MLflow Model Registry and bake it
into a local directory (./mlflow_model) so the API can load it offline.

Reads MLflow tracking configuration from the environment:
    MLFLOW_TRACKING_URI       e.g. https://dagshub.com/<user>/<repo>.mlflow
    MLFLOW_TRACKING_USERNAME  DagsHub username
    MLFLOW_TRACKING_PASSWORD  DagsHub access token
    MLFLOW_MODEL_NAME         registered model name (default: wine-quality-model)
    MLFLOW_MODEL_VERSION      version to pull, or "latest" (default: latest)

Run this once before starting the API locally. Inside Docker it is executed
during the image build so the model ships inside the image.
"""

import os
import mlflow
from mlflow.tracking import MlflowClient

MODEL_NAME = os.environ.get("MLFLOW_MODEL_NAME", "wine-quality-model")
MODEL_VERSION = os.environ.get("MLFLOW_MODEL_VERSION", "latest")
DST_DIR = "mlflow_model"


def resolve_version(client: MlflowClient) -> str:
    if MODEL_VERSION != "latest":
        return MODEL_VERSION
    versions = client.search_model_versions(f"name='{MODEL_NAME}'")
    if not versions:
        raise RuntimeError(
            f"No versions found for registered model '{MODEL_NAME}'. "
            "Register it from the MLFlow notebook first."
        )
    latest = max(versions, key=lambda v: int(v.version))
    return latest.version


def main():
    client = MlflowClient()
    version = resolve_version(client)

    uri = f"models:/{MODEL_NAME}/{version}"
    print(f"Downloading {uri} -> ./{DST_DIR}")

    local_path = mlflow.artifacts.download_artifacts(
        artifact_uri=uri, dst_path=DST_DIR
    )
    print(f"Registered model saved to {local_path}")


if __name__ == "__main__":
    main()
