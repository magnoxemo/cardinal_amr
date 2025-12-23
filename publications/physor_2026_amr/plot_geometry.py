import numpy as np
from matplotlib import pyplot as plt

plt.rcParams.update({'font.size': 14})
plt.rcParams.update({'text.usetex': True})

# Plot the LWR geometry
def lwr_geom():
  NUM_PINS = 10
  R_FUEL = 0.5
  T_CLAD = 0.1
  PITCH  = 1.5
  T_WATER = PITCH - 2.0 * (R_FUEL + T_CLAD)

  fig_1, ax_1 = plt.subplots()
  lines = []
  guide_l = [2, 5, 8]
  guide_r = [1, 4, 7]
  x_i = 0.0
  x_i_1 = 0.0
  for i in range(NUM_PINS):
    x_i += R_FUEL
    if i in guide_l:
      lines.append(ax_1.axvspan(x_i_1, x_i, facecolor = 'tab:blue', alpha = 1.0, label = 'Water', ymin=0.1, ymax=0.9))
    else:
      lines.append(ax_1.axvspan(x_i_1, x_i, facecolor = 'tab:green', alpha = 1.0, label = 'UO$_2$', ymin=0.1, ymax=0.9))
    x_i_1 += R_FUEL
    x_i += T_CLAD
    lines.append(ax_1.axvspan(x_i_1, x_i, facecolor = 'tab:grey', alpha = 1.0, label = 'Clad', ymin=0.1, ymax=0.9))
    x_i_1 += T_CLAD
    x_i += T_WATER
    lines.append(ax_1.axvspan(x_i_1, x_i, facecolor = 'tab:blue', alpha = 1.0, label = 'Water', ymin=0.1, ymax=0.9))
    x_i_1 += T_WATER
    x_i += T_CLAD
    lines.append(ax_1.axvspan(x_i_1, x_i, facecolor = 'tab:grey', alpha = 1.0, label = 'Clad', ymin=0.1, ymax=0.9))
    x_i_1 += T_CLAD
    x_i += R_FUEL
    if i in guide_r:
      lines.append(ax_1.axvspan(x_i_1, x_i, facecolor = 'tab:blue', alpha = 1.0, label = 'Water', ymin=0.1, ymax=0.9))
    else:
      lines.append(ax_1.axvspan(x_i_1, x_i, facecolor = 'tab:green', alpha = 1.0, label = 'UO$_2$', ymin=0.1, ymax=0.9))
    x_i_1 += R_FUEL

  ax_1.set_xlabel('x (cm)')
  ax_1.set_ylabel('Reflective Boundary')
  ax_1.set_yticks([])
  ax_2 = ax_1.twinx()
  ax_2.set_ylabel('Symmetry Plane')
  ax_2.set_yticks([])
  ax_1.set_xlim(left=0.0, right=7.5)
  fig_1.legend(handles=[lines[0], lines[1], lines[2]], ncol=3, loc='upper center')
  fig_1.set_figheight(2.5)
  fig_1.set_figwidth(5.0)
  fig_1.tight_layout()
  fig_1.savefig('./lwr_geometry.png')
  plt.show()
  plt.close()

# Plot the SFR geometry
def sfr_geom():
  NUM_PINS = 8
  R_FUEL = 0.5
  T_CLAD = 0.1
  PITCH  = 1.5
  T_NA = PITCH - 2.0 * (R_FUEL + T_CLAD)

  fig_1, ax_1 = plt.subplots()
  lines = []
  outer_fuel_pin_l = [0, 1, NUM_PINS - 1]
  outer_fuel_pin_r = [0, NUM_PINS - 2, NUM_PINS - 1]
  x_i = 0.0
  x_i_1 = 0.0
  for i in range(NUM_PINS):
    x_i += R_FUEL
    if i in outer_fuel_pin_l:
      lines.append(ax_1.axvspan(x_i_1, x_i, facecolor = 'tab:red', alpha = 1.0, label = 'HE Metallic Fuel', ymin=0.1, ymax=0.9))
    else:
      lines.append(ax_1.axvspan(x_i_1, x_i, facecolor = 'tab:orange', alpha = 1.0, label = 'LE Metallic Fuel', ymin=0.1, ymax=0.9))
    x_i_1 += R_FUEL
    x_i += T_CLAD
    lines.append(ax_1.axvspan(x_i_1, x_i, facecolor = 'tab:brown', alpha = 1.0, label = 'Clad', ymin=0.1, ymax=0.9))
    x_i_1 += T_CLAD
    x_i += T_NA
    lines.append(ax_1.axvspan(x_i_1, x_i, facecolor = 'tab:grey', alpha = 1.0, label = 'Sodium', ymin=0.1, ymax=0.9))
    x_i_1 += T_NA
    x_i += T_CLAD
    lines.append(ax_1.axvspan(x_i_1, x_i, facecolor = 'tab:brown', alpha = 1.0, label = 'Clad', ymin=0.1, ymax=0.9))
    x_i_1 += T_CLAD
    x_i += R_FUEL
    if i in outer_fuel_pin_r:
      lines.append(ax_1.axvspan(x_i_1, x_i, facecolor = 'tab:red', alpha = 1.0, label = 'HE Metallic Fuel', ymin=0.1, ymax=0.9))
    else:
      lines.append(ax_1.axvspan(x_i_1, x_i, facecolor = 'tab:orange', alpha = 1.0, label = 'LE Metallic Fuel', ymin=0.1, ymax=0.9))
    x_i_1 += R_FUEL

  ax_1.set_xlabel('x (cm)')
  ax_1.set_ylabel('Reflective Boundary')
  ax_1.set_yticks([])
  ax_2 = ax_1.twinx()
  ax_2.set_ylabel('Symmetry Plane')
  ax_2.set_yticks([])
  ax_1.set_xlim(left=0.0, right=6.0)
  fig_1.legend(handles=[lines[0], lines[9], lines[1], lines[2]], ncol=4, loc='upper center')
  fig_1.set_figheight(2.5)
  fig_1.set_figwidth(8.0)
  fig_1.tight_layout()
  fig_1.savefig('./sfr_geometry.png')
  plt.show()
  plt.close()

if __name__ == "__main__":
  lwr_geom()
  sfr_geom()
