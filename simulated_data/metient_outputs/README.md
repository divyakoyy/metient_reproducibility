T

### To run Metient-calibrate on simulated data from MACHINA:

With solving polytomies
bsub -n 8 -W 40:00 -R 'rusage[mem=8] span[hosts=1]' -o output_calibrate_solvepoly.log -e error_calibrate_solvepoly.log python predict_all_simulated_trees_calibrate.py ./machina_sims/ calibrate_solvepoly --gen 1.0 --solve_polys --bs 1024 --wip; 

Without solving polytomies
bsub -n 8 -W 40:00 -R 'rusage[mem=8] span[hosts=1]' -o output_calibrate.log -e error_calibrate.log python predict_all_simulated_trees_calibrate.py ./machina_sims/ calibrate --gen 1.0  --bs 1024 --wip; 

### To run Metient-evaluate on simulated data from MACHINA:

python predict_all_simulated_trees_evaluate.py ./machina_sims/ evaluate_solvepoly --gen 0.0 --solve_polys --bs 1024 --wip; python predict_all_simulated_trees_evaluate.py ./machina_sims/ evaluate --gen 0.0 --bs 1024 --wip; 

python predict_all_simulated_trees_evaluate.py ./machina_sims/ evaluate_solvepoly_gd_only --gen 1.0 --mig 0 --comig 0 --seed 0  --solve_polys --bs 1024 --wip; python predict_all_simulated_trees_evaluate.py ./machina_sims/ evaluate_gd_only --gen 1.0 --mig 0 --comig 0 --seed 0 --bs 1024 --wip;

### To run machina:

export GRB_LICENSE_KEY="/home/koyyald/gurobi.lic"
export GRB_LICENSE_FILE="/home/koyyald/gurobi.lic"
export LD_LIBRARY_PATH=/lila/home/koyyald/mambaforge/envs/machina/lib/libstdc++.so.6:$LD_LIBRARY_PATH
export LD_PRELOAD=/lila/home/koyyald/mambaforge/envs/machina/lib/libstdc++.so.6
./machina_pmh_ti_timing.sh /data/morrisq/divyak/machina-linux-binaries/pmh_ti ../../../../machina/data/sims/ ./machina_sims/
