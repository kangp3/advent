from collections import defaultdict

a = '<    A  >  A   v  < <    A A  >   ^  A A  >  A   v   A A  ^  A    <  v   A A A  >   ^  A'
a = '^     A             < <         ^ ^     A       > >     A           v v v         A'
count = defaultdict(int)
last = 'A'
for i in a:
    if i == ' ':
        continue
    count[(last, i)] += 1
    last = i
print(dict(count))
