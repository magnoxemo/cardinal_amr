[Problem]
  [Tallies]
    [heat_source]
      type = MeshTally
      score = 'kappa_fission fission'
      name = 'heat_source fission'
      output = 'unrelaxed_tally_std_dev unrelaxed_tally_rel_error'
      normalize_by_global_tally = false
    []
    [flux]
      type = MeshTally
      score = 'flux'
      output = 'unrelaxed_tally_std_dev unrelaxed_tally_rel_error'
      filters = 'SH'
      normalize_by_global_tally = false
    []
  []

  [Filters/SH]
    type = SphericalHarmonicsFilter
    order = 1
  []
[]
