
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
    assert p.is_file() and (not o.exists() or o.is_file())
    if o.is_file():
        print(f"WARNING: overriding {o}")

    return p, o


def get_json_results(path: Path):
    with path.open("r") as f:
        results = json.load(f)

    return results


def get_statistics(results: dict):
    best_time = np.inf
    best_conf = None
    for conf in results:
        time = results[conf]["all"]["timers"]["time_simulate"]["mean"]
        if time < best_time:
            best_time = time
            best_conf = conf
    
    return results[best_conf]


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
