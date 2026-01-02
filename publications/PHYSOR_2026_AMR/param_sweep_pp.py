#!/bin/python3
import os
from argparse import ArgumentParser
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# Plotting parameters
DEFAULT_FONT_SIZE = 12
LARGE_FONT_SIZE = 18

ALPHA = 0.7

AZIMUTHAL = 120.0
ELEVATION = 30.0

SIZE_3D_W = 12
SIZE_3D_H = 12

FIG_3D_FONT_SIZE = 22

SIZE_L2_W = 8
SIZE_L2_H = 6

# Dictionaries which map between shorthand and meaningful names.
ALG_NAMES = {
  'cj' : 'Current Jump',
  'cj_lh' : 'Current Jump (LH)',
  'inv_od' : 'Inverse OD',
  'inv_od_lh' : 'Inverse OD (LH)',
  'vj' : 'Value Jump',
  'vj_lh' : 'Value Jump (LH)'
}
ALG_COLOURS = {
  'cj' : 'tab:red',
  'cj_lh' : 'tab:red',
  'inv_od' : 'tab:green',
  'inv_od_lh' : 'tab:green',
  'vj' : 'tab:blue',
  'vj_lh' : 'tab:blue'
}
AXES_LABELS = {
  'Flux_X_Avg_Out' : 'Y-Z Averaged Flux (cm$^{-2}$ s$^{-1}$)',
  'Heating_X_Avg_Out' : 'Y-Z Averaged Heating (W cm$^{-3}$)',
  'Flux_X_Int_Out' : 'Y-Z Integrated Flux (s$^{-1}$)',
  'Heating_X_Int_Out' : 'Y-Z Integrated Heating (W cm$^{-1}$)'
}

# Unchanging GLOBAL variables.
NUM_PINS = {
  'sfr' : 8,
  'lwr' : 10
}
INIT_X_LAYER_BNDS = {
  'sfr' : [0.0,  0.5,  0.6,  0.9,  1.0,  2.0,  2.1,  2.4,  2.5,
           3.5,  3.6,  3.9,  4.0,  5.0,  5.1,  5.4,  5.5,  6.5,
           6.6,  6.9,  7.0,  8.0,  8.1,  8.4,  8.5,  9.5,  9.6,
           9.9,  10.0, 11.0, 11.1, 11.4, 11.5, 12.0],
  'lwr' : [0.0,  0.5,  0.6,  0.9,  1.0,  2.0,  2.1,  2.4,  2.5,
           3.5,  3.6,  3.9,  4.0,  5.0,  5.1,  5.4,  5.5,  6.5,
           6.6,  6.9,  7.0,  8.0,  8.1,  8.4,  8.5,  9.5,  9.6,
           9.9,  10.0, 11.0, 11.1, 11.4, 11.5, 12.5, 12.6, 12.9,
           13.0, 14.0, 14.1, 14.4, 14.5, 15.0]
}

CYCLES = 10
CYCLE_POINTS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
LINE_DATA = ['Flux_X_Avg_Out', 'Heating_X_Avg_Out', 'Flux_X_Int_Out', 'Heating_X_Int_Out']
BATCH_COUNT = [100, 1000]
ALGORITHMS  = ['cj', 'cj_lh', 'inv_od', 'inv_od_lh', 'vj', 'vj_lh']
REF_FRAC = ['01', '02', '03', '04', '05']

# Set default plotting settings.
plt.rcParams.update({'font.size': DEFAULT_FONT_SIZE})
plt.rcParams.update({'text.usetex': True})

# Helper functions.
## A function to return the indices corresponding to fuel locations.
def idx_mask_fuel(case, plot_half):
  if case == 'lwr':
    return mask_lwr(plot_half)
  else:
    return mask_sfr(plot_half)

