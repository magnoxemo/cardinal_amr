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
  marker = lh_gj_frac
  steps = ${NUM_CYCLES}

  [Indicators/error]
    type = VectorValueJumpIndicator
    variable = grad_kappa_fission
  []
  [Markers/lh_gj_frac]
    type = ErrorFractionLookAheadMarker
    indicator = error
    refine = ${R_ERROR_FRACTION}
    coarsen = 0.0
    rel_error_refine = ${R_STAT_ERROR}
    stat_error_indicator = 'heat_source_rel_error'
  []
[]
