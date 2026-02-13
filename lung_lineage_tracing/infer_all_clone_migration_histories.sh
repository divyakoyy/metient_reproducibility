#!/bin/bash

# Check if a directory argument was passed
if [ $# -lt 1 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

directory_str="$1"

# Loop through .tsv files in the directory
for file in ./metient_inputs/*.tsv; do
    # Get the filename without extension
    clone=$(basename "$file" .tsv)

    echo "Running Metient on clone $clone"
    
    # Different resource requirements for clones 1, 2, 3
    if [[ "$clone" == "1" || "$clone" == "2" || "$clone" == "3" ]]; then
        bsub -q gpuqueue -gpu "num=1" -R A100 -n 16 -W 24:00 -R "rusage[mem=16GB]" \
        -J "lt_${clone}" -o "logs/output_${clone}_${directory_str}.log" -e "logs/error_${clone}_${directory_str}.log" \
        "python infer_single_clone_migration_history.py $clone $directory_str"
    else
        # Default command for other clones
        bsub -q gpuqueue -gpu "num=1" -R A100 -n 8 -W 10:00 -R "rusage[mem=16GB]" \
        -J "lt_${clone}" -o "logs/output_${clone}_${directory_str}.log" -e "logs/error_${clone}_${directory_str}.log" \
        "python infer_single_clone_migration_history.py $clone $directory_str"
    fi
done
