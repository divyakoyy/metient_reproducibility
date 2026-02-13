import sys
import os
import argparse
import seaborn as sns
import pandas as pd
import torch
import glob
import shutil
import matplotlib.pyplot as plt
from metient import metient as met
from metient.util import data_extraction_util as data_util

def create_directory(directory_path):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)    
    os.makedirs(directory_path)

def get_matching_basenames(directory, pattern, suffix):
    file_paths = glob.glob(os.path.join(directory, pattern))
    basenames = [os.path.basename(file_path).replace(suffix, "") for file_path in file_paths]
    return basenames

if __name__=="__main__":
	
	parser = argparse.ArgumentParser(description='run metient on conipher generated trees')

	parser.add_argument('output_dir', type=str)
	parser.add_argument('--bs', type=int,default=-1)
	parser.add_argument('--num_runs', type=int,default=1)
	parser.add_argument('--solve_polys', type=bool,default=True)

	args = parser.parse_args()

	create_directory(args.output_dir)
	sys.stdout = open(os.path.join(args.output_dir, f"output.txt"), 'a')
	tsv_dir = './metient_inputs/'
	patients = get_matching_basenames(tsv_dir, "*_SNVs.tsv", "_SNVs.tsv")
	print(f"{len(patients)} patients")
	print(f"solve_polytomies: {args.solve_polys}")
	print(f"Batch size: {args.bs}")
	# Collect all data
	trees, ref_var_fns, run_names = [],[],[]
	for patient in patients:
		print(patient)
		df = pd.read_csv(os.path.join(tsv_dir, f"{patient}_SNVs.tsv"), sep="\t", index_col=False)
		print(df['site_category'].unique())
		ref_var_fns.append(os.path.join(tsv_dir, f"{patient}_SNVs.tsv"))
		tree_fn = os.path.join(tsv_dir, f"{patient}_tree.txt")
		trees.append(data_util.get_adjacency_matrix_from_txt_edge_list(tree_fn))
		run_names.append(patient)

	print_config = met.PrintConfig(visualize=True, verbose=False, k_best_trees=100)
	met.calibrate_label_clone_tree(trees, ref_var_fns, print_config, args.output_dir, run_names, "genetic",
				  				   sample_size=args.bs, solve_polytomies=args.solve_polys, num_runs=args.num_runs)

