import re

poop_obs = set()
with open('poop_cycles.txt') as f:
    for line in f:
        for match in re.findall(r'CYCLE: \((\d+), (\d+)\)', line):
            poop_obs.add((int(match[0]), int(match[1])))

quick_obs = set()
with open('quick_cycles4.txt') as f:
    for line in f:
        for match in re.findall(r'CYCLE: \((\d+), (\d+)\)', line):
            quick_obs.add((int(match[0]), int(match[1])))

print(quick_obs - poop_obs)
#print(poop_obs - quick_obs)
print(len(poop_obs), len(quick_obs))