## Masking the LWR case.
def mask_lwr(plot_half):
  bnds = make_refined_bnds('lwr')
  m = []
  m.append(np.intersect1d(np.where(bnds > 0.0),  np.where(bnds < 0.5)))
  m.append(np.intersect1d(np.where(bnds > 1.0),  np.where(bnds < 2.0)))
  m.append(np.intersect1d(np.where(bnds > 4.0),  np.where(bnds < 5.0)))
  m.append(np.intersect1d(np.where(bnds > 5.5),  np.where(bnds < 6.5)))
  if plot_half:
    return m
  m.append(np.intersect1d(np.where(bnds > 8.5),  np.where(bnds < 9.5)))
  m.append(np.intersect1d(np.where(bnds > 10.0), np.where(bnds < 11.0)))
  m.append(np.intersect1d(np.where(bnds > 13.0), np.where(bnds < 14.0)))
  m.append(np.intersect1d(np.where(bnds > 14.5), np.where(bnds < 15.0)))

  return m

## Masking the SFR case.
def mask_sfr(plot_half):
  bnds = make_refined_bnds('sfr')
  m = []
  m.append(np.intersect1d(np.where(bnds > 0.0),  np.where(bnds < 0.5)))
  m.append(np.intersect1d(np.where(bnds > 1.0),  np.where(bnds < 2.0)))
  m.append(np.intersect1d(np.where(bnds > 2.5),  np.where(bnds < 3.5)))
  m.append(np.intersect1d(np.where(bnds > 4.0),  np.where(bnds < 5.0)))
  if plot_half:
    m.append(np.intersect1d(np.where(bnds > 5.5),  np.where(bnds < 6.0)))
    return m
  m.append(np.intersect1d(np.where(bnds > 5.5),  np.where(bnds < 6.5)))
  m.append(np.intersect1d(np.where(bnds > 7.0),  np.where(bnds < 8.0)))
  m.append(np.intersect1d(np.where(bnds > 8.5),  np.where(bnds < 9.5)))
  m.append(np.intersect1d(np.where(bnds > 10.0), np.where(bnds < 11.0)))
  m.append(np.intersect1d(np.where(bnds > 11.5), np.where(bnds < 12.0)))

  return m

## A function to refine the boundaries.
def make_refined_bnds(case):
  MAX_H = 5
  bounds = INIT_X_LAYER_BNDS[case]
  for i in range(MAX_H):
    bnds = []
    for j in range(len(bounds) - 1):
      bnds.append(bounds[j])
      bnds.append(0.5 * (bounds[j] + bounds[j + 1]))
    bnds.append(bounds[-1])
    bounds = bnds

  return np.array(bounds)

## Check if a directory exists. If not, make it.
def check_make_dir(dir):
  if not os.path.isdir(dir):
    os.makedirs(dir)

## Check if an Exodus file exists for a given adaptivity cycle.
def check_adaptivity_exodus(case, alg, batch, ref, cycle):
  path = f'./{case}/{alg}_{batch}/frac_{ref}.e'
  if cycle > 1 and cycle < 10:
    path += f'-s00{str(cycle)}'
  if cycle >= 10:
    path += f'-s0{str(cycle)}'
  return os.path.exists(path)

def last_adaptivity_idx(case, alg, batch, ref, cycles):
  for c in range(len(cycles)):
    if not check_adaptivity_exodus(case, alg, batch, ref, cycles[c]):
      return c

  return len(cycles)

## Colour the SFR geometry.
def colour_sfr(ax):
  R_FUEL = 0.5
  T_CLAD = 0.1
  PITCH  = 1.5
  T_NA = PITCH - 2.0 * (R_FUEL + T_CLAD)

  outer_fuel_pin_l = [0, 1, NUM_PINS['sfr'] - 1]
  outer_fuel_pin_r = [0, NUM_PINS['sfr'] - 2, NUM_PINS['sfr'] - 1]
  x_i = 0.0
  x_i_1 = 0.0
  for i in range(NUM_PINS['sfr']):
    x_i += R_FUEL
    if i in outer_fuel_pin_l:
      ax.axvspan(x_i_1, x_i, facecolor = 'tab:red', alpha = ALPHA)
    else:
      ax.axvspan(x_i_1, x_i, facecolor = 'tab:orange', alpha = ALPHA)
    x_i_1 += R_FUEL
    x_i += T_CLAD
    ax.axvspan(x_i_1, x_i, facecolor = 'tab:brown', alpha = ALPHA)
    x_i_1 += T_CLAD
    x_i += T_NA
    ax.axvspan(x_i_1, x_i, facecolor = 'tab:grey', alpha = ALPHA)
    x_i_1 += T_NA
    x_i += T_CLAD
    ax.axvspan(x_i_1, x_i, facecolor = 'tab:brown', alpha = ALPHA)
    x_i_1 += T_CLAD
    x_i += R_FUEL
    if i in outer_fuel_pin_r:
      ax.axvspan(x_i_1, x_i, facecolor = 'tab:red', alpha = ALPHA)
    else:
      ax.axvspan(x_i_1, x_i, facecolor = 'tab:orange', alpha = ALPHA)
    x_i_1 += R_FUEL

