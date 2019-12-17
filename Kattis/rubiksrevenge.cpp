#include <bits/stdc++.h>
#define CONST 4
using namespace std;
#define rep(i,x,y) for (long i = (x); i < (y); i++)
typedef vector<string> vv;
typedef pair<vv, long> ii;

void rl(vv &s, long i) {
    long j;
    char t = s[i][0];
    rep(j,0,CONST) {
        if (j != CONST - 1) {
            s[i][j] = s[i][j + 1];
        } else s[i][j] = t;
    }
}

void rr(vv &s, long i) {
    string t = s[i];
    long j; 
    rep(j,0,CONST) {
        if (j) {
            s[i][j] = t[j - 1];
        } else s[i][j] = t[CONST - 1];
    }
}

void cu(vv &s, long i) {
    long j;
    char t = s[0][i];
    rep(j,0,CONST) {
        if (j != CONST - 1) {
            s[j][i] = s[j + 1][i];
        } else s[j][i] = t;
    }
}

void cd(vv &s, long i) {
    long j;
    vector<char> t;
    rep(j,0,CONST) t.push_back(s[j][i]);
    rep(j,0,CONST) {
        if (j) {
            s[j][i] = t[j - 1];
        } else s[j][i] = t[CONST - 1];
    }
}

int main() {
    vv c(CONST), f(CONST);
    unordered_map<string, long> m;
    unordered_map<long, long> pred, d;
    long i, j, k = 0;
    rep(i,0,CONST) cin >> c[i];
    rep(i,0,CONST) {
        f[i] = "RRRR";
        rep(j,0,CONST) {
            if (!i) {
                f[i][j] = 'R';
            } else if (i == 1) {
                f[i][j] = 'G';
            } else if (i == 2) {
                f[i][j] = 'B';
            } else f[i][j] = 'Y';
        }
    }
    bool ac = false;
    long r = LONG_MAX;
    string r1 = "", r2 ="";
    rep(i,0,CONST) r1 += c[i];
    rep(i,0,CONST) r2 += f[i];
    if (r1 == r2) {
        cout << 0;
        return 0;
    }
    m[r1] = k++, m[r2] = k++;
    d[0] = 0, d[1] = 0;
    pred[0] = 0, pred[1] = 1;
    queue<ii> q;
    q.push({c, 0}), q.push({f, 1});
    while (!q.empty() && !ac) {
        vv u = q.front().first;
        string us = "";
        rep(i,0,CONST) us += u[i];
        long s = q.front().second;
        q.pop();
        rep(i,0,CONST) {
            vv t = u;
            rep(j, 0, CONST) { 
                vv t = u;
                if (!j) {
                    rl(t,i);
                } else if (j == 1) {
                    rr(t,i);
                } else if (j == 2) {
                    cu(t,i);
                } else cd(t,i);
                string ts = "";
                long z;
                rep(z,0,CONST) ts += t[z];
                if (!m.count(ts)) {
                    m[ts] = k++;
                    pred[k - 1] = s;
                    d[k - 1] = d[m[us]] + 1;
                    q.push({t, s});
                } else if (pred[m[ts]] != pred[m[us]]) {
                    r = d[m[ts]] + d[m[us]] + 1;
                    ac = true;
                    break;
                }
            }
            if (ac) break;
        }
    }
    cout << r;
}