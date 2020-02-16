def getval(s):
    if s in f:
        return f[s]
    key.append(s)
    f[s] = len(key) - 1
    return f[s]
    

n = int(input())
key = []
f = dict()
for _ in range(n):
    m = int(input())
    f.clear(); key.clear()
    l = []
    for _ in range(m):
        s = str(input())
        s = s.rstrip()
        if s == "PUSH":
            l.append(getval(frozenset()))
            print(len(key[getval(frozenset())]))
        elif s == "DUP":
            t = l.pop()
            print(len(key[t]))
            l.append(t), l.append(t)
        elif s == "UNION":
            t = key[l.pop()]; t1 = key[l.pop()]
            t = t.union(t1)
            print(len(key[getval(t)]))
            l.append(getval(t))
        elif s == "INTERSECT":
            t = key[l.pop()]; t1 = key[l.pop()]
            t = t.intersection(t1)
            print(len(key[getval(t)]))
            l.append(getval(t))
        elif s == "ADD":
            t = key[l.pop()]; t1 = key[l.pop()]
            t2 = set()
            for i in t1:
                t2.add(i)
            t2.add(getval(t))
            t2 = frozenset(t2)
            print(len(key[getval(t2)]))
            l.append(getval(t2))
    print('***')