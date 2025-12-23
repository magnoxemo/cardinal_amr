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
  marker = error_combo
  steps = ${NUM_CYCLES}

  [Indicators/error]
    type = VectorValueJumpIndicator
    variable = current
  []
  [Markers]
    [error_frac]
      type = ErrorFractionMarker
      indicator = error
      refine = ${R_ERROR_FRACTION}
      coarsen = 0.0
    []
    [rel_error]
      type = ValueThresholdMarker
      invert = true
      coarsen = ${C_STAT_ERROR}
      refine = ${R_STAT_ERROR}
      variable = flux_l0_mpos0_rel_error
      third_state = DO_NOTHING
    []
    [error_combo]
      type = BooleanComboMarker
      # Only refine iff the relative error is sufficiently low AND there is a large enough
      # jump discontinuity in the solution.
      refine_markers = 'rel_error error_frac'
      # Coarsen based exclusively on relative error. Jump discontinuities in the solution
      # from large relative errors causes the 'error_frac' marker to erroneously mark elements
      # for refinement.
      coarsen_markers = 'rel_error'
      boolean_operator = and
    []
  []
[]
