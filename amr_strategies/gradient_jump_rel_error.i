!include amr_common.i

[AuxVariables]
  [grad_kappa_fission]
    family = MONOMIAL_VEC
    order = CONSTANT
  []
[]

[AuxKernels]
  [grad_kappa_fission]
    type = FDTallyGradAux
    variable = grad_kappa_fission
    score = 'kappa_fission'
  []
[]

[Adaptivity]
  marker = error_combo
  steps = ${NUM_CYCLES}

  [Indicators/error]
    type = VectorValueJumpIndicator
    variable = grad_kappa_fission
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
      variable = heat_source_rel_error
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
