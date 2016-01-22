from math import * 

SPC = "   "

class ID3:
    def entropy(self, s):
        p, tot = [self.org_dataset[i][self.hpos] for i in s], len(s)
        return 0 if p.count(p[0]) == tot else -sum(p.count(i) * log2(p.count(i) / tot) for i in {*p}) / tot

    def choose_best(self, s, av_attr):
        metric = []
        tot = len(s)
        for i in av_attr:
            splt = self.split_attr(s, i)
            info = sum(len(v) * self.entropy(v) for v in splt.values()) / tot
            metric.append([info, i])
        return min(metric)[1]

    def id3(self, s, av_attr):
        c = [self.org_dataset[i][self.hpos] for i in s]
        if self.entropy(s) == 0:
            return self.Node(c[0], self.dattr)
        if not av_attr: 
            return self.Node(max({*c}, key = c.count), self.dattr)
        bst = self.evalfunc(s, av_attr)
        splt = self.split_attr(s, bst)
        res = self.Node("", bst)
        #rem: add decisions for remaining classes of 'bst' to cover all scenarios
        res.sib = {k : self.id3(v, av_attr - {bst}) for k, v in splt.items()}
        return res

    def __init__(self, train_data, dattr):
        self.org_dataset = train_data
        self.hpos = train_data[0].index(dattr)
        self.decision_tree = None
        self.dattr = dattr
        self.evalfunc = self.choose_best

    def build(self):
        self.decision_tree = self.id3([i + 1 for i in range(len(self.org_dataset) - 1)], set(self.org_dataset[0]) - {self.dattr})

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
        p = self.org_dataset[0].index(attr)
        splt = {}
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
