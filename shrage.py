from collections import OrderedDict
from copy import deepcopy
import re
import time


def schrage(data):
    tasks = OrderedDict(sorted(data.items(), key=lambda x: x[0]))
    ready = OrderedDict()
    order = []
    cooled = []
    t = min(tasks.values(), key=lambda x: x[0])[0]

    while ready or tasks:
        avaible = OrderedDict(i for i in tasks.items() if i[1][0] <= t)
        ready.update(avaible)
        for i in avaible.keys():
            del tasks[i]
        if not ready:
            t = min(tasks.values(), key=lambda x: x[0])[0]
        else:
            long = max(ready.items(), key=lambda x: x[1][2])
            del ready[long[0]]
            order.append(long[0])
            t += long[1][1]
        cooled.append(t + long[1][2])

    return order, max(cooled)


def schrage_ptm(data):
    tasks = OrderedDict(sorted(data.items(), key=lambda x: x[0]))
    tasks_copy = deepcopy(tasks)
    ready = OrderedDict()
    t = 0
    cmax = 0
    l = None

    while ready or tasks:
        while tasks and min(tasks.values(), key=lambda x: x[0])[0] <= t:
            tmp = min(tasks.items(), key=lambda x: x[1][0])
            ready.update({tmp[0]: tmp[1]})
            del tasks[tmp[0]]
            if l is not None:
                if tmp[1][2] > tasks_copy[l][2]:
                    tasks_copy[l][1] = t - tmp[1][0]
                    t = tmp[1][0]
                    if tasks_copy[l][1] > 0:
                        ready.update({l: tasks_copy[l]})
        if not ready:
            t = min(tasks.values(), key=lambda x: x[0])[0]
        else:
            tmp = max(ready.items(), key=lambda x: x[1][2])
            del ready[tmp[0]]
            l = tmp[0]
            t += tmp[1][1]
            cmax = max(cmax, t + tmp[1][2])

    return cmax


def file_reader():
    """generator zwracjacy zawartosc danych z pliku data"""
    with open("schr.data_n.txt", encoding='utf8') as file:
        lines = file.readlines()
        start = re.compile(r'data\.\d:')
        end = re.compile(r'\n')
        flag = False
        for line in lines:
            if re.match(start, line):
                data = []
                flag = True
                continue
            if re.fullmatch(end, line):
                flag = False
            if flag:
                tmp = list(map(int, line.split()))
                data.append(tmp)
                if data[0][0] + 1 == len(data):
                    yield {key: value for key, value in enumerate(data[1:])}
        return StopIteration


examples = file_reader()
for i, example in enumerate(examples):
    if i == i:
        strat = time.perf_counter()
        result, cmax = schrage(example)
        times = time.perf_counter()-strat
        # cmax = schrage_ptm(example)
        print(result)
        print(cmax)
