import time
from flowshop import total_makespan, file_reader


def position(placed, element):
    order = placed[::]
    idx = 0
    if not isinstance(element[0], list):
        tmp = total_makespan(element, *order)
    else:
        tmp = total_makespan(*[element, *order])
    for i in range(1, len(order)+1):
        order.insert(i, element)
        cmax = total_makespan(*order)
        if cmax < tmp:
            idx = i
            tmp = cmax
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


if __name__ == '__main__':
    examples = file_reader()
    start = time.time()
    for w, e in enumerate(examples):
        o = neh(*e)
        print(f"{w}:")
        print(o)
    end = time.time()
    print(end - start)

