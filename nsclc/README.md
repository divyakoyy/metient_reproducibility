### To run Metient on NSCLC dataset:
bsub -q gpuqueue -gpu "num=1" -R A100 -n 16 -W 100:00 -R "rusage[mem=16GB]" -o output_tracerx_trees.log -e error_tracerx_trees.log python run_metient.py ./metient_outputs --bs 8192 --num_runs 100 --solve_polys True

`sample_overview_original.txt` downloaded and then processed from https://zenodo.org/records/7649257
`seedingTable.txt` downloaded from https://zenodo.org/records/7649257
`timingTable.txt` downloaded from https://zenodo.org/records/7649257