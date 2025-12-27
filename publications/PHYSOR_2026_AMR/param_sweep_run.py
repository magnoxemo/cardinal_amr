#!/bin/python3
import os
import shutil
from argparse import ArgumentParser

from param_sweep_common import *

def run_in_dir(dir, file, ranks, threads):
  old_dir = os.getcwd()
  # Change into the directory.
  os.chdir(dir)

  # Build the command.
  cmd = ''
  if ranks > 1:
    cmd += f'mpiexec -np {ranks} '
  cmd += f'cardinal-opt -i {file}'
  if threads > 1:
    cmd +=  f' --n-threads={threads}'

  # Run Cardinal for the given input file.
  if os.system(cmd):
    print('Cardinal failed to execute!')
    exit(1)
  # Go back to the previous directory.
  os.chdir(old_dir)


def run_sweep(case, ranks, threads):
  # Change into the case directory.
  os.chdir(f'./{case}')

  # Run the reference first.
  run_in_dir('./reference', 'openmc_ref.i', ranks, threads)

  # Then, run the parameter sweep.
  for alg in ALGORITHMS:
    for b in BATCHES:
      dir = f'./{alg}_{str(b[1] - b[0])}'
      for frac in REFINEMET_FRAC:
        fname = f'frac_0{frac}.i'
        run_in_dir(dir, fname, ranks, threads)


def main():
  ap = ArgumentParser(description='PHYSOR 2026 AMR parameter sweep runner. This script runs Cardinal for each ' \
                      'datapoint in the paper. Note: this script is not guaranteed to be safe in distributed ' \
                      'memory computing environments, use at your own risk!')
  ap.add_argument('case', type=str, help='The particular case to generate. Must be one of either lwr or sfr.')
  ap.add_argument('--ranks', dest='ranks', type=int, default=1,
                  help='Number of MPI ranks to use when running the parameter sweep')
  ap.add_argument('--threads', dest='threads', type=int, default=1,
                  help='Number of OpenMP threads to use when running the parameter sweep')
  args = ap.parse_args()

  # Make sure Cardinal exists in the system path.
  if not shutil.which('cardinal-opt'):
    raise Exception('cardinal-opt could not be found! ' \
                    'To run this script, Cardinal must be available on your system PATH.')

  # Make sure the parameter sweep input files have been generated.
  if not os.path.isdir(f'./{args.case}/reference'):
    raise Exception('Parameter sweep input files have not been generated! Please run ' \
                    f'param_sweep_generate.py {args.case} before running this script!')

  run_sweep(args.case, args.ranks, args.threads)

if __name__ == "__main__":
  main()
