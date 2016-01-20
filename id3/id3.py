from math import * 

SPC = "   "

class ID3:
    def entropy(self, s, attr):
        tot, ind = len(s), self.org_dataset[0].index(attr)
        p = [self.org_dataset[i][ind] for i in s]
        return -sum(p.count(i) * log2(p.count(i) / tot) for i in set(p)) / tot

    def choose_best(self, s, av_attr, attr):
        metric = []
        ent = self.entropy(s, attr)
        tot = len(s)
        for i in av_attr:
            splt = self.split_attr(s, i)
            ig = sum(len(v) * self.entropy(v, attr) for k, v in splt.items()) / tot
            metric.append([ent - ig, i])
        return max(metric)[1]

    def id3(self, s, av_attr):
        p = self.org_dataset[0].index(self.dattr)
        if not av_attr: 
            return self.Node(self.org_dataset[s[0]][p], self.dattr)
        c = [self.org_dataset[i][p] for i in s]
        if c.count(c[0]) == len(c): 
            return self.Node(max(set(c), key = c.count), self.dattr)
        bst = self.evalfunc(s, av_attr, self.dattr)
        splt = self.split_attr(s, bst)
        res = self.Node("", bst)
        for k, v in splt.items(): 
            res.sib[k] = self.id3(v, av_attr - set(bst))
        return res

    def __init__(self, train_data, attr):
        self.org_dataset = train_data
        self.decision_tree = None
        self.dattr = attr
        self.evalfunc = self.choose_best

    def build(self):
        self.decision_tree = self.id3([i + 1 for i in range(len(self.org_dataset) - 1)], set(self.org_dataset[0]) - set([self.dattr]))

    def trace(self): 
        self.decision_tree.trace()

    class Node:
        def __init__(self, lbl = "", d = None):
            self.sib = {}
            self.label = lbl
            self.div_attr = d
        def trace(self, indent = True, gap = ""):
            if self.sib == {}: 
                print(gap, self.div_attr, '=', self.label)
            else:
                dl = ""
                for k, v in self.sib.items():
                    print(gap + dl + "if", self.div_attr, "==", k, ":")
                    dl = "el"
                    v.trace(indent, gap + SPC if indent else gap)

    def split_attr(self, s, attr):
        splt = {}
        p = self.org_dataset[0].index(attr)
        for i in s:
            k = self.org_dataset[i][p]
            if k in splt: splt[k].append(i)
            else: splt[k] = [i]
        return splt

def main():
    f = open('data', 'r')
    dattr = f.readline().split()[0]
    data = [i.split() for i in f if i.split() != []]
    a = ID3(data, dattr)
    a.build()
    a.trace()

if __name__ == "__main__":
    main()
