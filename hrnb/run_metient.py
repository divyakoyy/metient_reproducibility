import sys
import os
import argparse
import shutil
from metient import metient as met
from metient.util import pairtree_data_extraction_util as ptutil

def create_directory(directory_path):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)    
    os.makedirs(directory_path)

if __name__=="__main__":
	
	parser = argparse.ArgumentParser()

	parser.add_argument('output_dir', type=str)
	parser.add_argument('--bs', type=int,default=-1)
	parser.add_argument('--num_runs', type=int,default=1)
	parser.add_argument('--solve_polys', type=bool,default=True)

	args = parser.parse_args()

	create_directory(args.output_dir)
	sys.stdout = open(os.path.join(args.output_dir, f"output.txt"), 'a')

	DATA_DIR = './metient_inputs/'
	TREE_DIR = os.path.join(DATA_DIR, 'orchard_trees')    

	TSV_DIR = os.path.join(DATA_DIR, 'orchard_eta_clustered_tsvs')                 
	patient_ids = [x.replace("_SNVs.tsv", "") for x in os.listdir(TSV_DIR)]

	print(patient_ids)
	len(patient_ids)
     
	mut_trees_fns = [os.path.join(TREE_DIR, f"{patient_id}.results.npz") for patient_id in patient_ids]
	trees = [data[0] for data in ptutil.get_adj_matrices_from_pairtree_results(mut_trees_fns)]
	ref_var_fns = [os.path.join(TSV_DIR, f"{patient_id}_SNVs.tsv") for patient_id in patient_ids]
	run_names = [f"{pid}_calibrate" for pid in patient_ids]

	print_config = met.PrintConfig(visualize=True, verbose=False, k_best_trees=100)
	met.calibrate_label_clone_tree(trees, ref_var_fns, print_config, args.output_dir, run_names, "genetic",
                                   sample_size=args.bs, solve_polytomies=args.solve_polys, num_runs=args.num_runs)