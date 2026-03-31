# The number of refinement cycles.
NUM_CYCLES = 10

# The upper error fraction. Elements are sorted from highest to lowest error,
# and then the elements with the largest error that sum to R_ERROR_FRACTION
# multiplied by the total error are refined.
R_ERROR_FRACTION = 0.3

# The upper limit of statistical relative error - elements with a relative error larger
# then R_STAT_ERROR will not be refined.
R_STAT_ERROR = 1e-2

# The lower limit of statistical relative error - elements with a relative error larger
# then C_STAT_ERROR will be coarsened.
C_STAT_ERROR = 1e-1
