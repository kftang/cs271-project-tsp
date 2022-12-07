import argparse
import sys
from pathlib import Path

import networkx as nx
import numpy as np

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('input_file', type=str)
  parser.add_argument('-s', help='sls algorithm', type=bool)
  
  # parse args to find file
  args = parser.parse_args()
  input_path = Path(args.input_file)
  if not input_path.exists():
    print(f'Input file {input_file} does not exist')
    sys.exit()

  # parse input file
  with input_path.open() as input_file:
    num_nodes = int(input_file.readline())
    adj_matrix = np.empty((num_nodes, num_nodes))
    for i in range(num_nodes):
      adj_matrix[i] = list(map(float, input_file.readline().split()))

  graph = nx.from_numpy_array(adj_matrix)