## Colour the LWR geometry.
def colour_lwr(ax):
  R_FUEL = 0.5
  T_CLAD = 0.1
  PITCH  = 1.5
  T_WATER = PITCH - 2.0 * (R_FUEL + T_CLAD)

  guide_l = [2, 5, 8]
  guide_r = [1, 4, 7]
  x_i = 0.0
  x_i_1 = 0.0
  for i in range(NUM_PINS['lwr']):
    x_i += R_FUEL
    if i in guide_l:
      ax.axvspan(x_i_1, x_i, facecolor = 'tab:blue', alpha = ALPHA)
    else:
      ax.axvspan(x_i_1, x_i, facecolor = 'tab:green', alpha = ALPHA)
    x_i_1 += R_FUEL
    x_i += T_CLAD
    ax.axvspan(x_i_1, x_i, facecolor = 'tab:grey', alpha = ALPHA)
    x_i_1 += T_CLAD
    x_i += T_WATER
    ax.axvspan(x_i_1, x_i, facecolor = 'tab:blue', alpha = ALPHA)
    x_i_1 += T_WATER
    x_i += T_CLAD
    ax.axvspan(x_i_1, x_i, facecolor = 'tab:grey', alpha = ALPHA)
    x_i_1 += T_CLAD
    x_i += R_FUEL
    if i in guide_r:
      ax.axvspan(x_i_1, x_i, facecolor = 'tab:blue', alpha = ALPHA)
    else:
      ax.axvspan(x_i_1, x_i, facecolor = 'tab:green', alpha = ALPHA)
    x_i_1 += R_FUEL

## Colour in the background based on the case.
def colour_background(ax, case):
  if case == 'sfr':
    colour_sfr(ax)
  else:
    colour_lwr(ax)

# Load the line plot "reference" solutions.
def load_data_xlines_ref(case):
  lines = {}
  for data in LINE_DATA:
    lines[data] = pd.read_csv(f'./{case}/reference/openmc_ref_out_post_process0_{data}_0001.csv')[data].to_numpy()
  return lines

## Load the data for line plots over x.
def load_data_xlines(case):
  lines = {}
  for ind in ALGORITHMS:
    lines[ind] = {}
    for b in BATCH_COUNT:
      lines[ind][b] = {}
      for r in REF_FRAC:
        lines[ind][b][r] = {}
        for data in LINE_DATA:
          lines[ind][b][r][data] = []
          for j in range(1, CYCLES + 1):
            if int((j) / 10) > 0:
              lines[ind][b][r][data].append(pd.read_csv(f'./{case}/{ind}_{b}/frac_{r}_post_process0_{data}_00{j}.csv')[data].to_numpy())
            else:
              lines[ind][b][r][data].append(pd.read_csv(f'./{case}/{ind}_{b}/frac_{r}_post_process0_{data}_000{j}.csv')[data].to_numpy())
  return lines

