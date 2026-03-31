!include amr_common.i

[Adaptivity]
  marker = lh_inv_od_frac
  steps = ${NUM_CYCLES}

  [Indicators/optical_depth]
    type = ElementOpticalDepthIndicator
    rxn_rate = 'fission'
    h_type = 'cube_root'
  []
  [Markers/lh_inv_od_frac]
    type = ErrorFractionLookAheadMarker
    indicator = optical_depth
    refine = ${R_ERROR_FRACTION}
    coarsen = 0.0
    rel_error_refine = ${R_STAT_ERROR}
    stat_error_indicator = 'heat_source_rel_error'
  []
[]
