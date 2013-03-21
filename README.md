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