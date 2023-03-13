# Python scripts for running GraphChainer experiments

- - Install [miniconda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
- `conda env create -f environment.yml`
- `conda acctivate GraphChainerScripts`
- Compile and place the aligner's binaries on the `bin/` folder (they are assumed to be called `GraphAligner, GraphChainer, minigraph, minichain` respectively)
- Place Badread's repo in this directory `git clone https://github.com/rrwick/Badread.git`

## Instructions

- Every python script has its own instructions/helper
- The scripts should be run in the order `[generate_sim_reads.py], run_experiment.py, compute_summary.py, compute_metrics.py` (if real reads are used the first script is skipped)
-- `generate_sim_reads.py` : Takes a graph as input and generates simulated reads from a random path of the graph using `GraphChainer` random path generator and `Bardread` simulator.
-- `run_experiment.py` : Runs the four tools on the specified graph and fastq files.
-- `compute_summary.py` : Computes csv tables with the metrics used in the paper, it receives as input the graph and the fastq file, or in the case of simulated reads, the files output by `generate_sim_reads.py`.
-- `compute_metrics.py` : Plots a graph with the summary (csv) files output by `compute_sumary.py` 
