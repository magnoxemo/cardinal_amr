import openmc
import numpy as np
from argparse import ArgumentParser
import openmc.material

from SFR.materials import make_sfr_material, material_dict
from SFR import common_input as geom


def simulation_settings(shannon_entropy: bool, height: float):
    pitch = geom.pitch
    lower_left = (-pitch / 2, -pitch / 2, 0.0)
    upper_right = (pitch / 2, pitch / 2, height)
    uniform_dist = openmc.stats.Box(lower_left, upper_right)

    setting = openmc.Settings()
    setting.source = openmc.IndependentSource(space=uniform_dist)
    setting.batches = 200
    setting.inactive = 40
    setting.particles = 20000

    if shannon_entropy:
        entropy_mesh = openmc.RegularMesh()
        entropy_mesh.lower_left = lower_left
        entropy_mesh.upper_right = upper_right
        entropy_mesh.dimension = (10, 10, 20)
        setting.entropy_mesh = entropy_mesh

    setting.temperature = {
        "default": 280.0 + 273.15,
        "method": "interpolation",
        "range": (294.0, 3000.0),
        "tolerance": 1000.0,
    }
    return setting


def argument_parser():
    ap = ArgumentParser(description="SFR Pincell Model Generator")
    ap.add_argument(
        "-n",
        dest="n_axial",
        type=int,
        default=1,
        help="Number of cells in the Z direction",
    )
    ap.add_argument(
        "-e",
        "--shannon_entropy",
        action="store_true",
        help="Add Shannon entropy mesh"
    )
    ap.add_argument("-p", dest="pincell_type", type=str, default="inner_pincell",
                    help=("Material composition of the pincell fuel material"
                          "based on the location of pincell in the reactor geometry"))

    return ap.parse_args()


def model_generate(arguments):
    """
    :return:
    a pincell universe,
    openmc.Materials class,
    openmc.Geometry class,
    openmc.Settings class

    the universe class is mostly for reuse if we want to create an assembly
    """

    if arguments.pincell_type == "inner_pincell":
        fuel_material = make_sfr_material(material_dict['inner_fuel'], percent_type='wo')
    else:
        fuel_material = make_sfr_material(material_dict['outer_fuel'], percent_type='wo')
    cladding_material = make_sfr_material(material_dict['cladding'], percent_type='ao')
    sodium = make_sfr_material(material_dict['sodium'], percent_type='ao')
    helium = make_sfr_material(material_dict['helium'], percent_type='ao')

    fuel_or = openmc.ZCylinder(r=geom.r_fuel)
    clad_ir = openmc.ZCylinder(r=geom.r_clad_inner)
    clad_or = openmc.ZCylinder(r=geom.r_clad_inner + geom.t_clad)

    z_plane = [openmc.ZPlane(z0=i) for i in np.linspace(-geom.height / 2, geom.height / 2, arguments.n_axial + 1)]

    top = z_plane[-1]
    bottom = z_plane[0]
    top.boundary_type = "vacuum"
    bottom.boundary_type = "vacuum"

    all_inner_cells = []

    for i in range(arguments.n_axial):
        layer = +z_plane[i] & -z_plane[i + 1]
        all_inner_cells.append(openmc.Cell(fill=fuel_material, region=layer & -fuel_or))
        all_inner_cells.append(openmc.Cell(fill=helium, region=layer & +fuel_or & -clad_ir))
        all_inner_cells.append(openmc.Cell(fill=cladding_material, region=layer & +clad_ir & -clad_or))
        all_inner_cells.append(openmc.Cell(fill=sodium, region=+clad_or & layer))

    return openmc.Universe(cells=all_inner_cells), openmc.Materials(
        [fuel_material, sodium, helium, cladding_material]), openmc.Geometry(all_inner_cells), simulation_settings(
        arguments.shannon_entropy, height=geom.height)


if __name__ == "__main__":
    args = argument_parser()
    _, mat, geometry, settings = model_generate(args)
    openmc.model.Model(geometry, mat, settings).export_to_model_xml()