# Function to plot the x line data (integrals / averages over the y-z plane in slices).
def plot_xline_plots(xl, ref_xl, case, to_mask):
  plt.rcParams.update({'font.size': LARGE_FONT_SIZE})
  x_bnds = make_refined_bnds(case)
  mask = idx_mask_fuel(case, True) if to_mask else []

  for ind in ALGORITHMS:
    for b in BATCH_COUNT:
      for r in REF_FRAC:
        for data in LINE_DATA:
          check_make_dir(f'./results/{case}/gif_images/{ind}/batch_{b}/ref_{r}/{data}')
          print(f'Generating figures in results/{case}/gif_images/{ind}/batch_{b}/ref_{r}/{data}/*')

          # Compute the bounds for both axes to prevent the axes scales from bouncing all over the
          # place during refinement.
          a1_min = 1e30
          a1_max = 0.0
          a2_min = 1e30
          a2_max = 0.0
          for j in range(1, CYCLES + 1):
            if to_mask:
              for m in mask:
                d = 100.0 * np.abs(xl[ind][b][r][data][j - 1][m[:-1]] - ref_xl[data][m[:-1]]) / np.maximum(ref_xl[data][m[:-1]], 1e-6)
                a2_min = np.minimum(np.min(d), a2_min)
                a2_max = np.maximum(np.max(d), a2_max)

                a1_min = np.minimum(np.minimum(np.min(xl[ind][b][r][data][j - 1][m[:-1]]), a1_min), np.minimum(np.min(ref_xl[data][m[:-1]]), a1_min))
                a1_max = np.maximum(np.maximum(np.max(xl[ind][b][r][data][j - 1][m[:-1]]), a1_max), np.maximum(np.max(ref_xl[data][m[:-1]]), a1_max))
            else:
              a1_min = np.minimum(np.minimum(np.min(xl[ind][b][r][data][j - 1]), a1_min), np.minimum(np.min(ref_xl[data]), a1_min))
              a1_max = np.maximum(np.maximum(np.max(xl[ind][b][r][data][j - 1]), a1_max), np.maximum(np.max(ref_xl[data]), a1_max))

          for j in range(1, CYCLES + 1):
            fig_1, ax_1 = plt.subplots()

            # Shade regions of the graph based on material.
            colour_background(ax_1, case)

            # Stairstep plot over bins.
            colour_1 = 'tab:red' if case == 'lwr' else 'tab:blue'
            colour_2 = 'tab:orange' if case == 'lwr' else 'tab:purple'
            if to_mask:
              for m in mask:
                l1 = ax_1.stairs(ref_xl[data][m[:-1]], x_bnds[m], linewidth=1, baseline=ref_xl[data][m[:-1]], color=colour_1, label='Reference', linestyle='--')
                l2 = ax_1.stairs(xl[ind][b][r][data][j - 1][m[:-1]], x_bnds[m], linewidth=1, baseline=xl[ind][b][r][data][j - 1][m[:-1]], color='black', label='AMR')
            else:
              l1 = ax_1.stairs(ref_xl[data], x_bnds, linewidth=1, baseline=ref_xl[data], color=colour_1, label='Reference', linestyle='--')
              l2 = ax_1.stairs(xl[ind][b][r][data][j - 1], x_bnds, linewidth=1, baseline=xl[ind][b][r][data][j - 1], color='black', label='AMR')
            ax_1.set_xlabel('x (cm)')
            ax_1.set_ylabel(AXES_LABELS[data])
            ax_1.set_title(f'Cycle {j}')
            ax_1.set_xlim(left=0.0, right=x_bnds[-1])
            ax_1.set_ylim(bottom = 0.95 * a1_min, top = 1.05 * a1_max)

            if to_mask:
              ax_2 = ax_1.twinx()
              for m in mask:
                d = 100.0 * np.abs(xl[ind][b][r][data][j - 1][m[:-1]] - ref_xl[data][m[:-1]]) / np.maximum(ref_xl[data][m[:-1]], 1e-6)
                l3 = ax_2.stairs(d, np.ones_like(x_bnds[m]) * INIT_X_LAYER_BNDS[case][-1] - x_bnds[m], linewidth=1, baseline=d, color=colour_2, label='Difference')
              ax_2.legend(handles=[l3], loc='upper right', borderpad=0.2)
              ax_2.set_ylabel('Absolute Relative Difference ($\%$)')

              ax_2.vlines(0.5 * (INIT_X_LAYER_BNDS[case][-1] + INIT_X_LAYER_BNDS[case][0]), ymin=0.0, ymax=1.0, color='black', transform=ax_2.get_xaxis_transform())
              ax_2.text(0.5 * (INIT_X_LAYER_BNDS[case][-1] + INIT_X_LAYER_BNDS[case][0]), 0.5, 'Symmetry Plane',
                        rotation='vertical', color='black', va='center', ha='right', transform=ax_2.get_xaxis_transform())
              ax_2.set_ylim(bottom = 0.95 * a2_min, top = 1.05 * a2_max)

            if case == 'sfr':
              ax_1.legend(handles=[l2, l1], loc='upper left', borderpad=0.2, bbox_to_anchor=(0.15, 1.0))
            else:
              ax_1.legend(handles=[l2, l1], loc='upper left', borderpad=0.2)

            fig_1.set_figheight(5.0)
            fig_1.set_figwidth(8.0)
            fig_1.tight_layout()
            fig_1.savefig(f'./results/{case}/gif_images/{ind}/batch_{b}/ref_{r}/{data}/{data}_{j}.png')
            plt.close('all')
  plt.rcParams.update({'font.size': DEFAULT_FONT_SIZE})

