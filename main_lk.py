from src.layers.dynamic import dpm_simulator as simulator
from src.layers.static.info_layer import InfoLayer
from src.layers.utils import import_simulation


if __name__ == '__main__':
  sim_path = './simulations.json'
  configs = import_simulation(sim_path)

  print(configs[0].build_dict())
  temp = InfoLayer(**configs[0].build_dict())
  #temp.print_character_info()
  #temp.print_engraving_info()
  temp.print_layer_info()