!include common.i

[AuxVariables]
  [heat_source]
    family = MONOMIAL
    order = CONSTANT
    initial_condition = '0.0'
  []
  [flux]
    family = MONOMIAL
    order = CONSTANT
    initial_condition = '0.0'
  []
[]

[UserObjects]
  [Heating_X_Int]
    type = LayeredIntegral
    variable = 'heat_source'
    direction = 'x'
    bounds = ${LAYER_BNDS}
    bound_uniform_splits = ${MAX_H_LEVEL}
  []
  [Heating_X_Avg]
    type = LayeredAverage
    variable = 'heat_source'
    direction = 'x'
    bounds = ${LAYER_BNDS}
    bound_uniform_splits = ${MAX_H_LEVEL}
  []
  [Flux_X_Int]
    type = LayeredIntegral
    variable = 'flux'
    direction = 'x'
    bounds = ${LAYER_BNDS}
    bound_uniform_splits = ${MAX_H_LEVEL}
  []
  [Flux_X_Avg]
    type = LayeredAverage
    variable = 'flux'
    direction = 'x'
    bounds = ${LAYER_BNDS}
    bound_uniform_splits = ${MAX_H_LEVEL}
  []
[]

[VectorPostprocessors]
  [Heating_X_Int_Out]
    type = SpatialUserObjectVectorPostprocessor
    userobject = Heating_X_Int
  []
  [Heating_X_Avg_Out]
    type = SpatialUserObjectVectorPostprocessor
    userobject = Heating_X_Avg
  []
  [Flux_X_Int_Out]
    type = SpatialUserObjectVectorPostprocessor
    userobject = Flux_X_Int
  []
  [Flux_X_Avg_Out]
    type = SpatialUserObjectVectorPostprocessor
    userobject = Flux_X_Avg
  []
[]

[Problem]
  type = FEProblem
  solve = false
[]

[Executioner]
  type = Transient
[]

[Outputs]
  csv = true
  exodus = false
  execute_on = 'TIMESTEP_END'
  checkpoint = false
  wall_time_checkpoint = false
[]
