import sys
import os
import argparse
import shutil
from metient import metient as met
from metient.util import pairtree_data_extraction_util as ptutil


MSK_MET_FREQ_FILE = '/data/morrisq/divyak/projects/metient/metient/data/msk_met/msk_met_freq_by_cancer_type.csv'

MAPPINGS = [
	# Patient A
	{
		'Parotid metastasis':'Head and Neck',
		'Locoregional skin metastasis 1, forehead':'Skin',
		'Locoregional skin metastasis 2, angle jaw':'Skin',
	},
	# Patient B
	{
		'Lymph node metastasis, left axilla':'Distant LN',
		'Locoregional skin metastasis 1, left back':'Skin',
		'Locoregional skin metastasis 2, left axilla':'Skin',
	},
	# Patient C
	{
		'Locoregional skin metastasis 1, right calf':'Skin',
		'Locoregional skin metastasis 2, right mid-calf':'Skin',
	},
	# Patient D
	{
		'Locoregional skin metastasis 1, right ankle':'Skin',
		'Locoregional skin metastasis 2, right leg':'Skin',
		'Lymph node metastasis, right groin':'Distant LN',
	},
	# Patient E
	{
		'Locoregional skin metastasis 1, left heel':'Skin',
		'Locoregional skin metastasis 2, left heel':'Skin',
		'Locoregional skin metastasis 3, left heel':'Skin',
		'Lymph node metastasis, left groin':'Distant LN',
	},
	# Patient F
	{
		'Locoregional skin metastasis, left ear':'Skin',
		'Distant skin metastasis, back':'Skin',
		'Lymph node metastasis, left cervical node':'Distant LN',
	},
	# Patient G
	{
		'Lung metastasis':'Lung',
		'Locoregional skin metastasis, axilla':'Skin',
	},
]
import pandas as pd

def get_metastasis_frequencies(site_mappings, met_freq_file):
    """
    Get normalized metastasis frequencies for each anatomical site from MSK data
    
    Args:
        site_mappings: List of dictionaries mapping sample sites to standardized categories
        met_freq_file: Path to CSV file containing metastasis frequencies
        
    Returns:
        List of dictionaries containing normalized frequencies for each patient's sites
    """
    # Read metastasis frequency data
    met_freq_df = pd.read_csv(met_freq_file)
    melanoma_freq = met_freq_df[met_freq_df['Cancer Type'] == 'Melanoma']

    # Get frequencies for our site categories
    O_by_patient = []
    for mapping in site_mappings:
        O = {}
        for mcpherson_site, msk_site in mapping.items():
            freq = float(melanoma_freq[msk_site].iloc[0])
            O[mcpherson_site] = freq
			
        # Normalize frequencies
        total = sum(O.values())
        print("\n",O)
        if total > 0:
            O = {k:v/total for k,v in O.items()}
        print(O)
        O_by_patient.append(O)
        
    return O_by_patient

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
	parser.add_argument('--calibration_type', type=str, required=True, 
	                   choices=['genetic', 'organotropism', 'both'],
	                   help='Type of calibration to perform')

	args = parser.parse_args()

	create_directory(args.output_dir)
	sys.stdout = open(os.path.join(args.output_dir, f"output.txt"), 'a')
     
	SANBORN_DATA_DIR = './metient_inputs'
	
	PATIENT_IDS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

	TREE_DIR = os.path.join(SANBORN_DATA_DIR, 'pyclone_vi_orchard_trees')    
	TSV_DIR = os.path.join(SANBORN_DATA_DIR, 'pyclone_vi_orchard_eta_clustered_tsvs')  

	Os = get_metastasis_frequencies(MAPPINGS, MSK_MET_FREQ_FILE)
	print(Os)
	
	mut_trees_fns = [os.path.join(TREE_DIR, f"{patient_id}.results.npz") for patient_id in PATIENT_IDS]
	trees = [data[0] for data in ptutil.get_adj_matrices_from_pairtree_results(mut_trees_fns)]
	ref_var_fns = [os.path.join(TSV_DIR, f"{patient_id}_SNVs.tsv") for patient_id in PATIENT_IDS]
	run_names = [f"{pid}_calibrate" for pid in PATIENT_IDS]
     
	print_config = met.PrintConfig(visualize=True, verbose=False, k_best_trees=100)
	met.calibrate_label_clone_tree(trees, ref_var_fns, print_config, args.output_dir, run_names, args.calibration_type,
                                   Os=Os, sample_size=args.bs, solve_polytomies=args.solve_polys, num_runs=args.num_runs)