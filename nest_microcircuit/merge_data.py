#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from pathlib import Path
from argparse import ArgumentParser


def get_paths():
    parser = ArgumentParser()
    parser.add_argument("path", type=str)
    parser.add_argument("--out", type=str, default="merge.json")
    parser.add_argument("--cleanup", default=False, action="store_true")
    args = parser.parse_args()
    p = Path(args.path)
    o = Path(args.out)
    assert p.is_dir() and (not o.exists() or o.is_file())
    if o.is_file():
        print(f"WARNING: overriding {o}")

    return p, o, args.cleanup


def get_json_results(path: Path):
    results = {
        "conf": {},
        "ranks": {},
        "all_values": {
            "stats": {},
            "timers": {}
        }
    }
    stat_count = {}
    for p in path.glob("*.json"):
        with p.open() as f:
            data = json.load(f)
        rank = data["rank"]
        conf = data["conf"]
        stats = data["stats"]
        timers = data["timers"]
        
        if results["conf"] == {}:
            results["conf"] = conf
        else:
            for param in conf:
                assert results["conf"][param] == conf[param]

        assert rank not in results["ranks"]
        results["ranks"][rank] = {
                "stats": stats,
                "timers": timers
            }

        if results["all_values"]["stats"] == {}:
            for stat in stats:
                stat_count[stat] = 1
                results["all_values"]["stats"][stat] = stats[stat]
        else:
            for stat in stats:
                stat_count[stat] += 1
                results["all_values"]["stats"][stat] += stats[stat]

        if results["all_values"]["timers"] == {}:
            for timer in timers:
                results["all_values"]["timers"][timer] = [timers[timer]]
        else:
            for timer in timers:
                results["all_values"]["timers"][timer].append(timers[timer])

    total_procs = results["conf"]["procs"]

    assert len(results["ranks"]) == total_procs

    for stat in results["all_values"]["stats"]:
        assert stat_count[stat] == total_procs

    for timer in results["all_values"]["timers"]:
        assert len(results["all_values"]["timers"][timer]) == total_procs

    return results


def cleanup(path: Path):
    for p in path.glob("*.json"):
        p.unlink()
    for p in path.glob("*.dat"):
        p.unlink()


def save_data(results: dict, out: Path):
    with out.open("w") as f:
        json.dump(results, f, indent=4)


def main():
    path, out, kup = get_paths()
    res = get_json_results(path)
    if kup:
        cleanup(path)
    save_data(res, out)


if __name__ == "__main__":
    main()
