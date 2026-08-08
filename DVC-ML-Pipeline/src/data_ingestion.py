"""
Stage 1: Data Ingestion
------------------------
Loads the Wine Quality (red) dataset (regression: predicts the wine
'quality' score from 11 physicochemical measurements) and dumps it as a
raw CSV file.

The dataset comes from the UCI Machine Learning Repository. The original
file is semicolon-separated with spaces in the column names, so we clean
the column names into a consistent lowercase/underscore form here.

Output:
    data/raw/data.csv
"""

import os
import pandas as pd

DATA_URL = (
    "https://archive.ics.uci.edu/ml/machine-learning-databases/"
    "wine-quality/winequality-red.csv"
)


def load_data() -> pd.DataFrame:
    """Load the Wine Quality (red) dataset into a DataFrame."""
    df = pd.read_csv(DATA_URL, sep=";")
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    # 'quality' (integer 3-8) is the regression target
    return df


def save_raw_data(df: pd.DataFrame, out_dir: str = "data/raw") -> None:
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "data.csv")
    df.to_csv(out_path, index=False)
    print(f"[data_ingestion] Saved raw data -> {out_path} (shape={df.shape})")


def main():
    df = load_data()
    save_raw_data(df)


if __name__ == "__main__":
    main()
