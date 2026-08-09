from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import pandas as pd
import mlflow.pyfunc


model = mlflow.pyfunc.load_model("mlflow_model")


FEATURE_NAMES = [
    "fixed_acidity",
    "volatile_acidity",
    "citric_acid",
    "residual_sugar",
    "chlorides",
    "free_sulfur_dioxide",
    "total_sulfur_dioxide",
    "density",
    "ph",
    "sulphates",
    "alcohol",
]


app = FastAPI(
    title="Wine Quality Prediction API",
    description=(
        "Predict red wine quality using an MLflow-registered "
        "machine learning model."
    ),
    version="1.0",
)


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)


class WineFeatures(BaseModel):
    features: list[float]


@app.get("/", include_in_schema=False)
def home():
    return FileResponse("static/index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(data: WineFeatures):

    if len(data.features) != len(FEATURE_NAMES):
        return {
            "error": (
                f"Expected {len(FEATURE_NAMES)} features, "
                f"but received {len(data.features)}."
            )
        }

    frame = pd.DataFrame(
        [data.features],
        columns=FEATURE_NAMES,
    )

    prediction = model.predict(frame)[0]

    return {
        "predicted_quality": round(float(prediction), 4),
        "feature_order": FEATURE_NAMES,
    }
