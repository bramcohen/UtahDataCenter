This is a utility for recording all accesses which happen to an object 
and then playing them back later. Even works through method invocations.

<pre>
>>> from UtahDataCenter import utah
>>> x = utah({})
>>> x[3] = []
>>> x[3].append({})
>>> x[3][0][4] = 'abc'
>>> x
{3: [{4: 'abc'}]}
>>> x.dump()
[3] = []
time 2013 Mar 20 20:56:58.635847
  File "<stdin>", line 1, in <module>

[3].append({})
time 2013 Mar 20 20:57: 4.570768
  File "<stdin>", line 1, in <module>

[3][0][4] = 'abc'
time 2013 Mar 20 20:57:34.640986
  File "<stdin>", line 1, in <module>
</pre>

treedemo.py demonstrates that it even works through method invocations

<pre>
~/UtahDataCenter master $ python3 treedemo.py 
.higher = tree[7,49,None,None]
time 2013 Mar 20 21:29:45.753952
  File "treedemo.py", line 38, in <module>
    mytree.insert(i, i*i)
  File "treedemo.py", line 19, in insert
    self.higher = tree(key, value)

.higher.lower = tree[6,36,None,None]
time 2013 Mar 20 21:29:45.754378
  File "treedemo.py", line 38, in <module>
    mytree.insert(i, i*i)
  File "treedemo.py", line 21, in insert
    self.higher.insert(key, value)
  File "treedemo.py", line 14, in insert
    self.lower = tree(key, value)

.lower = tree[4,16,None,None]
time 2013 Mar 20 21:29:45.754472
  File "treedemo.py", line 38, in <module>
    mytree.insert(i, i*i)
  File "treedemo.py", line 14, in insert
    self.lower = tree(key, value)

.higher.lower.lower = tree[5,25,None,None]
time 2013 Mar 20 21:29:45.754631
  File "treedemo.py", line 38, in <module>
    mytree.insert(i, i*i)
  File "treedemo.py", line 21, in insert
    self.higher.insert(key, value)
  File "treedemo.py", line 16, in insert
    self.lower.insert(key, value)
  File "treedemo.py", line 14, in insert
    self.lower = tree(key, value)

.higher.higher = tree[8,64,None,None]
time 2013 Mar 20 21:29:45.754785
  File "treedemo.py", line 38, in <module>
    mytree.insert(i, i*i)
  File "treedemo.py", line 21, in insert
    self.higher.insert(key, value)
  File "treedemo.py", line 19, in insert
    self.higher = tree(key, value)

.lower.lower = tree[0,0,None,None]
time 2013 Mar 20 21:29:45.754904
  File "treedemo.py", line 38, in <module>
    mytree.insert(i, i*i)
  File "treedemo.py", line 16, in insert
    self.lower.insert(key, value)
  File "treedemo.py", line 14, in insert
    self.lower = tree(key, value)

.lower.lower.higher = tree[1,1,None,None]
time 2013 Mar 20 21:29:45.755053
  File "treedemo.py", line 38, in <module>
    mytree.insert(i, i*i)
  File "treedemo.py", line 16, in insert
    self.lower.insert(key, value)
  File "treedemo.py", line 16, in insert
    self.lower.insert(key, value)
  File "treedemo.py", line 19, in insert
    self.higher = tree(key, value)

.lower.lower.higher.higher = tree[3,9,None,None]
time 2013 Mar 20 21:29:45.755248
  File "treedemo.py", line 38, in <module>
    mytree.insert(i, i*i)
  File "treedemo.py", line 16, in insert
    self.lower.insert(key, value)
  File "treedemo.py", line 16, in insert
    self.lower.insert(key, value)
  File "treedemo.py", line 21, in insert
    self.higher.insert(key, value)
  File "treedemo.py", line 19, in insert
    self.higher = tree(key, value)

.lower.lower.higher.higher.lower = tree[2,4,None,None]
time 2013 Mar 20 21:29:45.755489
  File "treedemo.py", line 38, in <module>
    mytree.insert(i, i*i)
  File "treedemo.py", line 16, in insert
    self.lower.insert(key, value)
  File "treedemo.py", line 16, in insert
    self.lower.insert(key, value)
  File "treedemo.py", line 21, in insert
    self.higher.insert(key, value)
  File "treedemo.py", line 21, in insert
    self.higher.insert(key, value)
  File "treedemo.py", line 14, in insert
    self.lower = tree(key, value)

.higher.higher.higher = tree[9,81,None,None]
time 2013 Mar 20 21:29:45.755685
  File "treedemo.py", line 38, in <module>
    mytree.insert(i, i*i)
  File "treedemo.py", line 21, in insert
    self.higher.insert(key, value)
  File "treedemo.py", line 21, in insert
    self.higher.insert(key, value)
  File "treedemo.py", line 19, in insert
    self.higher = tree(key, value)
</pre>