# PHYSOR 2026 AMR

This directory contains the input files and helper scripts necessary to reproduce the results in the following paper: K. C. Sawatzky *et al*., “Mesh Tally Adaptive
Mesh Refinement Strategies for Spatial Gradients Driven by Material
Heterogeneities”, in *Proceedings of PHYSOR 2026*, Turin, Italy.

To reproduce the results and figures from the paper, perform the following series of steps:

1. Run the parameter sweep generator script: `./param_sweep_generate.py CASE`, where `CASE` is either `lwr` or `sfr`. This will generate a series of Cardinal input files, each of these scripts is a single data point in the parameter sweep from the PHYSOR paper. This script assumes that `cardinal-opt` is available on your system path and you have installed the OpenMC python API.
2. Run the parameter sweep with the provided helper script:
`./param_sweep_run.py CASE --ranks RANKS --threads THREADS`, where `CASE` is either `lwr` or `sfr`, `RANKS` is the number of MPI ranks to use when running Cardinal, and `THREADS` is the number of OpenMP threads to use when running Cardinal. This script assumes that `cardinal-opt` is available on your system path and you have installed the OpenMC python API. Please note that this script is not guaranteed to work in a distributed memory computing environment
3. (Optional) Run the post-processing script to obtain the figures from the paper: `./param_sweep_pp.py CASE`, where `CASE` is either `lwr` or `sfr`.
