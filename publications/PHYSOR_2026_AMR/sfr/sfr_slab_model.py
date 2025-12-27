import openmc
import numpy as np

import sys
sys.path.append("../../../models/sfr")

from openmc_materials import MATERIALS as SFR_MATS

#--------------------------------------------------------------------------------------------------------------------------#
# Some geometrical parameters to tweak.
#--------------------------------------------------------------------------------------------------------------------------#
NUM_PINS = 8
R_FUEL = 0.5
T_CLAD = 0.1
PITCH  = 1.5

YZ_SIDES = 1.0

# The position of the outer pins.
OUTER_FUEL_PIN_L = [0, 1, NUM_PINS - 1]
OUTER_FUEL_PIN_R = [0, NUM_PINS - 2, NUM_PINS - 1]
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

  # Build the geometry. An infinite lattice of slabs "pincells", where the center cell is the inner fuel to introduce a flux gradient.
  cells  = []
  planes = []
  x = 0.0
  planes.append(openmc.XPlane(x0 = x))
  for i in range(NUM_PINS):
    x += R_FUEL
    planes.append(openmc.XPlane(x0 = x))
    if i in OUTER_FUEL_PIN_L:
      cells.append(openmc.Cell(name = f'Fuel {len(cells) + 1}', fill = SFR_MATS['outer_fuel'], region = +planes[-2] & -planes[-1] & yz_r))
    else:
      cells.append(openmc.Cell(name = f'Fuel {len(cells) + 1}', fill = SFR_MATS['inner_fuel'], region = +planes[-2] & -planes[-1] & yz_r))
    x += T_CLAD
    planes.append(openmc.XPlane(x0 = x))
    cells.append(openmc.Cell(name = f'Clad {len(cells) + 1}', fill = SFR_MATS['cladding'], region = +planes[-2] & -planes[-1] & yz_r))
    x += PITCH - 2.0 * (R_FUEL + T_CLAD)
    planes.append(openmc.XPlane(x0 = x))
    cells.append(openmc.Cell(name = f'Water {len(cells) + 1}', fill = SFR_MATS['sodium'], region = +planes[-2] & -planes[-1] & yz_r))
    x += T_CLAD
    planes.append(openmc.XPlane(x0 = x))
    cells.append(openmc.Cell(name = f'Clad {len(cells) + 1}', fill = SFR_MATS['cladding'], region = +planes[-2] & -planes[-1] & yz_r))
    x += R_FUEL
    planes.append(openmc.XPlane(x0 = x))
    if i in OUTER_FUEL_PIN_R:
      cells.append(openmc.Cell(name = f'Fuel {len(cells) + 1}', fill = SFR_MATS['outer_fuel'], region = +planes[-2] & -planes[-1] & yz_r))
    else:
      cells.append(openmc.Cell(name = f'Fuel {len(cells) + 1}', fill = SFR_MATS['inner_fuel'], region = +planes[-2] & -planes[-1] & yz_r))

  planes[0].boundary_type = 'reflective'
  planes[-1].boundary_type = 'reflective'
  #--------------------------------------------------------------------------------------------------------------------------#

  #--------------------------------------------------------------------------------------------------------------------------#
  # Setup the model container.
  #--------------------------------------------------------------------------------------------------------------------------#
  sfr_slab_model = openmc.model.Model(geometry=openmc.Geometry(openmc.Universe(cells=cells)))
  sfr_slab_model.settings.source = [openmc.IndependentSource(space = openmc.stats.Box(lower_left = (0.0, -YZ_SIDES, -YZ_SIDES),
                                                                                      upper_right = (x, YZ_SIDES, YZ_SIDES)))]
  # Add some temporary settings. These get overridden in Cardinal.
  sfr_slab_model.settings.batches = 100
  sfr_slab_model.settings.generations_per_batch = 10
  sfr_slab_model.settings.inactive = 10
  sfr_slab_model.settings.particles = 1000
  sfr_slab_model.export_to_model_xml()
  #--------------------------------------------------------------------------------------------------------------------------#

if __name__ == "__main__":
  main()
