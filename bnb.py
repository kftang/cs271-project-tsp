import math
from functools import total_ordering
from queue import PriorityQueue
from typing import List

import networkx as nx

@total_ordering
class SolutionState:
  path: List[int]
  depth: int
  bound: float

  def __init__(self, path: List[int] = [0], depth: int = 0, bound: float = 0) -> None:
    self.path = path
    self.depth = depth
    self.bound = bound

  def __eq__(self, other: 'SolutionState') -> bool:
    return self.bound == other.bound

  def __lt__(self, other: 'SolutionState') -> bool:
    return self.bound > other.bound

def find_bound(g: nx.Graph, state: SolutionState) -> float:
  bound = nx.path_weight(g, state.path, 'weight')
  unvisited_nodes = list(filter(lambda node: node not in state.path, g.nodes))
  last_node = state.path[-1]

  # use greedy choice to find edge for last node in the path
  bound += min([g[last_node][node]['weight'] for node in unvisited_nodes])

  # leftover edges to consider
  leftover = [*unvisited_nodes, state.path[0]]
  for node in unvisited_nodes:
    bound += min([g[node][leftover_node]['weight'] for leftover_node in leftover if leftover_node != node])

  return bound

def bnb(g: nx.Graph) -> List[int]:
  optimal_path = []

  # use priority queue to work on states with the best bound
  queue: PriorityQueue[SolutionState] = PriorityQueue()

  min_cost = math.inf

  # start at initial state
  init_state = SolutionState()
  init_state.bound = find_bound(g, init_state)
  queue.put(init_state)

  next_state = SolutionState()

  max_iterations = 1000
  i = 0

  while not queue.empty():
    if i > max_iterations:
      break
    i += 1

    state = queue.get()
    if state.bound < min_cost:
      next_state.depth = state.depth + 1
      for node in g.nodes:
        if node in state.path:
          continue
        next_state.path = [*state.path, node]

        # complete path found
        if next_state.depth == len(g.nodes) - 2:
          remaining_node = list(set(g.nodes) - set(next_state.path))[0]
          next_state.path = [*next_state.path, remaining_node]
          cost = nx.path_weight(g, next_state.path, 'weight')
          if cost < min_cost:
            min_cost = cost
            optimal_path = next_state.path
        else:
          next_state.bound = find_bound(g, next_state)
          if next_state.bound < min_cost:
            queue.put(next_state)
      # reset next solution state to find
      next_state = SolutionState(depth=next_state.depth)

  return optimal_path
