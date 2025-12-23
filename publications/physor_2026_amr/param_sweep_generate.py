#!/bin/python3
import os
import shutil
from argparse import ArgumentParser

from param_sweep_common import *

# Map the short name of the algorithms to their include path.
ALGORITHM_PATH = '../../../../amr_strategies/'
INCLUDE_MAP = {
  'cj' : f'!include {ALGORITHM_PATH}current_jump_rel_error.i',
  'cj_lh' : f'!include {ALGORITHM_PATH}current_jump_lh.i',
  'inv_od' : f'!include {ALGORITHM_PATH}opt_depth_rel_error.i',
  'inv_od_lh' : f'!include {ALGORITHM_PATH}opt_depth_lh.i',
  'vj' : f'!include {ALGORITHM_PATH}value_jump_rel_error.i',
  'vj_lh' : f'!include {ALGORITHM_PATH}value_jump_lh.i'
}

# The include path for the input file that runs OpenMC
BASE_INPUT_FILE_INCLUDE = '!include ../../openmc.i'

# Check if a directory exists. If not, make it.
def check_make_dir(dir):
  if not os.path.isdir(dir):
    os.makedirs(dir)

# Generate the parameter sweep for a case.
def gen_sweep(case):
  # Change into the case directory.
  os.chdir(f'./{case}')

  # Generate the required model.xml
  if not os.path.isfile('./model.xml'):
    os.system(f'python {case}_slab_model.py')

  # Use Cardinal to generate the meshes
  if not os.path.isfile(f'./{case}_mesh_in.e'):
    if os.system(f'cardinal-opt -i {case}_mesh.i --mesh-only'):
      print('Cardinal failed to execute!')
      exit(1)
  if not os.path.isfile(f'./{case}_mesh_ref_in.e'):
    if os.system(f'cardinal-opt -i {case}_mesh_ref.i --mesh-only'):
      print('Cardinal failed to execute!')
      exit(1)

  # Generate the refined reference input file
  check_make_dir('reference')
  with open('reference/openmc_ref.i', 'w') as inp:
    # Write the include for the OpenMC part of the input file
    inp.write(f'{BASE_INPUT_FILE_INCLUDE}\n')
    # Write the parameter overrides
    overrides =  '[Mesh/file]\n' \
                f'\tfile := ../{case}_mesh_ref_in.e\n' \
                 '[]\n' \
                 '[Problem]\n' \
                 '\tparticles := 100000\n' \
                 '\tbatches := 10100\n' \
                 '\tinactive_batches := 100\n' \
                 '\txml_directory := ../\n' \
                 '[]\n' \
                 '[MultiApps/post_process]\n' \
                 '\tinput_files := ../post_process.i\n' \
                 '[]\n'
    inp.write(overrides)

  # Generate the parameter sweep input files.
  for alg in ALGORITHMS:
    for b in BATCHES:
      dir = f'{alg}_{str(b[1] - b[0])}'
      check_make_dir(dir)
      for frac in REFINEMET_FRAC:
        fname = f'frac_0{frac}'
        with open(f'{dir}/{fname}.i', 'w') as inp:
          # Write the include for the AMR algorithm
          inp.write(f'{INCLUDE_MAP[alg]}\n')

          # Write the include for the OpenMC part of the input file
          inp.write(f'{BASE_INPUT_FILE_INCLUDE}\n')

          # Write the parameter overrides for the different parts of the parameter sweep
          overrides = f'R_ERROR_FRACTION := {str(float(frac) / 10.0)}\n' \
                       '[Mesh/file]\n' \
                      f'\tfile := ../{case}_mesh_in.e\n' \
                       '[]\n' \
                       '[Problem]\n' \
                      f'\tbatches := {b[1]}\n' \
                      f'\tinactive_batches := {b[0]}\n' \
                       '\txml_directory := ../\n' \
                       '[]\n' \
                       '[Adaptivity]\n' \
                      f'\tmax_h_level := 5\n' \
                       '[]\n' \
                       '[MultiApps/post_process]\n' \
                       '\tinput_files := ../post_process.i\n' \
                       '[]\n' \
                       '[Outputs]\n' \
                      f'\tfile_base := {fname}\n' \
                       '[]\n'
          inp.write(overrides)
  # Back out of the case directory.
  os.chdir('../')

def main():
  ap = ArgumentParser(description='PHYSOR 2026 AMR parameter sweep generator.')
  ap.add_argument('case', type=str, help='The particular case to generate. Must be one of either lwr or sfr.')
  args = ap.parse_args()

  if args.case != 'lwr' and args.case != 'sfr':
    raise Exception('case must be either lwr or sfr!')

  # Make sure Cardinal exists in the system path.
  if not shutil.which('cardinal-opt'):
    raise Exception('cardinal-opt could not be found! ' \
                    'To run this script, Cardinal must be available on your system PATH.')

  gen_sweep(args.case)

if __name__ == "__main__":
  main()
