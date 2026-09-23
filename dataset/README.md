from __future__ import annotations

import argparse
from pathlib import Path

from ml.preprocessing.preprocess import run_preprocessing


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the DDoS dataset preprocessing pipeline.")
    parser.add_argument("--dataset", type=str, required=True, help="Path to the dataset CSV file.")
    parser.add_argument("--output-dir", type=str, default="ml/models", help="Directory for saved artifacts.")
    parser.add_argument("--label-column", type=str, default="label", help="Column containing attack labels.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_preprocessing(
        dataset_path=Path(args.dataset),
        output_dir=Path(args.output_dir),
        label_column=args.label_column,
    )
    print(result)


if __name__ == "__main__":
    main()
