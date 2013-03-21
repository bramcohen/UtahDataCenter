from traceback import extract_stack, format_list
from time import time as defaulttime
from datetime import datetime
from collections import Sequence

class spam:
    def eggs(self):
        pass

method = type(spam().eggs)
function = type(lambda: 3)
builtinfunction = type(defaulttime)
nonet = type(None)

def utah(other, timefunc = defaulttime, log = None, prefix = '', self = None):
    if hasattr(other, 'nolog'):
        return other
    if hasattr(other, '_target'):
        return other
    t = type(other)
    if t in (int, bytes, str, tuple, nonet, bool, float):
        return other
    if log is None:
        log = []
    if t is dict:
        return DictLogger(timefunc, other, log, prefix)
    if t is list:
        return ListLogger(timefunc, other, log, prefix)
    if t is set:
        return SetLogger(timefunc, other, log, prefix)
    if t is method:
        if other.__self__ is not self:
            if hasattr(other.__self__, 'nolog'):
                return other
            self = utah(other.__self__, timefunc, log, prefix, self)
        return lambda *a, **b: other.__func__(*([self] + list(a)), **b)
    if t is function or t is builtinfunction:
        return other
    return ObjLogger(timefunc, other, log, prefix)

def utahed(t, timefunc = defaulttime):
    return lambda *a, **b: utah(t(*a, **b), timefunc)

def _dump(log, prefix = '', filters = []):
    for assign, t, stack in log:
        if any(x in assign for x in filters):
            continue
        if assign[:4] != 'del ':
            if assign[:len(prefix)] != prefix:
                continue
            print(assign[len(prefix):])
        else:
            if assign[4:len(prefix)+4] != prefix:
                continue
            print('del ' + assign[4+len(prefix):])
        print('time ' + format_time(t))
        print(''.join(format_list([x for x in stack if 'UtahDataCenter' not in x[0]])))

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def format_time(t):
    d = datetime.fromtimestamp(t)
    return '%i %s %2i %2i:%2i:%2i.%6i' % (d.year, months[d.month-1], d.day, d.hour, d.minute, d.second, d.microsecond)

class ObjLogger:
    def __init__(self, timefunc, other, log, prefix):
        object.__setattr__(self, '_time', timefunc)
        object.__setattr__(self, '_target', other)
        object.__setattr__(self, '_log', log)
        object.__setattr__(self, '_prefix', prefix)

    def __hash__(self):
        return hash(self._target)

    def __bool__(self):
        return (True if self._target else False)

    def __delattr__(self, key):
        if hasattr(key, '_target'):
            key = key._target
        self._log.append(('del ' + self._prefix + '.' + str(key), self._time(), extract_stack()))
        self._target.__delattr__(key)

    def __setattr__(self, key, value):
        if hasattr(key, '_target'):
            key = key._target
        if hasattr(value, '_target'):
            value = value._target
        self._log.append(((self._prefix + '.' + str(key) + ' = ' + repr(value)), self._time(), extract_stack()))
        self._target.__setattr__(key, value)

    def __iter__(self):
        return (utah(b, self._time, self._log, self._prefix + '<iter ' + str(a) + '>') for (a, b) in enumerate(self._target))

    def __len__(self):
        return len(self._target)

    def __getattr__(self, key):
        if hasattr(key, '_target'):
            key = key._target
        r = getattr(self._target, key)
        return utah(r, self._time, self._log, (self._prefix if callable(r) else (self._prefix + '.' + str(key))), self)

    def __repr__(self):
        return repr(self._target)

    def __str__(self):
        return str(self._target)

    def __eq__(self, thing):
        if hasattr(thing, '_target'):
            thing = thing._target
        return self._target == thing

    def dump(self, sub = '', filters = []):
        _dump(self._log, self._prefix + sub, filters)

    def dclear(self):
        del self._log[:]

class ListLogger(Sequence):
    def __init__(self, timefunc, target, log, prefix):
        self._time = timefunc
        self._target = target
        self._log  = log
        self._prefix = prefix

    def __iter__(self):
        return (utah(b, self._time, self._log, self._prefix + '[' + str(a) + ']') for (a, b) in enumerate(self._target))

    def _add(self, s):
        if hasattr(s, '_target'):
            s = s._target
        self._log.append((s, self._time(), extract_stack()))

    def dump(self, sub = '', filters = []):
        _dump(self._log, self._prefix + sub, filters)

    def dclear(self):
        del self._log[:]

    def __bool__(self):
        return (True if self._target else False)

    def __eq__(self, thing):
        if hasattr(thing, '_target'):
            thing = thing._target
        return self._target == thing

    def append(self, thing):
        if hasattr(thing, '_target'):
            thing = thing._target
        self._add(self._prefix  + '.append(' + repr(thing) + ')')
        self._target.append(thing)
    
    def count(self, thing):
        if hasattr(thing, '_target'):
            thing = thing._target
        return self._target.count(thing)
    
    def extend(self, stuff):
        stuff2 = [(x if not hasattr(x, '_target') else x._target) for x in stuff]
        self._add(self._prefix + '.extend(' + repr(stuff) + ')')
        self._target.extend(stuff2)
    
    def index(self, thing):
        if hasattr(thing, '_target'):
            thing = thing._target
        return self._target.index(thing)
    
    def insert(self, index, thing):
        if hasattr(index, '_target'):
            index = index._target
        if hasattr(thing, '_target'):
            thing = thing._target
        self._add(self._prefix + '.insert(' + str(index) + ', ' + repr(thing) + ')')
        self._target.insert(index, thing)
    
    def pop(self, index):
        if hasattr(index, '_target'):
            index = index._target
        self._add(self._prefix + '.pop(' + str(index) + ')')
        return self._target.pop(index)
    
    def remove(self, thing):
        if hasattr(thing, '_target'):
            thing = thing._target
        self._add(self._prefix + '.remove(' + str(thing) + ')')
        if hasattr(thing, '_target'):
            thing = thing._target
        self._target.remove(thing)
    
    def reverse(self):
        self._add(self._prefix + '.reverse()')
        self._target.reverse()
    
    def sort(self):
        self._add(self._prefix + '.sort()')
        self._target.sort()

    def __len__(self):
        return len(self._target)
    
    def __repr__(self):
        return repr(self._target)
    
    def __str__(self):
        return str(self._target)
    
    def __contains__(self, thing):
        return thing in self._target
    
    def __getitem__(self, index):
        if hasattr(index, '_target'):
            index = index._target
        return utah(self._target[index], self._time, self._log, self._prefix + '[' + str(index) + ']')
    
    def __setitem__(self, index, thing):
        if hasattr(index, '_target'):
            index = index._target
        if hasattr(thing, '_target'):
            thing = thing._target
        self._add(self._prefix + '[' + str(index) + '] = ' + repr(thing))
        self._target[index] = thing

    def __delitem__(self, key):
        if hasattr(key, '_target'):
            key = key._target
        self._add('del ' + self._prefix + '[' + str(key) + ']')
        del self._target[key]
    
