import time
from flowshop import total_makespan, file_reader
import re


def position(placed, element):
    order = placed[::]
    idx = 0
    tmp = total_makespan(element, *order)
    for i in range(1, len(order)+1):
        order.insert(i, element)
        c_max = total_makespan(*order)
        if c_max < tmp:
            idx = i
            tmp = c_max
        del order[i]
    return idx


def neh(*args):
    total = [[sum([args[i][y] for i in range(len(args))]), y] for y in range(len(args[0]))]
    s_total = sorted(total, key=lambda x: x[0], reverse=True)
    s_task = [s_total[i][1] for i in range(len(s_total))]
    order = [s_task[0]]
    for i in range(1, len(s_task)):
        tasks = [[args[i][y] for i in range(len(args))] for y in order]
        element = [args[z][s_task[i]] for z in range(len(args))]
        pos = position(tasks, element)
        order.insert(pos, s_task[i])
    return list(map(lambda x: x+1, order))


def solve_reader():
    """generator zwracjacy zawartosc danych z pliku data"""
    with open("neh.data.txt", encoding='utf8') as file:
        lines = iter(file.readlines())
        start = re.compile(r'neh:')
        end = re.compile(r'\n')
        flag = False
        for line in lines:
            if re.match(start, line):
                data = []
                flag = True
                next(lines)
                continue
            if re.fullmatch(end, line):
                if flag:
                    yield data
                flag = False
            if flag:
                tmp = list(map(int, line.split()))
                data.extend(tmp)
        return StopIteration


if __name__ == '__main__':
    solves = list(solve_reader())
    examples = file_reader()
    for w, e in enumerate(examples):
        start_t = time.time()
        o = neh(*e)
        end_t = time.time()
        print(f"{w}:")
        print(o)
        print(solves[w])
        if o == solves[w]:
            print("Wynik prawidłowy")
        print(end_t - start_t)

