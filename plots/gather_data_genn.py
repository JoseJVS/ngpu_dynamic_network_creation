
import json
import numpy as np

from pathlib import Path
from argparse import ArgumentParser


def get_paths():
    parser = ArgumentParser()
    parser.add_argument("path", type=str)
    parser.add_argument("out", type=str)
    args = parser.parse_args()
    p = Path(args.path)
    o = Path(args.out)
    assert p.is_dir() and (not o.exists() or o.is_file())
    if o.is_file():
        print(f"WARNING: overriding {o}")

    return p, o


def get_json_results(path: Path):
    results = {}
    for p in path.glob("*/*.json"):
        with p.open() as f:
            data = json.load(f)
        timers = data["timers"]
        for timer in timers:
            if timer not in results:
                results[timer] = []
            results[timer].append(timers[timer])
    return results


def get_statistics(results: dict):
    stats = {}
    for timer in results:
        times = np.array(results[timer]) / 1e9
        stats[timer] = {
            "mean": np.mean(times),
            "std": np.std(times)
        }
    
    return stats


def save_statistics(stats: dict, out: Path):
    with out.open("w") as f:
        json.dump(stats, f, indent=4)


def main():
    path, out = get_paths()
    res = get_json_results(path)
    stats = get_statistics(res)
    save_statistics(stats, out)


if __name__ == "__main__":
    main()
