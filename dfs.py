#!/usr/bin/python

import sys

import numpy as np
from copy import copy, deepcopy
import queue

frontier = queue.LifoQueue()
grids = set()

class State:
    def __init__(self, parent, grid, children, cost):
        self.grid = grid
        self.cost = cost
        self.parent = parent 
        self.children = children
    
    def read_puzzle(self, id):
        file = "puzzle2.txt"
        row = 0
        self.grid = [[0 for x in range(4)] for y in range(5)] 
        if id == 1:
            file = "puzzle1.txt"
        f = open(file, "r")
        for x in f:
            for j in range(0,4):
                self.grid[row][j] = int(x[j])
            row += 1
    
    def is_goal(self):
        return self.grid[3][1] == self.grid[3][2] == self.grid[4][1] == self.grid[4][2] == 1

    def set_child(self, cost, grid):
        result = ''
        for i in range(0,5):
            for j in range(0,4):
                result += str(grid[i][j])
        if result not in grids:
            childState = State(self, grid, set(), cost)
            grids.add(result)
            frontier.put(childState)
            # heapq.heappush(frontier, (childState.cost + childState.h_value, childState))
            self.children.add(childState)

    def get_successors(self):
        empty_spaces = [(ix,iy) for ix, row in enumerate(self.grid) for iy, i in enumerate(row) if i == 0]
        aCell = empty_spaces[0]
        bCell = empty_spaces[1]
        pos_vertical = aCell[1] == bCell[1] and abs(aCell[0] - bCell[0]) == 1
        pos_horizontal = aCell[0] == bCell[0] and abs(aCell[1] - bCell[1]) == 1

        soliders = [(ix,iy) for ix, row in enumerate(self.grid) for iy, i in enumerate(row) if i == 7]
        for solider in soliders:
            for cell in empty_spaces:
                if abs(solider[0] - cell[0]) + abs(solider[1] - cell[1]) == 1:
                    childGrid = deepcopy(self.grid)
                    childGrid[solider[0]][solider[1]] = 0
                    childGrid[cell[0]][cell[1]] = 7
                    self.set_child(self.cost + 1, childGrid)
        
        for hero_index in range(2, 7):
            hero_pos = [(ix,iy) for ix, row in enumerate(self.grid) for iy, i in enumerate(row) if i == hero_index]
            hero_higherPos = hero_pos[0]
            hero_lowerPos = hero_pos[1]
            
            for cell in empty_spaces:
                if (cell[1] == hero_higherPos[1]):
                    if abs(cell[0] - hero_higherPos[0]) == 2 and abs(cell[0] - hero_lowerPos[0]) == 1:
                        childGrid = deepcopy(self.grid)
                        childGrid[hero_higherPos[0]][hero_higherPos[1]] = 0
                        childGrid[cell[0]][cell[1]] = hero_index
                        self.set_child(self.cost + 1, childGrid)
                    
                    if abs(cell[0] - hero_lowerPos[0]) == 2 and abs(cell[0] - hero_higherPos[0]) == 1:
                        childGrid = deepcopy(self.grid)
                        childGrid[hero_lowerPos[0]][hero_lowerPos[1]] = 0
                        childGrid[cell[0]][cell[1]] = hero_index
                        self.set_child(self.cost + 1, childGrid)
                
                if cell[0] == hero_higherPos[0]:
                    if abs(cell[1] - hero_higherPos[1]) == 2 and abs(cell[1] - hero_lowerPos[1]) == 1:
                        childGrid = deepcopy(self.grid)
                        childGrid[hero_higherPos[0]][hero_higherPos[1]] = 0
                        childGrid[cell[0]][cell[1]] = hero_index
                        self.set_child(self.cost + 1, childGrid)

                    if abs(cell[1] - hero_lowerPos[1]) == 2 and abs(cell[1] - hero_higherPos[1]) == 1:
                        childGrid = deepcopy(self.grid)
                        childGrid[hero_lowerPos[0]][hero_lowerPos[1]] = 0
                        childGrid[cell[0]][cell[1]] = hero_index
                        self.set_child(self.cost + 1, childGrid)

            if pos_vertical and aCell[0] - hero_higherPos[0] == 0 and bCell[0] - hero_lowerPos[0] == 0 and abs(aCell[1] - hero_higherPos[1]) == 1 and abs(bCell[1] - hero_lowerPos[1]) == 1:
                childGrid = deepcopy(self.grid)
                childGrid[hero_higherPos[0]][hero_higherPos[1]] = 0
                childGrid[hero_lowerPos[0]][hero_lowerPos[1]] = 0
                childGrid[aCell[0]][aCell[1]] = hero_index
                childGrid[bCell[0]][bCell[1]] = hero_index
                self.set_child(self.cost + 1, childGrid)

            if pos_horizontal and abs(aCell[0] - hero_higherPos[0]) == 1 and abs(bCell[0] - hero_lowerPos[0]) == 1 and aCell[1] == hero_higherPos[1] and bCell[1] == hero_lowerPos[1]:
                childGrid = deepcopy(self.grid)
                childGrid[hero_higherPos[0]][hero_higherPos[1]] = 0
                childGrid[hero_lowerPos[0]][hero_lowerPos[1]] = 0
                childGrid[aCell[0]][aCell[1]] = hero_index
                childGrid[bCell[0]][bCell[1]] = hero_index
                self.set_child(self.cost + 1, childGrid)

        if pos_horizontal:
            valid_down = aCell[0] + 1 < 5
            valid_up =  aCell[0] - 1 >= 0
            if valid_down and self.grid[aCell[0]+1][aCell[1]] == 1 and self.grid[bCell[0]+1][bCell[1]] == 1:
                childGrid = deepcopy(self.grid)
                childGrid[aCell[0]+2][aCell[1]] = 0
                childGrid[bCell[0]+2][bCell[1]] = 0
                childGrid[aCell[0]][aCell[1]] = 1
                childGrid[bCell[0]][bCell[1]] = 1
                self.set_child(self.cost + 1, childGrid)
            
            if valid_up and self.grid[aCell[0]-1][aCell[1]] == 1 and self.grid[bCell[0]-1][bCell[1]] == 1:
                childGrid = deepcopy(self.grid)
                childGrid[aCell[0]-2][aCell[1]] = 0
                childGrid[bCell[0]-2][bCell[1]] = 0
                childGrid[aCell[0]][aCell[1]] = 1
                childGrid[bCell[0]][bCell[1]] = 1
                self.set_child(self.cost + 1, childGrid)

        if pos_vertical:
            valid_right = aCell[1] + 2 < 4
            valid_left =  aCell[1] - 2 >= 0
            if valid_right and self.grid[aCell[0]][aCell[1]+1] == 1 and self.grid[bCell[0]][bCell[1]+1] == 1:
                childGrid = deepcopy(self.grid)
                childGrid[aCell[0]][aCell[1]+2] = 0
                childGrid[bCell[0]][bCell[1]+2] = 0
                childGrid[aCell[0]][aCell[1]] = 1
                childGrid[bCell[0]][bCell[1]] = 1
                self.set_child(self.cost + 1, childGrid)

            if valid_left and self.grid[aCell[0]][aCell[1]-1] == 1 and self.grid[bCell[0]][bCell[1]-1] == 1:
                childGrid = deepcopy(self.grid)
                childGrid[aCell[0]][aCell[1]-2] = 0
                childGrid[bCell[0]][bCell[1]-2] = 0
                childGrid[aCell[0]][aCell[1]] = 1
                childGrid[bCell[0]][bCell[1]] = 1
                self.set_child(self.cost + 1, childGrid)
        return

def traceBack(goalState):
    results = []
    print('Cost of the solution: ' + str(goalState.cost))
    print()
    while goalState is not None:
        results.insert(0, np.array(goalState.grid))
        goalState = goalState.parent

    print('Number of states expanded: ' + str(len(grids)))
    print()
    print('Solution: ')
    print()
    count = 0
    for item in results:
        print(count)
        print_grid(item)
        count += 1

def print_grid(grid):
    result = ''
    for i in range(0,5):
        for j in range(0,4):
            result += str(grid[i][j])
        result += '\n'
    print(result)

def dfs():
    initial_grid = State(None, None, set(), 0)
    initial_grid.read_puzzle(int(sys.argv[1]))
    frontier.put(initial_grid)
    print("Initial state:")
    print_grid(initial_grid.grid)
    result = ''
    for i in range(0,5):
        for j in range(0,4):
            result += str(initial_grid.grid[i][j])
    grids.add(result)
    while frontier:
        currentState = frontier.get()
        if currentState.is_goal():
            traceBack(currentState)
            return
        else:
            currentState.get_successors()
    return 'No Solution'

dfs()