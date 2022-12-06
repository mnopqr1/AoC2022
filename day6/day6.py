"""AoC 2022 Day 6
Usage: python3 day6.py file.txt n, where n is the length of the marker.
"""
import sys
from collections import Counter

with open(sys.argv[1], 'r') as f:
    s = f.readline()

n = int(sys.argv[2])

buf = Counter(s[:n])
k = n
while any(m > 1 for m in buf.values()):
    buf[s[k-n]] -= 1
    if s[k] not in buf: 
        buf[s[k]] = 1
    else: 
        buf[s[k]] += 1
    k = k + 1
print(k)