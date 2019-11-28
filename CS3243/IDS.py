import os
import sys

pred = {}; action = {} 
explored = set()

def inbound(i, j):
    return i >= 0 and j >= 0 and i < 3 and j < 3

def get_neighbours(s):
    r = -1; c = -1
    found = False
    neighbour = []
    state = list(map(list, s))
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                r = i; c = j
                found = True
                break
        if found:
            break

    move = [(1,0), (-1,0), (0,1), (0,-1)]
    for i in range(len(move)):
        newr = r + move[i][0]; newc = c + move[i][1]
        if inbound(newr,newc):
            state[newr][newc], state[r][c] = state[r][c], state[newr][newc]
            neighbour.append((tuple(map(tuple,state)), i))
            state[newr][newc], state[r][c] = state[r][c], state[newr][newc]
    return neighbour

def get_command(index):
    if index == 0:
        return "UP"
    if index == 1:
        return "DOWN"
    if index == 2:
        return "LEFT"
    if index == 3:
        return "RIGHT"

def ids(state, prev_state, index, d, maxd, g_state, o_state):
    if state != o_state: 
        pred[state] = prev_state
        action[state] = get_command(index)
    explored.add(state)
    if state == g_state:
        return True
    if d >= maxd:
        return False
    neighbours = get_neighbours(state)
    for i in neighbours:
        n = i[0]
        index = i[1]
        if (n not in explored and ids(n, state, index, d + 1, maxd, g_state, o_state)):
            return True
    return False

class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # You may add more attributes as necessary
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()
        self.solvable = True

    def solve(self):
        #TODO: Write your code here
        # return: a list of actions like: ["UP", "DOWN"]
        o_state = tuple(map(tuple, self.init_state))
        g_state = tuple(map(tuple, self.goal_state))
        maxd = 29
        ac = False
        for i in range(1, maxd + 1):
            if (ids(o_state, o_state, -1, 0, i, g_state, o_state)):
                ac = True
                break
            pred.clear()
            action.clear()
            explored.clear()
        if ac:
            state = g_state
            while state != o_state:
                self.actions.append(action[state])
                state = pred[state]
            self.actions.reverse()
            print(len(self.actions))
        else:
            self.actions.append("UNSOLVABLE")
        return self.actions
        pass

init_state = [[7,0,5], [2,6,8], [4,3,1]]
goal_state = [[1,2,3], [4,5,6], [7,8,0]]
puzzle = Puzzle(init_state, goal_state)
ans = puzzle.solve()
print(ans)