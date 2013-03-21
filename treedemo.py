from random import shuffle
from UtahDataCenter import utah

class tree:
    def __init__(self, key, value):
        self.lower = None
        self.higher = None
        self.key = key
        self.value = value

    def insert(self, key, value):
        if key < self.key:
            if self.lower is None:
                self.lower = tree(key, value)
            else:
                self.lower.insert(key, value)
        else:
            if self.higher is None:
                self.higher = tree(key, value)
            else:
                self.higher.insert(key, value)

    def read(self, key):
        if key == self.key:
            return self.value
        return (self.lower if key < self.key else self.higher).read(key)

    def __repr__(self):
        return 'tree[%s,%s,%s,%s]' % (repr(self.key), repr(self.value), repr(self.lower), repr(self.higher))

mytree = tree(5, 5*5)

mytree = utah(mytree)

x = list(range(10))
shuffle(x)
for i in x:
    mytree.insert(i, i*i)

mytree.dump()
