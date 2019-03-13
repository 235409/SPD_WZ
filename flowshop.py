from itertools import permutations
import re
from random import randint


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


def permute_machine(*args):
    """permutacje maszyn"""
    data = list((zip(*args)))
    for p in permutations(data):
        yield [[p[z][y] for z in range(len(p))] for y in range(len(p[0]))]


def c_max(*args):
    """czas dla kazdej z permutacji danych maszyn"""
    for p in permute_machine(*args):
        yield total_makespan(*p)


def show_total_makespan(*args):
    """pokazuje kazda mozliwosc z jego czasem"""
    permutes = permute_machine(*args)
    print(f"Przeglad zupelny dla maszyn {args}:")
    for permute in permutes:
        machines = ''
        for n, i in enumerate(permute):
            if n == (len(permute)-1):
                machines += 'oraz ' + str(i)
            else:
                machines += str(i) + ', '
        print(f"\t {machines}: {total_makespan(*permute)}")


def johnsons_rule(arr1, arr2, arr3=None):
    """zasada jhnsona"""
    if arr3:        # dla 3 maszyn
        s_1 = [arr1[i]+arr2[i] for i in range(len(arr1))]
        s_2 = [arr2[i]+arr3[i] for i in range(len(arr1))]
    else:           # dla 2 maszyn
        s_1 = arr1
        s_2 = arr2
    d_1 = {i+1: s_1[i] for i in range(len(arr1))}   # dict zadanie: wartosc
    d_2 = {i+1: s_2[i] for i in range(len(arr2))}
    order = [i for i in range(len(arr1))]           # tablica z kolejnoscia
    i = 0       # indeks dla mszyny pierwszej
    y = -1      # -"- drugiej
    while d_1 and d_2:
        m_1 = min(d_1.values())
        m_2 = min(d_2.values())
        if m_1 <= m_2:          # pierwsza maszyna
            for k, v in d_1.items():
                if m_1 == v:    # szukanie indeksu
                    idx = k
            order[i] = idx
            i += 1
        else:                   # druga maszyna
            for k, v in d_2.items():
                if m_2 == v:
                    idx = k
            order[y] = idx
            y -= 1
        del d_2[idx]
        del d_1[idx]
    return order


def converter(pattern, *args):
    """ustawia wartosci tblic w odpowiedniej kolejnosci"""
    tab = []
    for arg in args:
        tab.append([arg[i-1] for i in pattern])
    return tab


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


if __name__ == '__main__':
    examples = file_reader()
    example = next(examples)
    o = johnsons_rule(*example)
    print(f"Kolejnosc {o}")
    arrays = converter(o, *example)
    print(f"Czas: {total_makespan(*arrays)}")

    arr1 = [randint(1, 10) for i in range(5)]
    arr2 = [randint(1, 10) for i in range(5)]
    arr3 = [randint(1, 10) for i in range(5)]

    o_2 = johnsons_rule(arr1, arr2, arr3)
    print(total_makespan(*converter(o_2, arr1, arr2, arr3)))
    cmax = list(c_max(arr1, arr2, arr3))
    print(min(cmax))
    show_total_makespan(arr1, arr2, arr3)