## Function to generate a relative L2 difference between each parameter sweep and the reference.
def l2_diffs(xl, ref_xl):
  diffs = {}
  for ind in ALGORITHMS:
    diffs[ind] = {}
    for b in BATCH_COUNT:
      diffs[ind][b] = {}
      for r in REF_FRAC:
        diffs[ind][b][r] = {}
        for data in LINE_DATA:
          diffs[ind][b][r][data] = []
          for j in range(1, CYCLES + 1):
            d = ref_xl[data] - xl[ind][b][r][data][j - 1]
            diffs[ind][b][r][data].append(np.abs(np.linalg.norm(d) / np.linalg.norm(ref_xl[data])))
  return diffs

## Function to plot the L2 difference as a function of adaptivity cycles and refinement threshold.
def plot_l2_diff(case, diffs):
  DATA_MARKERS = [",", ".", "o", "+", "x"]

  check_make_dir(f'./results/{case}/l2_diff')
  print(f'Generating figures in ./results/{case}/l2_diff/*')

  for b in BATCH_COUNT:
    for data in LINE_DATA:
      fig = plt.figure(figsize=(SIZE_3D_W,SIZE_3D_H))
      ax_1 = fig.add_subplot(projection='3d')

      first = True
      lb = ''
      for r in range(len(REF_FRAC)):
        for ind in ALGORITHMS:
          last_idx = last_adaptivity_idx(case, ind, b, '03', CYCLE_POINTS)
          style = '-' if ind.count('lh') > 0 else ':'
          ax_1.plot(CYCLE_POINTS[:last_idx], diffs[ind][b][REF_FRAC[r]][data][:last_idx], zs=(float(REF_FRAC[r]) / 10.0), zdir='x',
                    color = ALG_COLOURS[ind], marker = DATA_MARKERS[r], label = lb + ALG_NAMES[ind], linestyle = style, linewidth=2, markersize=8)
        if first:
          first = False
          lb = '_'
      ax_1.legend(ncols=3, prop={'size': FIG_3D_FONT_SIZE})
      ax_1.tick_params(which='both', labelsize=FIG_3D_FONT_SIZE)
      ax_1.set_xlabel('\nRefinement Threshold', fontsize=FIG_3D_FONT_SIZE)
      ax_1.set_ylabel('\nNumber of Cycles', fontsize=FIG_3D_FONT_SIZE)
      ax_1.set_zlabel('\n$L_2$ Relative Difference', fontsize=FIG_3D_FONT_SIZE)
      ax_1.view_init(elev = ELEVATION,  azim = AZIMUTHAL, roll = 0.0)
      ax_1.ticklabel_format(axis='z', style='sci', scilimits=(0,0))
      fig.tight_layout(rect=(-0.15, 0.0, 1.0, 1.0))
      fig.savefig(f'./results/{case}/l2_diff/{b}_{data}.png')
      plt.close('all')

## Function to fetch post-processor data for the parameter sweep.
def get_pp_data(case):
  pp_data = {}
  for ind in ALGORITHMS:
    pp_data[ind] = {}
    for b in BATCH_COUNT:
      pp_data[ind][b] = {}
      for r in REF_FRAC:
        df = pd.read_csv(f'./{case}/{ind}_{b}/frac_{r}.csv')
        pp_data[ind][b][r] = {
          'num_elem' : df['num_active'].to_numpy(),
          'max_err'  : df['max_heating_rel_err'].to_numpy(),
          'mean_err' : df['avg_heating_rel_err'].to_numpy(),
          'min_err'  : df['min_heating_rel_err'].to_numpy()
        }
  return pp_data

