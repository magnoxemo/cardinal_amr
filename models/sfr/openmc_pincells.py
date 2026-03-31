import openmc
from models.sfr import common_input as pincell_params
from models.sfr.openmc_materials import MATERIALS as sfr_mats

PINCELLS = {}

fuel_or = openmc.ZCylinder(r=pincell_params.r_fuel)
clad_ir = openmc.ZCylinder(r=pincell_params.r_clad_inner)
clad_or = openmc.ZCylinder(r=(pincell_params.r_clad_inner + pincell_params.t_clad))

cladding_cell = openmc.Cell(fill=sfr_mats['cladding'], region=+clad_ir & -clad_or)
gas_gap_cell = openmc.Cell(fill=sfr_mats['helium'], region=+fuel_or & -clad_ir)
fuel_cell_outer = openmc.Cell(fill=sfr_mats['inner_fuel'], region=-fuel_or)
fuel_cell_inner = openmc.Cell(fill=sfr_mats['inner_fuel'], region=-fuel_or)
sodium_cell = openmc.Cell(fill=sfr_mats['sodium'], region=+clad_or)

PINCELLS["inner"] = [openmc.Universe(cells=[fuel_cell_inner, gas_gap_cell, cladding_cell, sodium_cell]), openmc.Materials([inner_fuel_material, helium, cladding_material, sodium])]
PINCELLS["outer"] = [openmc.Universe(cells=[fuel_cell_inner, gas_gap_cell, cladding_cell, sodium_cell]), openmc.Materials([outer_fuel_material, helium, cladding_material, sodium])]
