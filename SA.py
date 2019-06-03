import random as r
from math import exp
from flowshop import file_reader, converter
import time
from neh import Neh


def total(*args):
    border = [[] for i in range(len(args))]
    border[0] = [sum(args[0][:i]) for i in range(1, len(args[0]) + 1)]
    for n in range(len(args[0])):
        for i in range(1, len(args)):
            if n == 0:
                border[i].append(border[i - 1][n] + args[i][n])
            else:
                if border[i - 1][n] > border[i][n - 1]:
                    border[i].append(border[i - 1][n] + args[i][n])
                else:
                    border[i].append(border[i][n - 1] + args[i][n])
    return border[len(args) - 1][len(args[0]) - 1]


def g_neighbor(solve, insert=False):
    n_solve = solve[::]
    if insert:
        element = n_solve.pop(r.randint(0, len(solve)-1))
        n_solve.insert(r.randint(0, len(solve)-1), element)
    else:
        index = r.sample(list(range(len(solve))), 2)
        n_solve[index[0]], n_solve[index[1]] = n_solve[index[1]], n_solve[index[0]]
    return n_solve


def transition_p(cmax, cmax_bis, t):
    if t == 0:
        return -1
    elif cmax_bis >= cmax:
        return exp((cmax-cmax_bis)/t)
    else:
        return 1


def change(*args):
    task = [args[i][0] for i in range(len(args))]
    task = [[task[z][y] for z in range(len(task))] for y in range(len(task[0]))]
    return task


def chilling(t, param=None, k=None, k_max=None):
    if param:
        return param * t
    return t*(k/k_max)


def sa(*args, neh=False, diffrent=False):
    if neh:
        n = Neh()
        pattern = n.neh(*args)
        elements = converter(pattern, *args)
        tasks = list(zip(*elements))
        task = [[tasks[i], pattern[i]-1] for i in range(len(pattern))]
    else:
        tasks = list(zip(*args))
        task = [[v, i] for i, v in enumerate(tasks)]
    solve = task[::]
    if not neh:
        r.shuffle(solve)
    t = 200
    iteration = 10000
    for i in range(iteration):
        cmax = total(*change(*solve))
        if diffrent:
            while True:
                solve_bis = g_neighbor(solve)
                cmax_bis = total(*change(*solve_bis))
                if cmax != cmax_bis:
                    break
        else:
            solve_bis = g_neighbor(solve)
            cmax_bis = total(*change(*solve_bis))
        p = transition_p(cmax, cmax_bis, t)
        if p >= r.uniform(0, 1):
            solve = solve_bis
        # t = chilling(t, k=i+1, k_max=iteration)
        t = chilling(t, param=0.99)
    solve = [solve[i][1] for i in range(len(solve))]
    return list(map(lambda x: x+1, solve))


if __name__ == '__main__':
    examples = file_reader()
    for w, e in enumerate(examples):
        if w == 30:
            start_t = time.time()
            o = sa(*e, neh=True, diffrent=True)
            end_t = time.time()
            czas = end_t - start_t
            print(f"{w}:")
            print(o)
            print("cmax przed", total(*e))
            print("Czas cmax", total(*converter(o, *e)))
            print(czas)