## Function to plot the post-processor data (number of active elements
## and mean relative error for heating).
def plot_pp_data(case, pp_data):
  DATA_MARKERS = [",", ".", "o", "+", "x"]
  plt.rcParams.update({'font.size': LARGE_FONT_SIZE})

  check_make_dir(f'./results/{case}/num_elem')
  check_make_dir(f'./results/{case}/mean_heating_err')
  print(f'Generating figures in ./results/{case}/num_elem/* and ./results/{case}/mean_heating_err/*')

  for b in BATCH_COUNT:
    fig_1 = plt.figure(figsize=(SIZE_3D_W,SIZE_3D_H))
    ax_1 = fig_1.add_subplot(projection='3d')

    first = True
    lb = ''
    for r in range(len(REF_FRAC)):
      for ind in ALGORITHMS:
        last_idx = last_adaptivity_idx(case, ind, b, '03', CYCLE_POINTS)
        style = '-' if ind.count('lh') > 0 else ':'
        ax_1.plot(CYCLE_POINTS[:last_idx], pp_data[ind][b][REF_FRAC[r]]['num_elem'][:last_idx], zs=(float(REF_FRAC[r]) / 10.0), zdir='x',
                  color = ALG_COLOURS[ind], marker = DATA_MARKERS[r], label = lb + ALG_NAMES[ind], linestyle = style, linewidth=2, markersize=8)
      if first:
        first = False
        lb = '_'
    ax_1.yaxis.set_inverted(True)
    ax_1.legend(ncols=3, prop={'size': FIG_3D_FONT_SIZE})
    ax_1.tick_params(which='both', labelsize=FIG_3D_FONT_SIZE)
    ax_1.set_xlabel('\nRefinement Threshold', fontsize=FIG_3D_FONT_SIZE)
    ax_1.set_ylabel('\nNumber of Cycles', fontsize=FIG_3D_FONT_SIZE)
    ax_1.set_zlabel('Number of Active Elements', fontsize=FIG_3D_FONT_SIZE)
    ax_1.view_init(elev = ELEVATION,  azim = AZIMUTHAL, roll = 0.0)
    ax_1.ticklabel_format(axis='z', style='sci', scilimits=(0,0))
    fig_1.tight_layout(rect=(-0.15, 0.0, 1.0, 1.0))
    fig_1.savefig(f'./results/{case}/num_elem/{b}_num_elem.png')
    plt.close('all')

  plt.rcParams.update({'font.size': DEFAULT_FONT_SIZE})

# The main function proper.
if __name__ == "__main__":
  ap = ArgumentParser(description='PHYSOR 2026 AMR parameter sweep post-processor.')
  ap.add_argument('case', type=str, help='The particular case to generate. Must be one of either lwr or sfr.')
  ap.add_argument('--disable-xlines', action='store_false',
                  help='Whether the solution should be plotted along the length of the slab for each ' \
                       'datapoint in the parameter sweep AND each adaptivity cycle.')
  ap.add_argument('--disable-3d',     action='store_false',
                  help='Whether the 3D comparison plots should be generateed or not.')
  ap.add_argument('--disable-mask',   action='store_false',
                  help='Whether the plots over the lengths of the slab overlay the material ' \
                       'compositions of the slab or not.')
  args = ap.parse_args()

  xl = load_data_xlines(args.case)
  ref_xl = load_data_xlines_ref(args.case)
  diffs = l2_diffs(xl, ref_xl)
  pp_data = get_pp_data(args.case)

  # Only plot the data over x if the user requests it.
  if args.disable_xlines:
    plot_xline_plots(xl, ref_xl, args.case, args.disable_mask)

  # Only plot 3D data if requested.
  if args.disable_3d:
    plot_l2_diff(args.case, diffs)
    plot_pp_data(args.case, pp_data)
