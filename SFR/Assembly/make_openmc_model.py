import os
import openmc
import openmc.material

from SFR.materials import make_sfr_material, material_dict
from SFR import common_input as geom
from SFR.Pincell.make_openmc_model import model_generate as pincell_model_generator
from SFR.Pincell.make_openmc_model import argument_parser


def make_hexagonal_ring_lists(number_of_ring: int, universe: openmc.Universe):
    return [[universe] if i == 1 else [universe] * (i - 1) * 6 for i in range(number_of_ring, 0, -1)]


def main(arguments):
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
    inner_u, material, _, setting = pincell_model_generator(arguments)
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
    args = argument_parser()
    _, mat, geometry, settings = main(args)
    openmc.model.Model(geometry, mat, settings).export_to_model_xml()
