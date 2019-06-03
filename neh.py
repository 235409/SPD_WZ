import time
from flowshop import file_reader, converter
import re


class Neh:
    def __init__(self):
        self.helper = []

    @staticmethod
    def total(*args):
        border = [[] for i in range(len(args))]
        border[0] = [sum(args[0][:i]) for i in range(1, len(args[0])+1)]
        for n in range(len(args[0])):
            for i in range(1, len(args)):
                if n == 0:
                    border[i].append(border[i-1][n] + args[i][n])
                else:
                    if border[i-1][n] > border[i][n-1]:
                        border[i].append(border[i-1][n] + args[i][n])
                    else:
                        border[i].append(border[i][n-1] + args[i][n])
        return [border[len(args)-1][len(args[0])-1], border]

    def total_acceleration(self, start, *args):
        border = [self.helper[i][0:start] for i in range(len(self.helper))]
        for n in range(start, len(args[0])):
            for i in range(len(args)):
                if i == 0:
                    border[i].append(border[i][n - 1] + args[i][n])
                else:
                    if border[i - 1][n] > border[i][n - 1]:
                        border[i].append(border[i - 1][n] + args[i][n])
                    else:
                        border[i].append(border[i][n - 1] + args[i][n])
        return [border[len(args) - 1][len(args[0]) - 1], border]

    def position(self, placed, element, flag=False):
        order = placed[::]
        idx = 0
        first = [element, *order]
        order_fine = [[first[z][y] for z in range(len(first))] for y in range(len(first[0]))]
        t = self.total(*order_fine)
        tmp = t[0]
        tmp_arr = t[1]
        for i in range(1, len(order)+1):
            order.insert(i, element)
            order_fine = [[order[z][y] for z in range(len(order))] for y in range(len(order[0]))]
            if i >= 2 and flag:
                c_max = self.total_acceleration(i, *order_fine)
            else:
                c_max = self.total(*order_fine)
            if c_max[0] < tmp:
                idx = i
                tmp = c_max[0]
                tmp_arr = c_max[1]
            del order[i]
        self.helper = tmp_arr
        return idx

    def neh(self, *args):
        total = [[sum([args[i][y] for i in range(len(args))]), y] for y in range(len(args[0]))]
        s_total = sorted(total, key=lambda x: x[0], reverse=True)
        s_task = [s_total[i][1] for i in range(len(s_total))]
        order = [s_task[0]]
        for i in range(1, len(s_task)):
            tasks = [[args[i][y] for i in range(len(args))] for y in order]
            element = [args[z][s_task[i]] for z in range(len(args))]
            if i == 1:
                pos = self.position(tasks, element)
            else:
                pos = self.position(tasks, element, flag=True)
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
    neh = Neh()
    for w, e in enumerate(examples):
        if w == w:
            start_t = time.time()
            o = neh.neh(*e)
            end_t = time.time()
            czas = end_t - start_t
            print(f"{w}:")
            print(o)
            print(solves[w])
            if o == solves[w]:
                print("Wynik prawidłowy")
            print(czas)
            print(neh.total(*converter(o, *e)))
