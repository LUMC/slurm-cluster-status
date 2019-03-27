slurm-snakemake
===============

Little tool to be used as argument to Snakemake's `--cluster-status` 
argument in a SLURM setting.

Input _must_ be the batch ID.

Output will be a string that is either:

1. running
2. success
3. failed

  

