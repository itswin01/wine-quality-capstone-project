import subprocess
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.prepare import load_dataset  # noqa: E402


def test_load_dataset():
    df = load_dataset()

    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert "quality" in df.columns


def test_prepare_script_runs(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    (tmp_path / "params.yaml").write_text(
        "prepare:\n"
        "  test_size: 0.2\n"
        "  random_state: 42\n"
    )

    dataset_path = Path(__file__).resolve().parents[1] / "winequality-red.csv"
    (tmp_path / "winequality-red.csv").write_bytes(dataset_path.read_bytes())

    result = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).resolve().parents[1] / "src" / "prepare.py"),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert (tmp_path / "data" / "train.csv").exists()
    assert (tmp_path / "data" / "test.csv").exists()
