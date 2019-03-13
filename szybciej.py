import re
import time
import numpy as nu
import random

def total_makespan(*args):
    """Liczy czas cmax danych kolejnych zadan maszyn"""
    border = []                                             # czasy skoczenia zadan z poprzedniej maszyny
    y = 0
    for n in range(len(args)-1):
        tmp = sum(args[y][0] for y in range(n+2))           # suma czasow zadan pierwszych maszyn
        for i in range(1, len(args[n+1])):
            if n == 0:                                      # maszyna druga
                if tmp >= sum(args[n][:i+1]):               # gdy zad poprzednie sie skonczylo
                    tmp += args[n+1][i]
                else:                                       # gdy zad poprzednie nie skoczylo sie
                    tmp = sum(args[n][:i+1]) + args[n+1][i]
            else:                                           # kazda maszyna nastepna
                if tmp >= border[y]:                        # zad poprzednie zakonczone
                    tmp += args[n + 1][i]
                else:
                    tmp = border[y] + args[n + 1][i]        # -"- niezkonczone
                y += 1                                      # nastepny czas
            border.append(tmp)
    return tmp


def posytion(o, what):
    order = o[::]
    idx = 0
    if not isinstance(what[0], list):
        tmp = total_makespan(what, *order)
    else:
        tmp = total_makespan(*[what, *order])
    for i in range(1, len(order)+1):
        order.insert(i, what)
        start = time.time()
        cmax = total_makespan(*order)
        print(time.time()-start)
        if cmax < tmp:
            # print("CMAX_z:", cmax, order)
            # print('LOL')
            idx = i
            tmp = cmax
        del order[i]
    return idx


def insert(order, position, value):
    seq = order[:]
    seq.insert(position, value)
    return seq

def neh(*args):
    total = [[sum([args[i][y] for i in range(len(args))]), y] for y in range(len(args[0]))]
    s_total = sorted(total, key=lambda x: x[0], reverse=True)
    s_task = [s_total[i][1] for i in range(len(s_total))]
    order = [s_task[0]]
    for i in range(1, len(s_task)):
        oarr = [[args[i][y] for i in range(len(args))] for y in order]
        what = [args[z][s_task[i]] for z in range(len(args))]
        pos = posytion(oarr, what)
        order = insert(order, pos, s_task[i])
    return list(map(lambda x: x+1, order))


def file_reader():
    """generator zwracjacy zawartosc danych z pliku data"""
    with open("neh.data.txt", encoding='utf8') as file:
        lines = file.readlines()
        start = re.compile(r'data\.\d{3}:')
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
                if data[0][0]+1 == len(data):
                    yield [[data[i][y] for i in range(1, len(data))] for y in range(data[0][1])]
        return StopIteration

def converter(pattern, *args):
    """ustawia wartosci tblic w odpowiedniej kolejnosci"""
    tab = []
    for arg in args:
        tab.append([arg[i-1] for i in pattern])
    return tab

# m_1 = [4, 4, 1, 5]
# m_2 = [1, 3, 2, 1]
# m_3 = [4, 3, 3, 3]
#
# print(neh(m_1, m_2, m_3))

# zad_1 = [4, 1, 4]
# zad_2 = [[4, 3, 3]]
# zad_4 = [5, 1, 3]
#
# print(posytion(zad_2, zad_1))

examples = file_reader()
start = time.time()
for w, e in enumerate(examples):
    if w > 69:
        o = neh(*e)
        print(f"{w}:")
        print(o)
end = time.time()
print(end - start)


