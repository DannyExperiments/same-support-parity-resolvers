from collections import defaultdict
from fractions import Fraction as F

adj = dict(S=('S','D1','D2'), R=('R','D1'), D1=('D1',), D2=('D2',))
colour = dict(S=2,R=1,D1=0,D2=0)
for uniform in (False,True):
    law = {'S':F(1,2),'R':F(1,2)}
    for n in range(25):
        block = defaultdict(F)
        for q, mass in law.items():
            for dest in ('S','R'):
                block[colour[q],dest] += mass/2
        observed = [sum(block[p,d] for d in ('S','R')) for p in range(3)]
        assert observed[1] == F(1,2)**(n+1)
        assert observed[2] == F(1,2)*F(1,3 if uniform else 2)**n
        assert sum(observed) == 1
        assert all(block[p,d] == observed[p]/2 for p in range(3) for d in ('S','R'))
        nxt = defaultdict(F)
        for q,mass in law.items():
            row = (F(1,2),F(1,4),F(1,4)) if q == 'S' and not uniform else (F(1,len(adj[q])),)*len(adj[q])
            for d,pr in zip(adj[q],row):
                nxt[d] += mass*pr
        law = nxt
assert sum(F(1,2)*F(2,3)**n for n in range(1,101)) == 1-F(2,3)**100
print('50 exact block laws, reset independence, and geometric-sum check passed.')
