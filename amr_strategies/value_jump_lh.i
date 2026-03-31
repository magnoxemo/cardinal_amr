!include amr_common.i

[Adaptivity]
  marker = lh_vj_frac
  steps = ${NUM_CYCLES}

  [Indicators/error]
    type = ValueJumpIndicator
    variable = heat_source
  []
  [Markers/lh_vj_frac]
    type = ErrorFractionLookAheadMarker
    indicator = error
    refine = ${R_ERROR_FRACTION}
    coarsen = 0.0
    rel_error_refine = ${R_STAT_ERROR}
    stat_error_indicator = 'heat_source_rel_error'
  []
[]
