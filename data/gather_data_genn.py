
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
    for p in path.glob("*.json"):
        with p.open() as f:
            data = json.load(f)
        #algo = data["nested_loop_algo"]
        timers = data["timers"]
        timers = {k.replace(" ", "_"): v for k, v in timers.items()}
        # Quick fix timer error for start and total values
        #if "start" in timers:
        #    timers["total"] = timers["total"] + timers["simulate"] - timers["start"]
        #    timers.pop("start", None)
        #if algo not in results:
        #    results[algo] = {}
        if results=={}:
            for timer in timers:
                results[timer] = []
            results['network_construction_time'] = []
            results['network_construction_time_nobuild'] = []

        for timer in timers:
            results[timer].append(timers[timer])

        #print(timers)
        results['network_construction_time'].append(timers['time_model_def'] + timers['time_build'] + timers['time_load'])
        results['network_construction_time_nobuild'].append(timers['time_model_def'] + timers['time_load'])

    return results


def get_statistics(results: dict):
    stats = {}
    #for algo in results:
    #    if algo not in stats:
    #        stats[algo] = {}
    for timer in results:
        times = np.array(results[timer])
        #print(times)
        if isinstance(times[0], np.int_):
            times = times / 1e9
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
