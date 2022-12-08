import argparse
import sys
from pathlib import Path

import networkx as nx
import numpy as np

from sls import sls

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('input_file', type=str)
  parser.add_argument('-s', help='sls algorithm', action='store_true')
  
  # parse args to find file
  args = parser.parse_args()
  input_path = Path(args.input_file)
  if not input_path.exists():
    print(f'Input file {args.input_file} does not exist')
    sys.exit()

  # parse input file
  with input_path.open() as input_file:
    num_nodes = int(input_file.readline())
    adj_matrix = np.empty((num_nodes, num_nodes))
    for i in range(num_nodes):
      distances = map(float, input_file.readline().split())
      for j, distance in enumerate(distances):
        adj_matrix[i][j] = distance

  g = nx.from_numpy_array(adj_matrix)

  opt_path = nx.approximation.traveling_salesman_problem(g, cycle=False)
  print(f'Optimal path: {opt_path}')
  opt_cost = nx.path_weight(g, opt_path, 'weight')
  print(f'Cost: {opt_cost}')

  if args.s:
    path = sls(g)
    print(f'Found path: {path}')
    cost = nx.path_weight(g, path, 'weight')
    print(f'Cost: {cost}')
