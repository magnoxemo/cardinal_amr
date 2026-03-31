!include amr_common.i

[AuxVariables]
  [current]
    family = MONOMIAL_VEC
    order = CONSTANT
  []
[]

[AuxKernels]
  [current]
    type = ParsedVectorAux
    variable = current
    coupled_variables = 'flux_l1_mneg1 flux_l1_mpos0 flux_l1_mpos1'
    expression_x = 'flux_l1_mpos1'
    expression_y = 'flux_l1_mneg1'
    expression_z = 'flux_l1_mpos0'
  []
[]

[Adaptivity]
  marker = lh_cj_frac
  steps = ${NUM_CYCLES}

  [Indicators/error]
    type = VectorValueJumpIndicator
    variable = current
  []
  [Markers/lh_cj_frac]
    type = ErrorFractionLookAheadMarker
    indicator = error
    refine = ${R_ERROR_FRACTION}
    coarsen = 0.0
    rel_error_refine = ${R_STAT_ERROR}
    stat_error_indicator = 'flux_l0_mpos0_rel_error'
  []
[]
