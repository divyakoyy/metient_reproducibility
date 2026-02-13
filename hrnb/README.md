### To run Metient on HR-NB dataset:
bsub -n 8 -W 48:00 -R rusage[mem=16GB] -o output_hrnb_trees.log -e error_hrnb_trees.log python run_metient.py ./metient_outputs --bs 8192 --num_runs 100 --solve_polys True

Inputs for Metient are in metient_inputs and outputs are in metient_outputs. Note: figures in metient_outputs only show top 10 solutions.
