from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import mlflow.pyfunc

## Load the registered model that was baked in by fetch_model.py
model = mlflow.pyfunc.load_model("mlflow_model")

## Feature order the model was trained on (11 physicochemical measurements)
FEATURE_NAMES = [
    "fixed_acidity", "volatile_acidity", "citric_acid", "residual_sugar",
    "chlorides", "free_sulfur_dioxide", "total_sulfur_dioxide", "density",
    "ph", "sulphates", "alcohol",
]

## Create FastAPI app
app = FastAPI(
    title="Wine Quality Prediction API",
    description="Predict red wine quality score using the registered MLflow model",
    version="1.0",
)


## Request schema — 11 feature values, in the order of FEATURE_NAMES
class WineFeatures(BaseModel):
    features: list[float]


@app.get("/")
def home():
    return {
        "message": "Welcome to the Wine Quality Prediction API!",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(data: WineFeatures):

    frame = pd.DataFrame([data.features], columns=FEATURE_NAMES)
    prediction = model.predict(frame)[0]

    return {
        "predicted_quality": round(float(prediction), 4),
        "feature_order": FEATURE_NAMES,
    }
