# Python scripts for running GraphChainer experiments

- Use same conda enviroment as GraphChainer's
- Modify `.env` file with the following variables `GRAPHALIGNER`, `GRAPHCHAINER`, `MINIGRAPH`, `MINICHAIN` (paths to the corresponding binaries)
- Place Badread's repo in this directory `git clone https://github.com/rrwick/Badread.git`

## Some instructions

- Every python script has its own instructions/helper
- The scripts should be run in the order `[generate_sim_reads.py], run_experiment.py, compute_summary.py, compute_metrics.py`
