#include <bits/stdc++.h>
#define INF 1000000000
#define MAXN 20005
using namespace std;
typedef long long ll;
typedef vector<vector<long>> vv;
typedef vector<set<long>> vi;
typedef pair<long,long> ii;

vi final;
long cc  = 0;

long relabel(long i, long j) {
    return 9 * i + j;
}

void findneighbours(vv &neigh) {
    vector<set<long>> s(81);
    for (long r = 0; r < 9; r++) {
        for (long c = 0; c < 9; c++) {
            long src = relabel(r,c);
            for (long i = 0; i < 9; i++) {
                if (i != c && !s[src].count(relabel(r,i))) {
                    neigh[src].push_back(relabel(r,i));
                    s[src].insert(relabel(r,i));
                }
                if (i != r && !s[src].count(relabel(i,c))) {
                    neigh[src].push_back(relabel(i,c));
                    s[src].insert(relabel(i,c));
                }  
            }
            long new_s = 27 * (r / 3) + 3 * (c / 3);
            for (long i = 0; i < 3; i++) {
                for (long j = 0; j < 3; j++) {
                    if (new_s + relabel(i,j) != src && !s[src].count(new_s + relabel(i,j))) {
                        neigh[src].push_back(new_s + relabel(i,j));
                        s[src].insert(new_s + relabel(i,j));
                    }
                }
            }
        }
    }
}

bool forward_check(vv &neigh, vi &dom, long idx, long val) {
    for (long &i : neigh[idx]) {
        set<long> sub_d = dom[i];
        if (sub_d.count(val)) {
            sub_d.erase(val);
            if (sub_d.empty()) return false;
        }
        dom[i] = sub_d;
    }
    return true;
}

bool revise(long u, long v, vi &dom) {
    set<long> sub_d = dom[u];
    bool res = false;
    for (auto it = dom[u].begin(); it != dom[u].end(); it++) {
        long i = *it;
        if ((long)(dom[v].size()) == 1 && dom[v].count(i)) {
            sub_d.erase(i);
            res = true;
            break;
        }
    }
    dom[u] = sub_d;
    return res;
}

bool AC3(vi &dom, vv &neigh) {
    queue<ii> q;
    for (long i = 0; i < 81; i++) {
        for (long &j : neigh[i]) q.push({i,j});
    }
    while (!q.empty()) {
        long u = q.front().first, v = q.front().second;
        q.pop();
        if (revise(u,v,dom)) {
            if (dom[u].empty()) return false;
            for (long &i : neigh[u]) {
                if (i != v && (long)(dom[u].size()) == 1) q.push({i,u});
            }
        }
    }
    return true;
}

bool eval(vi &dom) {
    for (long i = 0; i < 81; i++) {
        if ((long)(dom[i].size()) != 1) return false;
    }
    return true;
}

long mcv(vi &dom) {
    long m = LONG_MAX, idx = -1;
    for (long i = 0; i < 81; i++) {
        if ((long)(dom[i].size()) > 1 && (long)(dom[i].size()) < m) {
            m = (long)(dom[i].size());
            idx = i;
        }
    }
    return idx;
}

bool memo(vv &neigh, vi &dom) {
    if (eval(dom)) return true;
    long i = mcv(dom);
    for (auto it = dom[i].begin(); it != dom[i].end(); it++) {
        long j = *it;
        set<long> s; s.insert(j);
        vi d = dom; d[i] = s;
        bool p = forward_check(neigh, d, i, j);
        if (p) {
            bool p2 = AC3(d, neigh);
            if (p2) {
                bool res = memo(neigh, d);
                if (res) {
                    if (!cc) final = d;
                    if (cc == 2) return true;
                    cc++;
                }
            }
        }
    }
    return false;
}

void solve(vv &puzzle) {
    vv neigh(81); vi dom(81);
    for (long i = 0; i < 81; i++) {
        if (puzzle[i / 9][i % 9] == 0) {
            for (long j = 1; j < 10; j++) dom[i].insert(j);
        } else dom[i].insert(puzzle[i / 9][i % 9]);
    }
    findneighbours(neigh);
    bool res = memo(neigh, dom);
    if (cc == 1) {
        for (long i = 0; i < 81; i++) {
            puzzle[i / 9][i % 9] = *(final[i].begin());
        }
        for (long i = 0; i < 9; i++) {
            for (long j = 0; j < 9; j++) {
                cout << puzzle[i][j] << " ";
            }
            cout << '\n';
        }
    } else if (cc == 2) {
        cout << "Non-unique" << '\n';
    } else cout << "Find another job" << '\n';
    cout << '\n';
}

int main() {
    long f;
    while (cin >> f, !cin.eof()) {
        cc = 0;
        bool ac = false;
        vv puzzle(9, vector<long>(9));
        puzzle[0][0] = f;
        if (!f) ac = true;
        for (long i = 0; i < 9; i++) {
            for (long j = 0; j < 9; j++) {
                if (!i && !j) continue;
                cin >> puzzle[i][j];
                if (!puzzle[i][j]) ac = true;
            }
        }
        if (ac) {
            solve(puzzle);
        } else {
            for (long i = 0; i < 9; i++) {
                for (long j = 0; j < 9; j++) cout << puzzle[i][j] << " ";
                cout << '\n';
            }
            cout << '\n';
        }
    }
}