class DictLogger:
    def __init__(self, timefunc, target, log, prefix):
        self._time = timefunc
        self._target = target
        self._log  = log
        self._prefix = prefix

    def _add(self, s):
        self._log.append((s, self._time(), extract_stack()))

    def dump(self, sub = '', filters = []):
        _dump(self._log, self._prefix + sub, filters)

    def dclear(self):
        del self._log[:]

    def clear(self):
        self._add(self._prefix + '.clear()')
        self._target.clear()
    
    def get(self, a, b = None):
        if hasattr(a, '_target'):
            a = a._target
        if b is None:
            return utah(self._target.get(a, b), self._time, self._log, self._prefix + '.get(' + repr(a) + ')')
        else:
            return utah(self._target.get(a, b), self._time, self._log, self._prefix + '.get(' + repr(a) + ',' + repr(b) + ')')
    
    def items(self):
        return [(a, utah(b, self._time, self._log, self._prefix + '[' + repr(a) + ']')) for (a, b) in self._target.items()]
    
    def keys(self):
        return self._target.keys()
    
    def pop(self, key):
        if hasattr(key, '_target'):
            key = key._target
        self._add(self._prefix + '.pop(' + repr(key) + ')')
        return self._target.pop(key)
    
    def values(self):
        return [utah(b, self._time, self._log, self._prefix + '[' + repr(a) + ']') for (a, b) in self._target.items()]

    def __iter__(self):
        return (a for a in self._target)
    
    def __bool__(self):
        return (True if self._target else False)

    def __eq__(self, thing):
        if hasattr(thing, '_target'):
            thing = thing._target
        return self._target == thing

    def __len__(self):
        return len(self._target)
    
    def __repr__(self):
        return repr(self._target)
    
    def __str__(self):
        return str(self._target)
    
    def __contains__(self, thing):
        return thing in self._target
    
    def __delitem__(self, key):
        if hasattr(key, '_target'):
            key = key._target
        self._add('del ' + self._prefix + '[' + repr(key) + ']')
        del self._target[key]
    
    def __getitem__(self, index):
        if hasattr(index, '_target'):
            index = index._target
        return utah(self._target[index], self._time, self._log, self._prefix + '[' + repr(index) + ']')

    def __setitem__(self, index, thing):
        if hasattr(index, '_target'):
            index = index._target
        if hasattr(thing, '_target'):
            thing = thing._target
        self._add(self._prefix + '[' + repr(index) + '] = ' + repr(thing))
        self._target[index] = thing

class SetLogger:
    def __init__(self, timefunc, target, log, prefix):
        self._time = timefunc
        self._target = target
        self._log  = log
        self._prefix = prefix

    def _add(self, s):
        self._log.append((s, self._time(), extract_stack()))

    def dump(self, sub = '', filters = []):
        _dump(self._log, self._prefix + sub, filters)

    def dclear(self):
        del self._log[:]

    def add(self, other):
        if hasattr(other, '_target'):
            other = other._target
        self._add(self._prefix + '.add(' + repr(other) + ')')
        self._target.add(other)

    def remove(self, other):
        if hasattr(other, '_target'):
            other = other._target
        self._add(self._prefix + '.remove(' + repr(other) + ')')
        self._target.remove(other)

    def clear(self):
        self._add(self._prefix + '.clear()')
        self._target.clear()
    
    def pop(self):
        self._add(self._prefix + '.pop()')
        return self._target.pop()
    
    def __iter__(self):
        return (utah(b, self._time, self._log, self._prefix + '<iter ' + str(a) + '>') for (a, b) in enumerate(self._target))
    
    def __bool__(self):
        return (True if self._target else False)

    def __eq__(self, thing):
        if hasattr(thing, '_target'):
            thing = thing._target
        return self._target == thing._target

    def __len__(self):
        return len(self._target)
    
    def __repr__(self):
        return repr(self._target)
    
    def __str__(self):
        return str(self._target)
    
    def __contains__(self, thing):
        return thing in self._target

