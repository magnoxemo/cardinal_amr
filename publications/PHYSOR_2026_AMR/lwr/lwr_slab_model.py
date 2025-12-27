import openmc
import numpy as np

import sys
sys.path.append("../../../models/lwr")

from openmc_materials import MATERIALS as LWR_MATS

#--------------------------------------------------------------------------------------------------------------------------#
# Some geometrical parameters to tweak.
#--------------------------------------------------------------------------------------------------------------------------#
NUM_PINS = 10
R_FUEL = 0.5
T_CLAD = 0.1
PITCH  = 1.5

YZ_SIDES = 1.0

# The positions of the guide tubes.
LEFT_GUIDE_INDICES  = [2, 5, 8]
RIGHT_GUIDE_INDICES = [1, 4, 7]
#--------------------------------------------------------------------------------------------------------------------------#

def main():
  #--------------------------------------------------------------------------------------------------------------------------#
  # Generate the geometry.
  #--------------------------------------------------------------------------------------------------------------------------#
  # Reflective Y and Z planes to make an "infinite" medium.
  y_0 = openmc.YPlane(y0 = -YZ_SIDES, boundary_type = 'reflective')
  y_1 = openmc.YPlane(y0 = YZ_SIDES, boundary_type = 'reflective')
  z_0 = openmc.ZPlane(z0 = -YZ_SIDES, boundary_type = 'reflective')
  z_1 = openmc.ZPlane(z0 = YZ_SIDES, boundary_type = 'reflective')
  yz_r = +y_0 & -y_1 & +z_0 & -z_1

  # Build the parameterized geometry. An infinite lattice of slabs "pincells", where the center cell is water to introduce
  # more moderation (and therefore a flux gradient).
  cells  = []
  planes = []
  x = 0.0
  planes.append(openmc.XPlane(x0 = x))
  for i in range(NUM_PINS):
    x += R_FUEL
    planes.append(openmc.XPlane(x0 = x))
    if i in LEFT_GUIDE_INDICES:
      cells.append(openmc.Cell(name = f'Water {len(cells) + 1}', fill = LWR_MATS['H2O'], region = +planes[-2] & -planes[-1] & yz_r))
    else:
      cells.append(openmc.Cell(name = f'Fuel {len(cells) + 1}', fill = LWR_MATS['UO2'], region = +planes[-2] & -planes[-1] & yz_r))
    x += T_CLAD
    planes.append(openmc.XPlane(x0 = x))
    if i in LEFT_GUIDE_INDICES:
      cells.append(openmc.Cell(name = f'Clad {len(cells) + 1}', fill = LWR_MATS['AL_C'], region = +planes[-2] & -planes[-1] & yz_r))
    else:
      cells.append(openmc.Cell(name = f'Clad {len(cells) + 1}', fill = LWR_MATS['ZR_C'], region = +planes[-2] & -planes[-1] & yz_r))
    x += PITCH - 2.0 * (R_FUEL + T_CLAD)
    planes.append(openmc.XPlane(x0 = x))
    cells.append(openmc.Cell(name = f'Water {len(cells) + 1}', fill = LWR_MATS['H2O'], region = +planes[-2] & -planes[-1] & yz_r))
    x += T_CLAD
    planes.append(openmc.XPlane(x0 = x))
    if i in RIGHT_GUIDE_INDICES:
      cells.append(openmc.Cell(name = f'Clad {len(cells) + 1}', fill = LWR_MATS['AL_C'], region = +planes[-2] & -planes[-1] & yz_r))
    else:
      cells.append(openmc.Cell(name = f'Clad {len(cells) + 1}', fill = LWR_MATS['ZR_C'], region = +planes[-2] & -planes[-1] & yz_r))
    x += R_FUEL
    planes.append(openmc.XPlane(x0 = x))
    if i in RIGHT_GUIDE_INDICES:
      cells.append(openmc.Cell(name = f'Water {len(cells) + 1}', fill = LWR_MATS['H2O'], region = +planes[-2] & -planes[-1] & yz_r))
    else:
      cells.append(openmc.Cell(name = f'Fuel {len(cells) + 1}', fill = LWR_MATS['UO2'], region = +planes[-2] & -planes[-1] & yz_r))

  planes[0].boundary_type = 'reflective'
  planes[-1].boundary_type = 'reflective'
  #--------------------------------------------------------------------------------------------------------------------------#

  #--------------------------------------------------------------------------------------------------------------------------#
  # Setup the model container.
  #--------------------------------------------------------------------------------------------------------------------------#
  lwr_slab_model = openmc.model.Model(geometry=openmc.Geometry(openmc.Universe(cells=cells)))
  lwr_slab_model.settings.source = [openmc.IndependentSource(space = openmc.stats.Box(lower_left = (0.0, -YZ_SIDES, -YZ_SIDES),
                                                                                      upper_right = (x, YZ_SIDES, YZ_SIDES)))]
  # Add some temporary settings. These get overridden in Cardinal.
  lwr_slab_model.settings.batches = 100
  lwr_slab_model.settings.generations_per_batch = 10
  lwr_slab_model.settings.inactive = 10
  lwr_slab_model.settings.particles = 1000
  lwr_slab_model.export_to_model_xml()
  #--------------------------------------------------------------------------------------------------------------------------#

if __name__ == "__main__":
  main()
