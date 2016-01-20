from math import * 
spc = "   "
def entropy(s, attr):
    tot = len(s) - 1
    d = {}
    for i in zip(*s):
        if i[0] == attr:
            for j in i[1:]:
                d[j] = d.get(j, 0) + 1
            break
    return -sum((i / tot) * log2(i / tot) for i in d.values())

class Node:
    def __init__(self, lbl = "", d = None):
        self.sib = {}
        self.label = lbl
        self.div_attr = d
    def trace(self, indent = True, gap = ""):
        if self.sib == {}: print(gap, self.div_attr, '=', self.label)
        else:
            dl = ""
            for k, v in self.sib.items():
                print(gap + dl + "if", self.div_attr, "==", k, ":")
                dl = "el"
                v.trace(indent, gap + spc if indent else gap)

def split_attr(s, attr):
    st = list(zip(*s))
    splt = {}
    for i in st:
        if i[0] == attr:
            for drow, j in enumerate(i[1:]):
                if j in splt: splt[j].append(drow)
                else: splt[j] = [drow]
            break
    rem_data = list(zip(*(i for i in st if i[0] != attr))) #remove bst column from dataset
    return [splt, rem_data]

def choose_best1(s, dattr):
    metric = []
    for i in s[0]:
        if i == dattr: continue
        metric.append([entropy(s, i), i])
    return min(metric)[1]

def choose_best2(s, dattr):
    metric = []
    ent = entropy(s, dattr)
    tot = len(s) - 1
    for i in s[0]:
        if i == dattr: continue
        ig = 0
        splt, rem_data = split_attr(s, i)
        for k, v in splt.items():
            new_data = [rem_data[0]] + [rem_data[i + 1] for i in v]
            ig += len(v) / tot * entropy(new_data, dattr)
        metric.append([ent - ig, i])
    return max(metric)[1]

#dattr is the attribute to be decided
#s is the dataset
def id3(s, dattr, best_evaluator):
    st = list(zip(*s))
    if len(st) == 1 and st[0][0] == dattr: 
        return Node(st[0][1], dattr)
    for i in st:
        if i[0] == dattr:
            c = i[1:]
            if c.count(c[0]) == len(c): return Node(c[0], dattr)
            break
    bst = best_evaluator(s, dattr)
    splt, rem_data = split_attr(s, bst)
    res = Node("", bst)
    for k, v in splt.items():
        res.sib[k] = id3([rem_data[0]] + [rem_data[i + 1] for i in v], dattr, best_evaluator)
    return res

def main():
    f = open('data', 'r')
    dattr = f.readline().split()[0]
    data = [i.split() for i in f]
    tree = id3(data, dattr, choose_best2)
    tree.trace()
if __name__ == "__main__":
    main()
