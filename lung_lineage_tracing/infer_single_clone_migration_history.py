import os
from metient import *
import argparse
from datetime import datetime
import json
import pandas as pd

SAMPLE_SIZE = 2048
NUM_RUNS = 200
USE_ORGANO = True
SOLVE_POLYS = False

TISSUE_ORDER = ['LL',"RE","RW","M1","M2","Liv"]
TISSUE_COLORS = ["#6aa84f","#c27ba0","#bf4040", "#6fa8dc", "#e69138", "#9e9e9e"]
TISSUE_COLOR_MAP = dict(zip(TISSUE_ORDER, TISSUE_COLORS))

def count_nodes_from_edges(file_path):
    nodes = set()

    with open(file_path, 'r') as file:
        for line in file:
            node1, node2 = map(int, line.split())
            nodes.update([node1, node2])
    return len(nodes)

def get_color_list(tsv_fn):
    df = pd.read_csv(tsv_fn, sep='\t')
    index_to_tissue_map = dict(zip(df['anatomical_site_index'], df['anatomical_site_label']))
    color_list = [TISSUE_COLOR_MAP[index_to_tissue_map[i]] for i in index_to_tissue_map]
    return color_list

if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('clone_num', type=int, help="sclineage tracing data clone number")
    parser.add_argument('output_dir', type=str, help="output dir")
    parser.add_argument('-ss', '--samplesize', type=int, default=SAMPLE_SIZE, help=f'Number of samples (default: {SAMPLE_SIZE})')
    parser.add_argument('-r', '--runs',type=int, default=NUM_RUNS, help=f'Number of iterations (default: {NUM_RUNS})')
    
    args = parser.parse_args()
    input_dir = "./metient_inputs/"

    clone = args.clone_num
    output_dir = os.path.join("./metient_outputs/", args.output_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    tree_fn = os.path.join(input_dir, f"{clone}_tree.txt")
    tsv_fn = os.path.join(input_dir, f"{clone}.tsv")

    num_nodes = count_nodes_from_edges(tree_fn)

    O = None

    weights = Weights.pancancer_genetic_uniform_weighting()
    if USE_ORGANO:
        organotropism_frequencies = "./metient_inputs/quinn2021_m5k_organotropism.json"
        with open(organotropism_frequencies, 'r') as json_file:
            O = json.load(json_file)
            weights.organotrop = 0.001

    if num_nodes < 300:
        color_list = get_color_list(tsv_fn)
        print_config = PrintConfig(custom_colors=color_list)
    else:
        print_config = PrintConfig(visualize=False)

    print("Sample size", args.samplesize, "Num runs", args.runs, "Visualize", print_config.visualize)
    
    clone_to_sample_size = {x: args.samplesize for x in range(1, 101)}
    clone_to_num_runs = {x: args.runs for x in range(1, 101)}
    # Update specific clones with custom values
    clone_to_sample_size.update({1: 256, 2: 256, 3: 256, 4: 256, 5: 256})

    evaluate_label_clone_tree(tree_fn, tsv_fn, weights, print_config, output_dir, clone, O=O,
                              solve_polytomies=SOLVE_POLYS, sample_size=clone_to_sample_size[clone], 
                              num_runs=clone_to_num_runs[clone])
