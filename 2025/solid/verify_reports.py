import argparse
import json
import math
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import Any, cast

MetricMap = dict[str, Any]


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare JSON outputs from the sales-report implementations."
    )
    parser.add_argument(
        "--outputs-dir",
        type=Path,
        default=Path(__file__).parent / "output",
        help="Directory containing the JSON outputs.",
    )
    parser.add_argument(
        "--baseline",
        type=Path,
        default=None,
        help=(
            "Specific baseline JSON file to compare against. "
            "Defaults to the first file found in outputs-dir."
        ),
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=1e-6,
        help="Absolute tolerance for comparing numeric values.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print per-file comparison details even when all metrics match.",
    )
    return parser.parse_args(list(argv))


def load_metrics(path: Path) -> MetricMap:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)

    if not isinstance(data, dict):
        raise TypeError(f"Expected JSON object in {path}, found {type(data).__name__}")

    if not all(isinstance(key, str) for key in data):
        raise TypeError(f"Expected string keys in {path}")

    return cast(MetricMap, data)


def is_close(a: Any, b: Any, tolerance: float) -> bool:
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(float(a), float(b), rel_tol=0.0, abs_tol=tolerance)
    return a == b


def compare_metrics(
    baseline_metrics: MetricMap,
    candidate_metrics: MetricMap,
    tolerance: float,
) -> tuple[bool, str]:
    baseline_keys = set(baseline_metrics)
    candidate_keys = set(candidate_metrics)

    missing = baseline_keys - candidate_keys
    extra = candidate_keys - baseline_keys

    if missing or extra:
        parts = []
        if missing:
            parts.append(f"missing keys: {sorted(missing)}")
        if extra:
            parts.append(f"unexpected keys: {sorted(extra)}")
        return False, "; ".join(parts)

    mismatches = []
    for key in sorted(baseline_keys):
        baseline_value = baseline_metrics[key]
        candidate_value = candidate_metrics[key]
        if not is_close(baseline_value, candidate_value, tolerance):
            mismatches.append(
                f"{key!r}: {candidate_value!r} != {baseline_value!r}"
            )

    if mismatches:
        return False, "; ".join(mismatches)
    return True, ""


def main(argv: Iterable[str]) -> int:
    args = parse_args(argv)

    outputs_dir: Path = args.outputs_dir
    if not outputs_dir.exists() or not outputs_dir.is_dir():
        print(f"Outputs directory does not exist: {outputs_dir}", file=sys.stderr)
        return 2

    json_files = sorted(outputs_dir.glob("*.json"))
    if not json_files:
        print(f"No JSON files found in {outputs_dir}", file=sys.stderr)
        return 2

    baseline_arg = args.baseline
    if baseline_arg is not None:
        if not baseline_arg.exists():
            print(f"Baseline file not found: {baseline_arg}", file=sys.stderr)
            return 2
        baseline_path = baseline_arg
    else:
        baseline_path = json_files[0]

    baseline_metrics = load_metrics(baseline_path)
    print(f"Baseline: {baseline_path.name}")

    failures: list[tuple[Path, str]] = []
    for path in json_files:
        if path == baseline_path:
            if args.verbose:
                print(f"✔ {path.name} (baseline)")
            continue

        metrics = load_metrics(path)
        ok, message = compare_metrics(baseline_metrics, metrics, args.tolerance)
        if ok:
            if args.verbose:
                print(f"✔ {path.name}")
        else:
            print(f"✖ {path.name}: {message}")
            failures.append((path, message))

    if failures:
        print(f"\n{len(failures)} file(s) differ from baseline.", file=sys.stderr)
        return 1

    print("\nAll report outputs match.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

