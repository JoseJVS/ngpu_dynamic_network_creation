#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
    for p in path.glob("*/*/*.json"):
        with p.open() as f:
            data = json.load(f)

        d_conf = data["conf"]
        d_seed = d_conf.pop("seed")
        d_ranks = data["ranks"]
        d_all_values = data["all_values"]

        id_conf = f"n-{d_conf['nodes']}-p-{d_conf['procs']}-t-{d_conf['threads']}"
        if id_conf not in results:
            results[id_conf] = {
                "conf": d_conf,
                "seeds": [],
                "ranks": {},
                "all_values": {
                    "stats": {},
                    "timers": {}
                }
            }

        # In one configuration a seed must be unique
        r_seeds = results[id_conf]["seeds"]
        assert d_seed not in r_seeds
        r_seeds.append(d_seed)

        r_ranks = results[id_conf]["ranks"]
        r_all_values = results[id_conf]["all_values"]
        
        # BEGIN rank lists
        for rank in d_ranks:
            d_stats = d_ranks[rank]["stats"]
            d_timers = d_ranks[rank]["timers"]

            if rank not in r_ranks:
                r_ranks[rank] = {
                    "stats": {},
                    "timers": {}
                }

            r_stats = r_ranks[rank]["stats"]
            r_timers = r_ranks[rank]["timers"]

            # Ger per rank stats
            if r_stats == {}:
                for stat in d_stats:
                    r_stats[stat] = [d_stats[stat]]
            else:
                for stat in d_stats:
                    r_stats[stat].append(d_stats[stat])
            
            
            # Get per rank timers
            if r_timers == {}:
                for timer in d_timers:
                    r_timers[timer] = [d_timers[timer]]
            else:
                for timer in d_timers:
                    r_timers[timer].append(d_timers[timer])
        # END rank lists

        # BEGIN all values
        # Get per conf stats
        if r_all_values["stats"] == {}:
            for stat in d_all_values["stats"]:
                r_all_values["stats"][stat] = [d_all_values["stats"][stat]]
        else:
            for stat in d_all_values["stats"]:
                r_all_values["stats"][stat].append(d_all_values["stats"][stat])

        # Get per conf timers
        if r_all_values["timers"] == {}:
            for timer in d_all_values["timers"]:
                r_all_values["timers"][timer] = d_all_values["timers"][timer]
        else:
            for timer in d_all_values["timers"]:
                r_all_values["timers"][timer].extend(d_all_values["timers"][timer])
        # END all values

    # Sanity check
    for cid in results:
        num_seeds = len(results[cid]["seeds"])
        for rank in results[cid]["ranks"]:
            for stat in results[cid]["ranks"][rank]["stats"]:
                assert len(results[cid]["ranks"][rank]["stats"][stat]) == num_seeds
            for timer in results[cid]["ranks"][rank]["timers"]:
                assert len(results[cid]["ranks"][rank]["timers"][timer]) == num_seeds
        for stat in results[cid]["all_values"]["stats"]:
            assert len(results[cid]["all_values"]["stats"][stat]) == num_seeds
        for timer in results[cid]["all_values"]["timers"]:
            assert len(results[cid]["all_values"]["timers"][timer]) == num_seeds * results[cid]["conf"]["procs"] * results[cid]["conf"]["nodes"]

    return results


def get_statistics(results: dict):
    stats = {}
    
    for cid in results:
        r_conf = results[cid]["conf"]
        r_seeds = results[cid]["seeds"]
        r_ranks = results[cid]["ranks"]
        r_all_values = results[cid]["all_values"]

        if cid not in stats:
            stats[cid] = {
                "conf": r_conf,
                "seeds": r_seeds,
                "ranks": {},
                "all_values": {
                    "stats": {},
                    "timers": {}
                }
            }

        s_ranks = stats[cid]["ranks"]
        s_all_values = stats[cid]["all_values"]

        # BEGIN rank lists
        for rank in r_ranks:
            r_stats = r_ranks[rank]["stats"]
            r_timers = r_ranks[rank]["timers"]

            assert rank not in s_ranks
            s_ranks[rank] = {
                    "stats": {},
                    "timers": {}
                }
            
            s_stats = s_ranks[rank]["stats"]
            s_timers = s_ranks[rank]["timers"]

            for stat in r_stats:
                stat_vals = np.array(r_stats[stat])
                s_stats[stat] = {
                    "mean": np.mean(stat_vals),
                    "std": np.std(stat_vals)
                }

            for timer in r_timers:
                timer_vals = np.array(r_timers[timer]) / 1e9
                s_timers[timer] = {
                    "mean": np.mean(timer_vals),
                    "std": np.std(timer_vals)
                }
        # END rank lists

        # BEGIN all values
        for stat in r_all_values["stats"]:
            stat_vals = np.array(r_all_values["stats"][stat])
            s_all_values["stats"][stat] = {
                "mean": np.mean(stat_vals),
                "std": np.std(stat_vals)
            }

        for timer in r_all_values["timers"]:
            timer_vals = np.array(r_all_values["timers"][timer]) / 1e9
            if timer == "time_network":
                time_net = timer_vals
            elif timer == "time_create":
                time_cr = timer_vals
            elif timer == "time_connect":
                time_cn = timer_vals
            elif timer == "time_presimulate":
                time_ps = timer_vals
            s_all_values["timers"][timer] = {
                "mean": np.mean(timer_vals),
                "std": np.std(timer_vals)
            }

        time_build = time_net + time_cr + time_cn + time_ps
        s_all_values["timers"]["network_construction_time"] = {
                "mean": np.mean(time_build),
                "std": np.std(time_build)
            }
        # END all values
    
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
