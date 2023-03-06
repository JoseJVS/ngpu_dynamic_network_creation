
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
        algo = data["nested_loop_algo"]
        timers = data["timers"]
        if algo not in results:
            results[algo] = {}
            for timer in timers:
                results[algo][timer] = []
        for timer in timers:
            results[algo][timer].append(timers[timer])

    return results


def get_statistics(results: dict):
    stats = {}
    for algo in results:
        if algo not in stats:
            stats[algo] = {}
        for timer in results[algo]:
            times = np.array(results[algo][timer]) / 1e9
            if timer == "time_network":
                times_network = times
            if timer == "time_create":
                times_create = times
            if timer == "time_connect":
                times_connect = times
            if timer == "time_calibrate":
                times_calibrate = times
            stats[algo][timer] = {
                "mean": np.mean(times),
                "std": np.std(times)
            }

        times_build = times_network + times_create + times_connect + times_calibrate
        stats[algo]["network_construction_time"] = {
            "mean": np.mean(times_build),
            "std": np.std(times_build)
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
