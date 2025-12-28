from utils.setup import *
from utils.tree import *
from utils.config import *
from offline.states import *
from online.counter import *
import numpy as np
import argparse
import os
import pickle

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Gap to optimal comparison.')
    parser.add_argument('--config', default="demo", help="Config File Path")
    parser.add_argument('--k', type=int, default=None, help="Override partition count k")
    
    parsed_args = parser.parse_args()
    args = Args(parsed_args.config)

    if parsed_args.k is not None:
        args.k = parsed_args.k

    args.set_policy('sw,oracle')

    fnames, files, parts, config = setup_perfile(args)
    queries = get_workload_perfile(config, files, fnames, args)
   
    for i, fname in enumerate(fnames):
        print(f"\n{'='*60}")
        print(f"PROCESSING: {fname} (Fair Mode: Interval Loop)")
        print(f"{'='*60}")

        df, df_sample, _ = get_data(config, args, parts, files[i], fname)
        k = args.k 
    
        output_dir_name = "%s/%s-%s-%d-%d-%s" % (
            config["ds"], fname, args.q, args.interval, k, args.method)
            
        tb = TreeBuilder(df, df_sample, config, args, k, output_dir_name)

        schedule = {}

        results_path = "resources/schedule/oracle/%s-%s-40.p" % (config["ds"], args.q)
        try:
            results = pickle.load(open(results_path, "rb"))
        except: results = {}

        query = []
        reorg = []
        
        print(f"Oracle/interval {args.interval}...")

        T = len(queries) // args.interval
        
        for j in range(T):
            qs = queries[j * args.interval : (j + 1) * args.interval]
            
            reorg.append(j)

            base_folder = "resources/labels/sw"

            folder_name = "%s/%s-%s-%d-%d-%s" % (
                config["ds"], fname, args.q, args.interval, k, args.method)
            
            full_path = f"{base_folder}/{folder_name}/{j}.p"
 
            if not os.path.exists(full_path) and j > 0:
                 full_path = f"{base_folder}/{folder_name}/{j-1}.p"

            try:
                if os.path.exists(full_path):
                    tree = tb.load_by_path(full_path)
                    read, _ = tree.eval(qs, avg=False)
                    query.extend(list(read))
                else:
                    print(f"Missing Layout: {full_path}")
            except Exception as e:
                print(f"Error loading {full_path}: {e}")
                break

        total_reorg_cost = len(reorg) * args.alpha
        total_query_cost = sum(query)
        
        print(f"Oracle Result -> Query: {total_query_cost:.2f}, Movement: {total_reorg_cost}")

        results["online"] = [query, reorg]
        pickle.dump(results, open(results_path, "wb"))
        print("OREO saved.")