# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Greedy maze solver for all entrance, exit pairs
#
# __author__ = <student name here>
# __copyright__ = 'Copyright 2025, RMIT University'
# -------------------------------------------------------------------


from maze.util import Coordinates
from maze.maze import Maze

from knapsack.knapsack import Knapsack
from itertools import permutations

from typing import List, Dict, Optional
from collections import deque

class TaskDSolver:
    def __init__(self, knapsack:Knapsack):
        self.m_solverPath: List[Coordinates] = []
        self.m_cellsExplored = 0 
        self.m_entranceUsed = None
        self.m_exitUsed = None
        self.m_knapsack = knapsack
        self.m_value = 0
        self.m_reward = float('-inf') 

    def reward(self):
        return self.m_knapsack.optimalValue - self.m_cellsExplored

    def solveMaze(self, maze: Maze, entrance: Coordinates, exit: Coordinates):
        self.m_knapsack.optimalCells = []
        self.m_knapsack.optimalValue = 0
        self.m_knapsack.optimalWeight = 0

        visited = set()
        parent = {}

        # --- Safely enter the maze ---
        start = None
        for neighbour in maze.neighbours(entrance):
            if not maze.hasWall(entrance, neighbour):
                start = neighbour
                break

        if not start:
            raise ValueError("No accessible cell from entrance!")

        queue = deque([start])
        visited.add(start)

        while queue:
            current = queue.popleft()
            self.m_solverPath.append(current)
            self.m_cellsExplored = len(set(self.m_solverPath))

            # Check for treasure at current cell
            if current in maze.m_items:
                weight, value = maze.m_items[current]
                if self.m_knapsack.optimalWeight + weight <= self.m_knapsack.capacity:
                    self.m_knapsack.optimalCells.append(current)
                    self.m_knapsack.optimalValue += value
                    self.m_knapsack.optimalWeight += weight

            # Exit if adjacent to defined exit cell
            if any(not maze.hasWall(current, nbr) and nbr == exit for nbr in maze.neighbours(current)):
                parent[exit] = current
                break

            for neighbour in maze.neighbours(current):
                if neighbour not in visited and not maze.hasWall(current, neighbour):
                    visited.add(neighbour)
                    parent[neighbour] = current
                    queue.append(neighbour)

        # --- Backtrack path from exit to start ---
        path = []
        node = exit
        while node != start:
            path.append(node)
            node = parent.get(node)
            if node is None:
                break
        path.append(start)
        path.reverse()

        self.m_solverPath = path
        self.m_cellsExplored = len(set(self.m_solverPath))
        self.m_entranceUsed = entrance
        self.m_exitUsed = exit
        self.m_reward = self.reward()




