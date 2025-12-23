!include amr_common.i

[Adaptivity]
  marker = error_combo
  steps = ${NUM_CYCLES}

  [Indicators/optical_depth]
    type = ElementOpticalDepthIndicator
    rxn_rate = 'fission'
    h_type = 'cube_root'
  []
  [Markers]
    [depth_frac]
      type = ErrorFractionMarker
      indicator = optical_depth
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
      # Only refine iff the relative error is sufficiently low AND the optical depth is
      # sufficiently large.
      refine_markers = 'rel_error depth_frac'
      # Coarsen based exclusively on relative error.
      coarsen_markers = 'rel_error'
      boolean_operator = and
    []
  []
[]
