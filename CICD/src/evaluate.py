"""
Stage 3: evaluate
Scores the model on the held-out test set,
This exit code is what stops a bad model from ever reaching the register step.
"""
import sys
import json
import yaml
import joblib
import pandas as pd

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


def main():
    params = yaml.safe_load(open("params.yaml"))["evaluate"]

    model = joblib.load("model/model.joblib")

    test_df = pd.read_csv("data/test.csv")

    X_test = test_df.drop(columns=["quality"])
    y_test = test_df["quality"]

    preds = model.predict(X_test)

    metrics = {
        "mae": mean_absolute_error(y_test, preds),
        "rmse": mean_squared_error(y_test, preds) ** 0.5,
        "r2": r2_score(y_test, preds),
    }

    with open("metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print(json.dumps(metrics, indent=2))

    # Quality Gate
    if metrics["r2"] < params["min_r2"]:
        print(
            f"FAIL: R² {metrics['r2']:.4f} "
            f"is below gate {params['min_r2']}"
        )
        sys.exit(1)

    print("PASS: model cleared the quality gate")


if __name__ == "__main__":
    main()
