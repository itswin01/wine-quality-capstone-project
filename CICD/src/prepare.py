"""
Stage 1: prepare
Loads the raw dataset and produces a deterministic train/test split.
"""
import yaml
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

OUT_DIR = Path("data")


def load_dataset() -> pd.DataFrame:
    df = pd.read_csv("winequality-red.csv")
    return df


def main():
    params = yaml.safe_load(open("params.yaml"))["prepare"]

    OUT_DIR.mkdir(exist_ok=True)

    df = load_dataset()

    X = df.drop(columns=["quality"])
    y = df["quality"]

    train_X, test_X, train_y, test_y = train_test_split(
        X,
        y,
        test_size=params["test_size"],
        random_state=params["random_state"],
    )

    train_df = train_X.copy()
    train_df["quality"] = train_y

    test_df = test_X.copy()
    test_df["quality"] = test_y

    train_df.to_csv(OUT_DIR / "train.csv", index=False)
    test_df.to_csv(OUT_DIR / "test.csv", index=False)

    print(f"Wrote {len(train_df)} train rows")
    print(f"Wrote {len(test_df)} test rows")


if __name__ == "__main__":
    main()
