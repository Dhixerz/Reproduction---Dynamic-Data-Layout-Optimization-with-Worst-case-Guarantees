from utils.setup import *
from utils.tree import *
from utils.config import *
from offline.states import *
from online.counter import *
import numpy as np
import argparse
import os
import pickle


def run_random(fname, k, output_dir, N=3):
    query = []
    movement = []
    schedule = {}
    T = len(queries) // args.interval
    for trials in range(N):
        tb = TreeBuilder(df, df_sample, config, args, k, output_dir)
        init_states = tb.get_init_states(queries)
        sg = StateGenerator(tb, init_states, args.interval, eps, True)
        sg.reset_reservoir(args.res)
        cm = CounterManager(sg, alpha, args.gamma, args.lag)

        # Run randomized algorithm
        for i in range(T):
            new_queries = queries[i * args.interval:(i + 1) * args.interval]
            cm.process_queries(new_queries)
  
        avg_states = np.average(cm.num_states) if len(cm.num_states) > 0 else 0
        max_states = max(cm.num_states) if len(cm.num_states) > 0 else 0
        avg_removed = np.average(cm.num_removed) if len(cm.num_removed) > 0 else 0

        print("q: %f, m: %f" % (cm.query_cost, cm.movement_cost))
        print("Avg #states: %f (max: %d), avg removed: %f" % (
            avg_states, max_states, avg_removed))

        query.append(cm.query_cost)
        movement.append(cm.movement_cost)
        schedule["%s-%d" % (fname, trials)] = cm.schedule
    return schedule, query, movement


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Random.')
    parser.add_argument('--config', default="demo", help="Config File Path")

    parser.add_argument('--k', type=int, default=None, help="Override partition count k")
    
    parsed_args = parser.parse_args()
    args = Args(parsed_args.config)
 
    if parsed_args.k is not None:
        print(f"k {args.k} to {parsed_args.k}")
        args.k = parsed_args.k

    np.random.seed(args.seed)
    np.seterr(invalid='ignore')
    alpha = args.alpha
    eps = args.eps
    print("alpha=%d, epsilon=%.3f" % (alpha, eps))

    fnames, files, parts, config = setup_perfile(args)
    queries = get_workload_perfile(config, files, fnames, args)
    print("# queries: %d" % len(queries))
    total_query = 0
    total_movement = 0
    total_size = 0
    for i, fname in enumerate(fnames):
        print(fname)
     
        df, df_sample, _ = get_data(config, args, parts, files[i], fname)
        k = args.k  

        N = len(df)
        output_dir = "%s/%s-%s-%d-%d-%s" % (config["ds"], fname, args.q, args.interval, k, args.method)

        schedule, query, movement = run_random(fname, k, output_dir, 1)

        total_size += N
        total_query += np.average(query) * N
        total_movement += np.average(movement) * N
        print("[%s] Query: %f, %f, Movement: %f, %f" % (
            fname, np.average(query), np.std(query), np.average(movement), np.std(movement)))
        if args.policy == "oracle":
            pickle.dump(schedule, open(
                "resources/schedule/random/%s-%s-%s-%d-%s-%d-oracle-%d-%d.p" % (config["ds"],
                        fname, args.q, args.k, args.method, args.alpha, args.gamma, args.lag), "wb"))
        else:
            pickle.dump(schedule, open(
                "resources/schedule/random/%s-%s-%s-%d-%s-%d-%.2f-%d-%d.p" % (config["ds"],
                fname, args.q, args.k, args.method, args.alpha, args.eps, args.gamma, args.lag), "wb"))
    print("[Random (%s,%d)] Query: %f, Movement: %f" % (
        args.policy, args.interval, total_query / total_size, total_movement / total_size))
    print("Total size: %d" % total_size)