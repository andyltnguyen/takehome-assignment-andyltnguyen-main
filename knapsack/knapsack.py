# -------------------------------------------------
# File for Tasks A and B
# Class for knapsack
# PLEASE UPDATE THIS FILE
#
# __author__ = 'Edward Small'
# __copyright__ = 'Copyright 2025, RMIT University'
# -------------------------------------------------

import csv
from maze.maze import Maze


class Knapsack:
    """
    Base class for the knapsack.
    """

    def __init__(self, capacity: int, knapsackSolver: str):
        """
        Constructor.

        @param capacity: the maximum weight the knapsack can hold
        @param knapsackSolver: the method we wish to use to find optimal knapsack items (recur or dynamic)
        """
        # initialise variables
        self.capacity = capacity
        self.optimalValue = 0
        self.optimalWeight = 0
        self.optimalCells = []
        self.knapsackSolver = knapsackSolver

    def solveKnapsack(self, maze: Maze, filename: str):
        """
        Calls the method to calculate the optimal knapsack solution
        @param maze: The maze we are considering
        """
        map = []
        # Sort by row (i) first, then column (j)
        sorted_items = sorted(maze.m_items.items(), key=lambda item: (item[0][0], item[0][1]))

        for cell, (weight, value) in sorted_items:
            map.append([cell, weight, value])

        if self.knapsackSolver == "recur":
            self.optimalCells, self.optimalWeight, self.optimalValue = self.recursiveKnapsack(map,
                                                                                              self.capacity,
                                                                                              len(map),
                                                                                              filename)
        elif self.knapsackSolver == "dynamic":
            self.optimalCells, self.optimalWeight, self.optimalValue = self.dynamicKnapsack(map,
                                                                                            self.capacity,
                                                                                            len(map),
                                                                                            filename)

        else:
            raise Exception("Incorrect Knapsack Solver Used.")

    def recursiveKnapsack(self, items: list, capacity: int, num_items: int, filename: str = None,
                        stats={'count': 0, 'logged': False}):
        """
        Recursive 0/1 Knapsack that logs how many times it's been called
        when the base case is first hit.
        """
        # Only increment if we're still counting
        if not stats['logged']:
            stats['count'] += 1

        # Base case
        if capacity == 0 or num_items == 0:
            if not stats['logged'] and filename:
                with open(filename + '.txt', "w") as f:
                    f.write(str(stats['count']))  # Only log the first base case
                stats['logged'] = True
            return [], 0, 0

        # Get current item
        location, weight, value = items[num_items - 1]

        # Case 1: Cannot take this item
        if weight > capacity:
            return self.recursiveKnapsack(items, capacity, num_items - 1, filename, stats)

        # Case 2: Include the item
        Linc, winc, vinc = self.recursiveKnapsack(
            items, capacity - weight, num_items - 1, filename, stats)
        Linc = Linc + [location]
        winc += weight
        vinc += value

        # Case 3: Exclude the item
        Lexc, wexc, vexc = self.recursiveKnapsack(
            items, capacity, num_items - 1, filename, stats)

        # Choose better
        if vinc > vexc:
            return Linc, winc, vinc
        else:
            return Lexc, wexc, vexc

    def dynamicKnapsack(self, items: list, capacity: int, num_items: int, filename: str):
        """
        Dynamic 0/1 Knapsack using recursive memoization (top-down DP).
        Saves the dynamic programming table as a csv.
        """

        dp = [[None] * (capacity + 1) for _ in range(num_items + 1)]
        dp[0] = [0] * (capacity + 1)  # Fully initialize base case


        def memo(i, c):
            if dp[i][c] is not None:
                return dp[i][c]

            if i == 0 or c == 0:
                dp[i][c] = 0
                return 0

            weight = items[i - 1][1]
            value = items[i - 1][2]

            if weight > c:
                dp[i][c] = memo(i - 1, c)
            else:
                dp[i][c] = max(memo(i - 1, c), memo(i - 1, c - weight) + value)

            return dp[i][c]

        # Only start recursion from final state — no full-table loop
        memo(num_items, capacity)

        # Backtrack to find selected items
        selected_items = []
        selected_weight = 0
        cap = capacity
        for i in range(num_items, 0, -1):
            if dp[i][cap] is None or dp[i][cap] == dp[i - 1][cap]:
                continue
            location, weight, value = items[i - 1]
            selected_items.append(location)
            selected_weight += weight
            cap -= weight

        selected_items.reverse()
        max_value = dp[num_items][capacity]

        # Save to CSV
        self.saveCSV(dp, items, capacity, filename)

        return selected_items, selected_weight, max_value


    def saveCSV(self, dp: list, items: list, capacity: int, filename: str):
        with open(filename+".csv", 'w', newline='') as f:
            writer = csv.writer(f)

            # Header: capacities from 0 to capacity
            header = [''] + [str(j) for j in range(capacity + 1)]
            writer.writerow(header)

            # First row: dp[0], meaning "no items considered"
            first_row = [''] + [(val if val is not None else '#') for val in dp[0]]
            writer.writerow(first_row)

            # Following rows: each item
            for i in range(1, len(dp)):
                row_label = f"({items[i - 1][1]}, {items[i - 1][2]})"
                row = [row_label] + [(val if val is not None else '#') for val in dp[i]]
                writer.writerow(row)

