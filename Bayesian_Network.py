import sys
import json
import copy
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q

class State():
    def __init__(self, lhs, rhs, cpt):
        self.lhs = lhs
        self.rhs = rhs
        self.cpt = cpt

    def multiply (self, other):
        res = State(set(), set(), [])
        res.lhs = self.lhs.union(other.lhs)
        res.rhs = self.rhs.union(other.rhs)
        res.rhs = res.rhs.difference(res.lhs)
        commonVar = (self.lhs.union(self.rhs)).intersection(other.lhs.union(other.rhs))
        newCpt = []
        for i in self.cpt:
            for j in other.cpt:
                add = True
                for k in commonVar:
                    if i[k] != j[k]:
                        add = False
                        break

                if add:
                    r_entry = dict()
                    for (key, val) in i.items():
                            r_entry[key] = val

                    for (key, val) in j.items():
                            r_entry[key] = val

                    r_entry["probability"] = i["probability"] * j["probability"]
                    newCpt.append(r_entry)

        res.cpt = newCpt
        return res
    
    def eliminate(self, v):
        visited = list(); newCpt = list()
        for i in range(len(self.cpt)):
            visited.append(False)
        
        for i in range(len(self.cpt)):
            if visited[i]:
                continue

            new_entry = dict()
            for (var, val) in self.cpt[i].items():
                new_entry[var] = val

            for j in range(i + 1, len(self.cpt)):
                add = True
                for var in self.cpt[i].keys():
                    if self.cpt[i][var] != self.cpt[j][var] and var != v and var != "probability":
                        add = False
                        break
                
                if add:
                    new_entry["probability"] += self.cpt[j]["probability"]
                    visited[j] = True

            visited[i] = True
            newCpt.append(new_entry)
        
        self.lhs.remove(v)
        self.cpt = newCpt
        return self
    
    def normalize(self, query):
        num = 0; denom = 0
        for i in self.cpt:
            res = True
            for (var,val) in query["given"].items():
                if i[var] != val:
                    res = False
                    break

            for (var, val) in query["tofind"].items():
                if i[var] != val:
                    res = False
                    break
            
            if res:
                num = i["probability"]
                break
        
        for i in self.cpt:
            add = True
            for (var, val) in query["given"].items():
                if i[var] != val:
                    add = False
                    break
            
            if add:
                denom += i["probability"]
        
        return num / denom

class BayesianNetwork(object):
    def __init__(self, structure, values, queries):
        # you may add more attributes if you need
        self.variables = structure["variables"]
        self.dependencies = structure["dependencies"]
        self.conditional_probabilities = values["conditional_probabilities"]
        self.prior_probabilities = values["prior_probabilities"]
        self.queries = queries
        self.answer = []
        self.children = dict()

    def construct(self):
        # TODO: Your code here to construct the Bayesian network
        for i in self.variables.keys():
            self.children[i] = 0
    
        for (var,table) in self.dependencies.items():
            for j in table:
                self.children[j] += 1

        for (var,table) in self.conditional_probabilities.items():
            for entry in table:
                entry[var] = entry["own_value"]
                del entry["own_value"]
        
        for (var, val) in self.prior_probabilities.items():
            self.conditional_probabilities[var] = []
            for (state, num) in val.items():
                new_entry = dict()
                new_entry[var] = state
                new_entry["probability"] = num
                self.conditional_probabilities[var].append(new_entry)
        
        pass

    def infer(self):
        # TODO: Your code here to answer the queries given using the Bayesian
        # network built in the construct() method.
        self.answer = []  # your code to find the answer
        for i in self.queries:
            a_dict = dict()
            a_dict["index"] = i["index"]
            a_dict["answer"] = self.solve(i)
            self.answer.append(a_dict)

        # for the given example:
        # self.answer = [{"index": 1, "answer": 0.01}, {"index": 2, "answer": 0.71}]
        # the format of the answer returned SHOULD be as shown above.
        return self.answer

    def solve(self, i):
        visited = set(); initial = set()
        factors = []
        for j in i["given"].keys():
            visited.add(j); initial.add(j)
        for j in i["tofind"].keys():
            visited.add(j); initial.add(j)

        self.bfs(visited)
        eliminate = visited.difference(initial)
        for j in visited:
            lhs = set(); rhs = set(); cpt = []
            lhs.add(j)
            if j in self.dependencies.keys():
                for k in self.dependencies[j]:
                    rhs.add(k)
            cpt = copy.copy(self.conditional_probabilities[j])
            factors.append(State(lhs, rhs, cpt))

        self.order_eliminate(factors, eliminate)
        return self.evaluate(factors, i)  

    def bfs(self, visited):
        q = Q.Queue()
        for i in visited:
            q.put(i)
        while not q.empty():
            u = q.get()
            if u not in self.dependencies:
                continue
            for i in self.dependencies[u]:
                if i not in visited:
                    visited.add(i)
                    q.put(i)
    
    def order_eliminate(self, factors, eliminate):
        pq = Q.PriorityQueue()
        for i in eliminate:
            pq.put((self.children[i], i))

        while not pq.empty():
            u = pq.get()
            v = u[1]
            r_factors = list()
            for i in factors:
                if v in i.rhs or v in i.lhs:
                    r_factors.append(i)

            for i in r_factors:
                factors.remove(i)

            factors.append(self.sum_out(r_factors, v))
        
    def sum_out(self, r_factors, v):
        result = r_factors[0]
        for i in range(1, len(r_factors)):
            result = result.multiply(r_factors[i])
        result = result.eliminate(v)
        return result

    def evaluate(self, factors, query):
        result = factors[0]
        for i in range(1, len(factors)):
            result = result.multiply(factors[i])
        return result.normalize(query)    

    # You may add more classes/functions if you think is useful. However, ensure
    # all the classes/functions are in this file ONLY and used within the
    # BayesianNetwork class.

def main():
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 4:
        print ("\nUsage: python b_net_A3_xx.py structure.json values.json queries.json \n")
        raise ValueError("Wrong number of arguments!")

    structure_filename = sys.argv[1]
    values_filename = sys.argv[2]
    queries_filename = sys.argv[3]

    try:
        with open(structure_filename, 'r') as f:
            structure = json.load(f)
        with open(values_filename, 'r') as f:
            values = json.load(f)
        with open(queries_filename, 'r') as f:
            queries = json.load(f)

    except IOError:
        raise IOError("Input file not found or not a json file")

    # testing if the code works
    b_network = BayesianNetwork(structure, values, queries)
    b_network.construct()
    answers = b_network.infer()
    for i in answers:
        print(i)

if __name__ == "__main__":
    main()
