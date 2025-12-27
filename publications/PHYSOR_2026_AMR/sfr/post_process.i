LAYER_BNDS = '0.0  0.5  0.6  0.9  1.0  2.0  2.1  2.4  2.5  3.5  3.6  3.9  4.0  5.0  5.1  5.4  5.5 6.5
              6.6  6.9  7.0  8.0  8.1  8.4  8.5  9.5  9.6  9.9  10.0 11.0 11.1 11.4 11.5 12.0'

[Mesh]
  [ref_file]
    type = FileMeshGenerator
    file = sfr_mesh_ref_in.e
  []
[]

!include ../common_pp.i
