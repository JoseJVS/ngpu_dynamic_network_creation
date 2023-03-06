
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
        threads = data["threads"]
        data.pop("threads", None)
        procs = data["procs"]
        data.pop("procs", None)
        vps = data["vps"]
        data.pop("vps", None)
        conf = f"{threads}-{procs}-{vps}"
        if conf not in results:
            results[conf] = {
                "threads": threads,
                "procs": procs,
                "vps": vps,
                "ranks": {},
                "all": {
                    "stats": {},
                    "timers": {}
                }
            }
        all = results[conf]["all"]
        ranks = results[conf]["ranks"]
        for rank in data:
            if rank not in ranks:
                ranks[rank] = {
                    "stats": {},
                    "timers": {}
                }
            stats = ranks[rank]["stats"]
            for stat in data[rank]["stats"]:
                if stat not in stats:
                    stats[stat] = []
                if stat not in all["stats"]:
                    all["stats"][stat] = 0
                stats[stat].append(data[rank]["stats"][stat])
                all["stats"][stat] += data[rank]["stats"][stat]
            
            timers = ranks[rank]["timers"]
            for timer in data[rank]["timers"]:
                if timer not in timers:
                    timers[timer] = []
                if timer not in all["timers"]:
                    all["timers"][timer] = []
                timers[timer].append(data[rank]["timers"][timer])
                all["timers"][timer].append(data[rank]["timers"][timer])

    return results


def get_statistics(results: dict):
    stats = {}
    for conf in results:
        if conf not in stats:
            stats[conf] = {
                "threads": results[conf]["threads"],
                "procs": results[conf]["procs"],
                "vps": results[conf]["vps"],
                "ranks": {},
                "all": {
                    "stats": {},
                    "timers": {}
                }
            }
        s_ranks = stats[conf]["ranks"]
        r_ranks = results[conf]["ranks"]
        for rank in r_ranks:
            if rank not in s_ranks:
                s_ranks[rank] = {
                    "stats": {},
                    "timers": {}
                }
            for stat in r_ranks[rank]["stats"]:
                stat_vals = r_ranks[rank]["stats"][stat]
                assert len(stat_vals) == 10
                s_ranks[rank]["stats"][stat] = {
                    "mean": np.mean(stat_vals),
                    "std": np.std(stat_vals),
                }
            for timer in r_ranks[rank]["timers"]:
                timer_vals = np.array(r_ranks[rank]["timers"][timer]) / 1e9
                assert len(timer_vals) == 10
                s_ranks[rank]["timers"][timer] = {
                    "mean": np.mean(timer_vals),
                    "std": np.std(timer_vals),
                }
        
        s_all = stats[conf]["all"]
        r_all = results[conf]["all"]
        for stat in r_all["stats"]:
            s_all["stats"][stat] = r_all["stats"][stat] / 10
            if stat == "num_neurons":
                s_all["stats"][stat] = s_all["stats"][stat] / results[conf]["procs"]
        for timer in r_all["timers"]:
            timer_vals = np.array(r_all["timers"][timer]) / 1e9
            assert len(timer_vals) == 10 * results[conf]["procs"]
            s_all["timers"][timer] = {
                "mean": np.mean(timer_vals),
                "std": np.std(timer_vals),
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
