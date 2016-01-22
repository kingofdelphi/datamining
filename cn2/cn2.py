#implemnts cn2 disregarding time / space complexity

from math import * 

MAX = 20

class CN2:
    def __init__(self, data, dattr):
        self.data = data
        self.dattr = dattr

    #returns all (attribute, value) pair
    #A selector is of the form (attribute, value), [check for equality]
    def getSelectors(self, data):
         d = {i[0] : set(i[1:]) for i in zip(*data) if i[0] != self.dattr}
         return [[k, i] for k, v in d.items() for i in v]

    #return cojunction of a complex and a selector
    def conjunct(self, comp, sel):
        if not comp: 
            return [sel]
        if sel[0] in (i[0] for i in comp):
            return None #invalid conjunction
        return comp + [sel]

    def entropy(self, s):
        hpos = s[0].index(self.dattr)
        tot = len(s) - 1
        p = [s[i + 1][hpos] for i in range(tot)]
        return 0 if p.count(p[0]) == tot else -sum(p.count(i) * log2(p.count(i) / tot) for i in {*p}) / tot

    def maximal(self, star):
        res = []
        for i in range(len(star)):
            for j in range(i + 1, len(star)):
                if sum(k in star[j] for k in star[i]) == len(star[i]):
                    break
            else:
                res.append(star[i])
        return res

    def setcovered(self, data, comp):
        h = data[0]
        res = [h]
        for i in data[1:]:
            d = dict(zip(h, i))
            if sum(j[0] in d and d[j[0]] == j[1] for j in comp) == len(comp):
                res.append(i)
        return res

    def bestComplex(self, data):
        star = [[]] #contains empty complex
        bc, bce = None, 1.1
        selectors = self.getSelectors(data)
        while star:
            #multiply two sets
            newstar = [self.conjunct(i, j) for i in star for j in selectors]
            newstar = self.maximal([i for i in newstar if i != None])
            np = []
            for i in newstar:
                s = self.setcovered(data, i)
                if len(s) > 1: #not just header
                    np.append([self.entropy(s), i])
            np = sorted(np)
            if np and (np[0][0] < bce):
                bc, bce = np[0][1], np[0][0]
            np = np[:min(len(np), MAX)] # trim
            star = [i[1] for i in np]
        return bc

    #returns ordered set of rules
    def build(self):
        self.rules = []
        hp = self.data[0].index(self.dattr)
        data = self.data
        while data:
            bc = self.bestComplex(data)
            cv = self.setcovered(data, bc)
            if bc != None:
                data = [data[0]] + [i for i in data if i not in cv]
                r = [cv[i][hp] for i in range(1, len(cv))]
                self.rules.append([bc, max(set(r), key = r.count)])
            else: break
        r = [self.data[i][hp] for i in range(1, len(self.data))]
        self.rules.append([["default_rule"], max(set(r), key = r.count)])

    def descPrint(self):
        v = ""
        for c, d in self.rules[:len(self.rules) - 1]: #complex, decision
            s = " and ".join(str(i[0]) + " = " + str(i[1]) for i in c) 
            print(v + "if", s, "then", self.dattr, "=", d)
            v = "el"
        print("else", self.dattr, "=", self.rules[-1][1])

def main():
    f = open('data', 'r')
    dattr = f.readline().split()[0]
    data = [i.split() for i in f if i.split() != []]
    d = CN2(data, dattr)
    d.build()
    d.descPrint()

if __name__ == "__main__":
    main()
