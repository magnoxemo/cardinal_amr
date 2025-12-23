R_FUEL  = 0.5
D_FUEL  = ${fparse 2.0 * R_FUEL}
T_CLAD  = 0.1
PITCH   = 1.5

T_WATER = ${fparse PITCH - 2.0 * (R_FUEL + T_CLAD)} # 0.3

[Mesh]
  [CMG]
    type = CartesianMeshGenerator
    dim = 3
    dx = '${R_FUEL} ${T_CLAD} ${T_WATER} ${T_CLAD}
          ${D_FUEL} ${T_CLAD} ${T_WATER} ${T_CLAD}
          ${D_FUEL} ${T_CLAD} ${T_WATER} ${T_CLAD}
          ${D_FUEL} ${T_CLAD} ${T_WATER} ${T_CLAD}
          ${D_FUEL} ${T_CLAD} ${T_WATER} ${T_CLAD}
          ${D_FUEL} ${T_CLAD} ${T_WATER} ${T_CLAD}
          ${D_FUEL} ${T_CLAD} ${T_WATER} ${T_CLAD}
          ${D_FUEL} ${T_CLAD} ${T_WATER} ${T_CLAD}
          ${D_FUEL} ${T_CLAD} ${T_WATER} ${T_CLAD}
          ${D_FUEL} ${T_CLAD} ${T_WATER} ${T_CLAD} ${R_FUEL}'
    dy = '2.0'
    dz = '2.0'
    ix = '1         1         1          1
          1         1         1          1
          1         1         1          1
          1         1         1          1
          1         1         1          1
          1         1         1          1
          1         1         1          1
          1         1         1          1
          1         1         1          1
          1         1         1          1         1'
    iy = '1'
    iz = '1'
    subdomain_id = '0 1 2 1
                    0 1 2 3
                    2 3 2 1
                    0 1 2 1
                    0 1 2 3
                    2 3 2 1
                    0 1 2 1
                    0 1 2 3
                    2 3 2 1
                    0 1 2 1 0'
  []
  [Rename]
    type = RenameBlockGenerator
    input = CMG
    old_block = '0 1 2 3'
    new_block = 'fuel zr_clad water clad'
  []
  [Origin]
    type = TransformGenerator
    input = Rename
    transform = TRANSLATE
    vector_value = '0.0 -1.0 -1.0'
  []
[]
