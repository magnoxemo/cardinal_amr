[Mesh]
  [file]
    type = FileMeshGenerator
    file = mesh_in.e
  []
[]

[Problem]
  type = OpenMCCellAverageProblem
  particles = 10000
  inactive_batches = 100
  batches = 1100

  power = 1.0
  source_rate_normalization = 'kappa_fission'
  skip_statepoint = true

  [Tallies]
    [flux]
      type = MeshTally
      score = 'flux'
      output = 'unrelaxed_tally_std_dev unrelaxed_tally_rel_error'
      filters = 'sh'
      normalize_by_global_tally = false
    []
    [heat_source]
      type = MeshTally
      score = 'kappa_fission fission'
      name = 'heat_source fission'
      output = 'unrelaxed_tally_std_dev unrelaxed_tally_rel_error'
      normalize_by_global_tally = false
    []
  []

  [Filters/sh]
    type = SphericalHarmonicsFilter
    order = 1
  []
[]

[Executioner]
  type = Transient
  num_steps = 10
[]

[Postprocessors]
  [num_active]
    type = NumElements
    elem_filter = active
  []
  [max_level]
    type = ElementMaxLevelPostProcessor
    level = 'h'
  []

  [max_heating_rel_err]
    type = TallyRelativeError
    value_type = max
    tally_score = kappa_fission
  []
  [avg_heating_rel_err]
    type = TallyRelativeError
    value_type = average
    tally_score = kappa_fission
  []
  [min_heating_rel_err]
    type = TallyRelativeError
    value_type = min
    tally_score = kappa_fission
  []

  [max_flux_rel_err]
    type = TallyRelativeError
    value_type = max
    tally_score = flux
  []
  [avg_flux_rel_err]
    type = TallyRelativeError
    value_type = average
    tally_score = flux
  []
  [min_flux_rel_err]
    type = TallyRelativeError
    value_type = min
    tally_score = flux
  []

  [max_fiss_rel_err]
    type = TallyRelativeError
    value_type = max
    tally_score = fission
  []
  [avg_fiss_rel_err]
    type = TallyRelativeError
    value_type = average
    tally_score = fission
  []
  [min_fiss_rel_err]
    type = TallyRelativeError
    value_type = min
    tally_score = fission
  []
[]

[Outputs]
  execute_on = 'TIMESTEP_END'
  exodus = true
  csv = true
  checkpoint = false
  wall_time_checkpoint = false
[]

[MultiApps]
  [post_process]
    type = TransientMultiApp
    input_files = 'post_process.i'
    execute_on = 'TIMESTEP_END'
  []
[]

[Transfers]
  [heating_to_pp]
    type = MultiAppGeneralFieldShapeEvaluationTransfer
    to_multi_app = 'post_process'
    source_variable = 'heat_source'
    variable = 'heat_source'
  []
  [flux_to_pp]
    type = MultiAppGeneralFieldShapeEvaluationTransfer
    to_multi_app = 'post_process'
    source_variable = 'flux_l0_mpos0'
    variable = 'flux'
  []
[]
