import os
import sys
import Queue

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
            state[r][c], state[newr][newc] = state[newr][newc], state[r][c]
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
        ac = False
        q = Queue.Queue()
        pred = {}; action = {} 
        explored = set()
        explored.add(o_state)
        q.put(o_state)
        m = -1
        while not q.empty():
           m = max(m, q.qsize())
           u = q.get()
           neighbours = get_neighbours(u)
           for p in neighbours:
               n = p[0]
               command = get_command(p[1])
               if n not in explored:
                   explored.add(n)
                   pred[n] = u
                   action[n] = command
                   if n == g_state:
                       ac = True
                       break
                   q.put(n)
           if ac:
                break
        print(len(explored))
        print(m)
        if ac:
            state = g_state
            while state != o_state:
                self.actions.append(action[state])
                state = pred[state]
            self.actions.reverse()
        else:
            self.actions.append("UNSOLVABLE")
        return self.actions
        pass
    # You may add more (helper) methods if necessary.
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.

if __name__ == "__main__":
    # do NOT modify below
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    init_state = [[0 for i in range(3)] for j in range(3)]
    goal_state = [[0 for i in range(3)] for j in range(3)]
    lines = f.readlines()

    i,j = 0, 0
    for line in lines:
        for number in line:
            if '0'<= number <= '8':
                init_state[i][j] = int(number)
                j += 1
                if j == 3:
                    i += 1
                    j = 0

    for i in range(1, 9):
        goal_state[(i-1)//3][(i-1)%3] = i
    goal_state[2][2] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')







