from typing import List

import networkx as nx
import math

def heuristic(g: nx.Graph, cur_node_idx: int, next_node_idx: int) -> float:
  cur_next_dist = g[cur_node_idx][next_node_idx]['weight']
  return cur_next_dist


def sls(g: nx.Graph) -> List[int]:
  solution = [0]
  visited = {0}
  last_node = 0
  while len(solution) != len(g.nodes):
    min_node = None
    min_score = math.inf
    for node in g.nodes:
      if node in visited:
        continue
      score = heuristic(g, last_node, node)
      if score < min_score:
        min_node = node
        min_score = score

    visited.add(min_node)
    solution.append(min_node)
    last_node = min_node
  return solution
