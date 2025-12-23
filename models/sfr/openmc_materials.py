import openmc

MATERIAL_COMP = {
  'outer_fuel': {
    'density': 10.0,
    'percent_type' : 'wo',
    'composition': {
      "U235": 0.0018,
      "U238": 0.73,
      "Pu238": 0.0053,
      "Pu239": 0.0711,
      "Pu240": 0.0445,
      "Pu241": 0.0124,
      "Pu242": 0.0156,
      "Am241": 0.0017,
      "O16": 0.1176
    }
  },
  'inner_fuel': {
    'density': 10.0,
    'percent_type' : 'wo',
    'composition': {
      "U235": 0.0019,
      "U238": 0.7509,
      "Pu238": 0.0046,
      "Pu239": 0.0612,
      "Pu240": 0.0383,
      "Pu241": 0.0106,
      "Pu242": 0.0134,
      "Am241": 0.001,
      "O16": 0.1181
    }
  },
  'cladding': {
    'density': 10.0,
    'percent_type' : 'ao',
    'composition': {
      "Cu63": 0.9908,
      "O16": 0.00551,
      "O17": 2.09212e-6,
      "Al27": 0.0037
    }
  },
  'sodium': {
    'density': 0.96,
    'percent_type' : 'ao',
    'composition': {
      "Na23": 1.0
    }
  },
  'helium': {
    'density': 0.001598,
    'percent_type' : 'ao',
    'composition': {
        "He3": 4.81e-10,
        "He4": 0.00024,
    }
  }
}

MATERIALS = {}
for name, material_dict in MATERIAL_COMP.items():
  MATERIALS[name] = openmc.Material(name = name)
  MATERIALS[name].set_density('g/cm3', material_dict['density'])
  for nuclide, percent in material_dict['composition'].items():
    MATERIALS[name].add_nuclide(nuclide, percent=percent, percent_type=material_dict['percent_type'])
