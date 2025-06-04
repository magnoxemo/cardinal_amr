import sys
sys.path.append("../../")

import openmc
import openmc.material

from materials import make_sfr_material, material_dict
import common_input as geom
from SFR.Pincell.make_sfr_pincell_model import model_generate as pincell_model_generator


def make_hexagonal_ring_lists(number_of_ring: int, universe: openmc.Universe):
    ring_list = []
    for i in range(number_of_ring, 0, -1):
        if i == 1:
            ring = [universe]
        else:
            ring = [universe] * (i - 1) * 6
        ring_list.append(ring)
    return ring_list


def main():
    """

    :return:
    a assembly universe,
    openmc.Materials class,
    openmc.Geometry class,
    openmc.Settings class

    the universe class is mostly for reuse if we want to create an assembly
    """

    top = openmc.ZPlane(z0=geom.height / 2)
    bottom = openmc.ZPlane(z0=-geom.height / 2)
    top.boundary_type = "vacuum"
    bottom.boundary_type = "vacuum"
    sodium = make_sfr_material(material_dict['sodium'], percent_type='ao')
    inner_u, material, _, setting = pincell_model_generator()
    material.append(sodium)

    sodium_mod_cell = openmc.Cell(fill=sodium)
    sodium_mod_u = openmc.Universe(cells=(sodium_mod_cell,))

    lattice = openmc.HexLattice()
    lattice.center = (0.0, 0.0, 0.0)
    lattice.orientation = "y"
    lattice.outer = sodium_mod_u
    lattice.pitch = (geom.lattice_pitch, geom.height / geom.AXIAL_DIVISIONS)
    lattice.universes = [make_hexagonal_ring_lists(9, inner_u)] * geom.AXIAL_DIVISIONS

    outer_in_surface = openmc.model.hexagonal_prism(
        edge_length=geom.edge_length, orientation="y"
    )
    main_in_assembly = openmc.Cell(
        fill=lattice, region=outer_in_surface & +bottom & -top
    )
    out_in_assembly = openmc.Cell(
        fill=sodium,
        region=~outer_in_surface & +bottom & -top
    )
    main_in_u = openmc.Universe(cells=[main_in_assembly, out_in_assembly])
    return main_in_u, material, openmc.Geometry(main_in_u), setting


if __name__ == "__main__":
    _, mat, geometry, settings = main()
    openmc.model.Model(geometry, mat, settings).export_to_xml()

