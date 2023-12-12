import re

from bisect import bisect, bisect_left, bisect_right
from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from math import ceil, comb, factorial, gcd, isclose, lcm

from algo import a_star, custsort, merge_ranges, sssp
from constants import EPSILON
from helpers import adjacent, between, chunks, chunks_with_overlap, columns, digits, dimensions, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, overlap, positives, rays, rays_from_inside, words


def parse(lines):
    return [line.split() for line in lines]
    
@cache
def solve_row(springs, config):
    n = len(springs)
    goal = ints(config)
    m = sum(goal)

    def interpret(s):
        parts = [p for p in s.split('.') if p]
        partlens = [len(p) for p in parts]

        return partlens 
    
    def possible(partial):        
        tot = partial.count('#')

        if tot > m:
            return False
        
        if '?' not in partial:
            return True        
        
        start = interpret(partial.split('?')[0])

        goallen = len(goal)
        startlen = len(start)

        if startlen > goallen:
            return False        
        
        for i in range(startlen-1):
            if goal[i] != start[i]:
                # print('oops', partial, start, goal)
                return False

        return True
        

    @cache
    def solve(pos, s):
        if pos == n:
            return interpret(s) == goal
        
        if s[pos] == '?':
            l1 = list(s)
            l2 = list(s)

            l1[pos] = '.'
            l2[pos] = '#'

            a = ''.join(l1)
            b = ''.join(l2)

            ways = 0

            if possible(a):
                ways += solve(pos+1, a)
            if possible(b):
                ways += solve(pos+1, b)
                
            return ways
        
        return solve(pos+1, str(s))
    
    return solve(0, str(springs))


def solve_a(lines):
    return -1  
    data = parse(lines)
    total = 0

    for springs, config in data:
        total += solve_row(springs, config)
        print(springs, config, total)

    return total


def solvesimple(springs, num):
    if num > len(springs):
        return 0
    
    first = -1
    last = -1

    for i, c in enumerate(springs):
        if c == '#':
            if first == -1:
                first = i
            last = i

    if first == -1:
        return len(springs) - num + 1
    
    return last-first == num-1


def nurowsolve(springs, config):    
    con = ints(config)
    periods = len(con) - 1

    if periods == 0:
        return solvesimple(springs, con[0])

    questindices = [i for i in range(len(springs)) if springs[i] == '?']
    total = 0

    for c in combinations(questindices, periods):
        breaks = list(c)
        parts = [springs[:breaks[0]]]

        for i in range(1, periods):
            parts.append(springs[breaks[i-1]:breaks[i]])

        parts.append(springs[breaks[-1]:])

        ways = 1

        for i in range(periods):
            ways *= solvesimple(parts[i], con[i])

        total += ways

    return total

nurowsolve('###????', '3,1')
def nusolve(s, c):
    goal = ints(c)
    parts = [p for p in re.split(r'\.+', s) if p]
    seen = {}

    def solve(partpos, goalpos):
        if partpos == len(parts):
            return goalpos == len(goal)
        
        part = parts[partpos]

        minimal = part.count('#')
        extras = part.count('?')

        if goalpos == len(goal):
            if minimal > 0:
                return 0
            
            return solve(partpos+1, goalpos)        
        
        if (partpos, goalpos) in seen:
            return seen[(partpos, goalpos)]
        
        poss = 0
        cumsum = 0

        for x in range(len(goal) - goalpos):
            cumsum += goal[goalpos + x]

            if cumsum > minimal + extras:
                break

            ways = nurowsolve(part, ','.join(str(g) for g in goal[goalpos:goalpos+x+1]))

            poss += ways * solve(partpos+1, goalpos+x+1)

        if minimal == 0:
            poss += solve(partpos+1, goalpos)
        
        seen[(partpos, goalpos)] = poss

        return poss

    return solve(0, 0)


def solve_b(lines):
    # return -1
    data = parse(lines)
    total = 0

    for i, d in enumerate(data):        
        springs, config = d

        s = []
        c = []

        for _ in range(5):
            s.append(springs + '?')
            c.append(config + ',')        

        s1 = ''.join(s)[:-1]
        c1 = ''.join(c)[:-1]
        
        score = nusolve(s1, c1)        

        total += score

        print(i, len(data), score, total)

    return total


def main():
    lines = []

    with open('12.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())
