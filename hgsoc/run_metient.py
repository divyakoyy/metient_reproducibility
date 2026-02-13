import sys
import os
import argparse
import shutil
from metient import metient as met

MSK_MET_FREQ_FILE = '/data/morrisq/divyak/projects/metient/data/msk_met/msk_met_freq_by_cancer_type.csv'

MAPPINGS = [
	# Patient 1
	{
		'Right Ovary':'Ovary',
		'Left Ovary':'Ovary',
		'Left Fallopian Tube':'Female Genital',
		'Right Fallopian Tube':'Female Genital',
		'Omentum':'Intra-Abdominal',
		'Appendix':'Bowel',
		'Small Bowel':'Bowel',
	},
	# Patient 2
	{
		'Omentum':'Intra-Abdominal',
	},
	# Patient 3
	{
		'Right Ovary':'Ovary',
		'Left Ovary':'Ovary',
		'Adnexa':'Female Genital',
		'Cul de Sac':'Intra-Abdominal',
		'Left Fallopian Tube Fimbriae':'Female Genital',
		'Omentum':'Intra-Abdominal',
		'Right Fallopian Tube':'Female Genital',
		'Sigmoid Colon Deposit':'Bowel',
	},
	# Patient 4
	{
		'Left Ovary Surface':'Ovary',
		'Right Ovary':'Ovary',
		'Left Pelvic Sidewall':'Bone',
		'Right Pelvic Sidewall':'Bone',
	},
	# Patient 7
	{
		'Right Ovary':'Ovary',
		'Left Ovary':'Ovary',
		'Right Uterosacral':'Unspecified', 
		'Bowel Implant':'Bowel',
		'Brain Metastasis':'CNS/Brain',
		'Righ Pelvic Mass':'Distant LN',
	},
	# Patient 9
	{
		'Right Ovary':'Ovary',
		'Left Ovary':'Ovary',
		'Omentum':'Intra-Abdominal',
	},
	# Patient 10
	{
		'Left Fallopian Tube':'Female Genital',
		'Omentum':'Intra-Abdominal',
	}
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
    ovarian_freq = met_freq_df[met_freq_df['Cancer Type'] == 'Ovarian Cancer']


    # Get frequencies for our site categories
    O_by_patient = []
    for mapping in site_mappings:
        O = {}
        for mcpherson_site, msk_site in mapping.items():
            freq = float(ovarian_freq[msk_site].iloc[0])
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
     
	MCPHERSON_DATA_DIR = './metient_inputs'
	
	PATIENT_IDS = [1,2,3,4,7,9,10]
	Os = get_metastasis_frequencies(MAPPINGS, MSK_MET_FREQ_FILE)

	mut_trees_fns = [os.path.join(MCPHERSON_DATA_DIR, f"patient{patient_id}_tree.txt") for patient_id in PATIENT_IDS]
	ref_var_fns = [os.path.join(MCPHERSON_DATA_DIR, f"patient{patient_id}_SNVs.tsv") for patient_id in PATIENT_IDS]
	run_names = [f"{pid}_calibrate" for pid in PATIENT_IDS]
     
	print_config = met.PrintConfig(visualize=True, verbose=False, k_best_trees=100)
	met.calibrate_label_clone_tree(mut_trees_fns, ref_var_fns, print_config, args.output_dir, run_names, args.calibration_type,
                                   Os=Os, sample_size=args.bs, solve_polytomies=args.solve_polys, num_runs=args.num_runs)