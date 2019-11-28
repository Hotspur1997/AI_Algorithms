# Marc Phua Hsiao Meng A0183219A
# Rishi Mahadevan A0184318B
import sys
import copy
import collections
import time
count = 0

def relabel(i,j):
    return 9 * i + j

def findneighbours(neigh):
    for r in range(9):
        for c in range(9):
            s = relabel(r,c)
            for i in range(9):
                if i != c:
                    neigh[s].add(relabel(r,i))
                if i != r:
                    neigh[s].add(relabel(i,c))
            src = 27 * (r // 3) + 3 * (c // 3)
            for i in range(3):
                for j in range(3):
                    if src + relabel(i,j) != s:
                        neigh[s].add(src + relabel(i,j))      

def forward_check(neigh, dom, idx, val):
    for i in neigh[idx]:
        sub_domain = copy.copy(dom[i])
        if val in sub_domain:
            sub_domain.remove(val)
            if len(sub_domain) == 0:
                return False
        dom[i] = sub_domain
    return True
    
def revise(u, v, dom):
   sub_domain = copy.copy(dom[u])
   res = False
   for i in dom[u]:
       if len(dom[v]) == 1 and i in dom[v]:
           sub_domain.remove(i)
           res = True
   dom[u] = sub_domain
   return res

def AC3(dom, neigh):
    q = collections.deque()
    for i in range(81):
        for j in neigh[i]:
            q.append([i, j])
    while q:
       u,v = q.popleft()
       if revise(u,v,dom):
           if len(dom[u]) == 0:
               return False
           for i in neigh[u]:
               if i != v:
                   q.append([i,u])
    return dom

def backtrack(neigh, dom):
    global count
    if dom is False:
        return False
    if all(len(i) == 1 for i in dom):
        return dom
    n,i = min((len(dom[i]), i) for i in range(81) if len(dom[i]) > 1)
    for j in dom[i]:
        d = copy.copy(dom)
        s  = set(); s.add(j)
        d[i] = s
        p = forward_check(neigh, d, i, j)
        if p:
            res = backtrack(neigh, AC3(d, neigh))
            if res is not False:
                return res
    count += 1        
    return False
        
class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists

    def solve(self):
        #TODO: Your code here
        start = time.time()
        neighbours = []
        domain = []
        for i in range(81):
            domain.append(set())
            neighbours.append(set())
            if self.ans[i // 9][i % 9] == 0:
                for j in range(1,10):
                    domain[i].add(j)
            else:
                domain[i].add(self.ans[i // 9][i % 9])
        findneighbours(neighbours)
        domain = backtrack(neighbours, domain)
        for i in range(81):
            self.ans[i // 9][i % 9] = domain[i].pop()
        end = time.time()
        print(end - start)  
        print(count)  
        # don't print anything here. just resturn the answer
        # self.ans is a list of lists
        return self.ans
    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY

if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python sudoku_A2_xx.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python sudoku_A2_xx.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
