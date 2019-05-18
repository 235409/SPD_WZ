from shrage import *
from copy import deepcopy


def cmax(data, order):
    time = sum(data[order[0]][:-1])
    qk = [sum(data[order[0]][:-1]) + data[order[0]][2]]
    for i in order[1:]:
        if data[i][0] > time:
            time = sum(data[i][:-1])
            qk.append(time + data[i][2])
        else:
            time += data[i][1]
            qk.append(time + data[i][2])
    return max(qk)


def critical(data, order, b):
    tasks = OrderedDict((x, data[x]) for x in order)
    crt = [order[0]]
    end = sum(tasks[order[0]][:-1])
    for i in order[1:order.index(b)+1]:
        if tasks[i][0] > end:
            crt.clear()
            crt.append(i)
            end = sum(tasks[i][:-1])
        else:
            crt.append(i)
            end += tasks[i][1]
    return crt


def get_c(data, path):
    tasks = OrderedDict((x, data[x]) for x in path)
    qb = tasks[path[-1]][2]
    for c in path[-2::-1]:
        if tasks[c][2] < qb:
            return c
    return None


def parameters(data, path):
    tasks = OrderedDict((x, data[x]) for x in path)
    rk = min(tasks[x][0] for x in path)
    qk = min(tasks[x][2] for x in path)
    pk = sum(tasks[x][1] for x in path)

    return rk, qk, pk


def carlier(data):
    tasks = deepcopy(data)
    order, u, b = schrage(tasks)
    try:
        if u < ub:
            ub = u
            end = order
    except UnboundLocalError:
        ub = u
        end = order
    path = critical(tasks, order, b)

    a = path[0]
    c = get_c(tasks, path)
    if c is None:
        return end
    idxc = path.index(c)
    k = path[idxc+1:]

    rk, qk, pk = parameters(tasks, k)

    rpc = tasks[c][0]
    tasks[c][0] = max(rpc, rk + pk)

    lb = schrage_ptm(tasks)
    lb = max(sum([rk, qk, pk]), sum(parameters(tasks, path[idxc:])), lb)
    if lb < ub:
        return carlier(tasks)
    tasks[c][0] = rpc

    qpc = tasks[c][2]
    tasks[c][2] = max(qpc, qk + pk)

    lb = schrage_ptm(tasks)
    lb = max(sum([rk, qk, pk]), sum(parameters(tasks, path[idxc:])), lb)
    if lb < ub:
        return carlier(tasks)
    tasks[c][2] = qpc
    return end


examples = file_reader("schr.data_n.txt")
for i, example in enumerate(examples):
    if i == i:
        lol = carlier(example)
        print(lol)
        print(cmax(example, lol))
