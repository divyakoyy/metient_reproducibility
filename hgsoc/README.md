### To run Metient on HGSOC dataset, calibrating to genetic distance and organotropism:
bsub -n 8 -W 24:00 -R rusage[mem=8GB] -o output_hgsoc_trees.log -e error_hgsoc_trees.log python run_metient.py ./genetic_organotrop_calibration --bs 8192 --num_runs 100 --solve_polys True --calibration_type both

### To run Metient on HGSOC dataset, calibrating to genetic distance only:
bsub -n 8 -W 24:00 -R rusage[mem=8GB] -o output_hgsoc_trees.log -e error_hgsoc_trees.log python run_metient.py ./genetic_calibration --bs 8192 --num_runs 100 --solve_polys True --calibration_type genetic

### To run Metient on HGSOC dataset, calibrating to organotropism only:
bsub -n 8 -W 24:00 -R rusage[mem=8GB] -o output_hgsoc_trees.log -e error_hgsoc_trees.log python run_metient.py ./organotrop_calibration --bs 8192 --num_runs 100 --solve_polys True --calibration_type organotropism

Inputs for Metient are in metient_inputs and outputs are in metient_outputs.