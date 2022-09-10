
from itertools import *
from collections import deque
from operator import mul, length_hint
from random import choice, sample, randrange
from math import modf
__name__ = "itertools_recipes"

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def prepend(value, iterator):
    "Prepend a single value in front of an iterator"
    # prepend(1, [2, 3, 4]) -> 1 2 3 4
    return chain([value], iterator)

def tabulate(function, start=0):
    "Return function(0), function(1), ..."
    return map(function, count(start))

def tail(n, iterable):
    "Return an iterator over the last n items"
    # tail(3, 'ABCDEFG') --> E F G
    return iter(deque(iterable, maxlen=n))

def consume(iterator, n=None):
    "Advance the iterator n-steps ahead. If n is None, consume entirely."
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)

def nth(iterable, n, default=None):
    "Returns the nth item or a default value"
    return next(islice(iterable, n, None), default)

def all_equal(iterable):
    "Returns True if all the elements are equal to each other"
    g = groupby(iterable)
    return next(g, True) and not next(g, False)

def quantify(iterable, pred=bool):
    "Count how many times the predicate is true"
    return sum(map(pred, iterable))

def padnone(iterable):
    """Returns the sequence elements and then returns None indefinitely.
    Useful for emulating the behavior of the built-in map() function.        ← ¿os ʍoɥ ¿ʇɐɥʍ
    """
    return chain(iterable, repeat(None))

def ncycles(iterable, n):
    "Returns the sequence elements n times"
    return flatten(repeat(tuple(iterable), n))

def dotproduct(vec1, vec2):
    return sum(map(mul, vec1, vec2))

#def flatten(listOfLists):
#    "Flatten one level of nesting"
#    return chain.from_iterable(listOfLists)
flatten = chain.from_iterable

def repeatfunc(func, times=None, *args):
    """Repeat calls to func with specified arguments.
    Example:  repeatfunc(random.random)
    """
    if times is None:
        return starmap(func, repeat(args))
    return starmap(func, repeat(args, times))

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    num_active = len(iterables)
    nexts = cycle(iter(it).__next__ for it in iterables)
    while num_active:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            # Remove the iterator we just exhausted from the cycle.
            num_active -= 1
            nexts = cycle(islice(nexts, num_active))

def partition(pred, iterable):
    'Use a predicate to partition entries into false entries and true entries'
    # partition(is_odd, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9
    t1, t2 = tee(iterable)
    return filterfalse(pred, t1), filter(pred, t2)

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = tuple(iterable)
    #return flatten(combinations(s, r) for r in range(len(s)+1))
    return flatten(map(combinations, repeat(s),  range(len(s)+1)))

def unique_everseen(iterable, key=None):
    "List unique elements, preserving order. Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element

def unique_justseen(iterable, key=None):
    "List unique elements, preserving order. Remember only the element just seen."
    # unique_justseen('AAAABBBCCDAABBB') --> A B C D A B
    # unique_justseen('ABBCcAD', str.lower) --> A B C A D
    return map(next, map(itemgetter(1), groupby(iterable, key)))

def iter_except(func, exception, first=None):
    """ Call a function repeatedly until an exception is raised.

    Converts a call-until-exception interface to an iterator interface.
    Like builtins.iter(func, sentinel) but uses an exception instead
    of a sentinel to end the loop.

    Examples:
        iter_except(functools.partial(heappop, h), IndexError)   # priority queue iterator
        iter_except(d.popitem, KeyError)                         # non-blocking dict iterator
        iter_except(d.popleft, IndexError)                       # non-blocking deque iterator
        iter_except(q.get_nowait, Queue.Empty)                   # loop over a producer Queue
        iter_except(s.pop, KeyError)                             # non-blocking set iterator

    """
    try:
        if first is not None:
            yield first()            # For database APIs needing an initial cast to db.first()
        while True:
            yield func()
    except exception:
        pass

def first_true(iterable, default=False, pred=None):
    """Returns the first true value in the iterable.

    If no true value is found, returns *default*

    If *pred* is not None, returns te first item
    for which pred(item) is true.

    """
    # first_true([a,b,c], x) --> a or b or c or x
    # first_true([a,b], x, f) --> a if f(a) else b if f(b) else x
    return next(filter(pred, iterable), default)

def random_product(*args, repeat=1):
    "Random selection from itertools.product(*args, **kwds)"
    #pools = [tuple(pool) for pool in args] * repeat
    #return tuple(choice(pool) for pool in pools)
    pools = (repeat(tuple(map(tuple, args)), repeat))
    return (map(choice, pools)) # .‿ .
    
def random_permutation(iterable, r=None):
    "Random selection from itertools.permutations(iterable, r)"
    pool = tuple(iterable)
    #r = len(pool) if r is None else r
    #return tuple(sample(pool, r)))
    return (sample(pool, r or len(pool)))

def random_combination(iterable, r):
    "Random selection from itertools.combinations(iterable, r)"
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(sample(range(n), r))
    return map(pool.__getitem__, indices)
    #return tuple(pool[i] for i in indices)

def random_combination_with_replacement(iterable, r):
    "Random selection from itertools.combinations_with_replacement(iterable, r)"
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(map(randrange, repeat(n, r)))
    return map(pool.__getitem__, indices)
    #indices = sorted(randrange(n) for i in range(r))
    #return tuple(pool[i] for i in indices)

def nth_combination(iterable, r, index):
    'Equivalent to list(combinations(iterable, r))[index]'
    pool = tuple(iterable)
    n = len(pool)
    if r < 0 or r > n:
        raise ValueError
    c = 1
    k = min(r, n-r)
    for i in range(1, k+1):
        c = c * (n - k + i) // i
    if index < 0:
        index += c
    if index < 0 or index >= c:
        raise IndexError
    result = []
    while r:
        c, n, r = c*r//n, n-1, r-1
        while index >= c:
            index -= c
            c, n = c*(n-r)//n, n-1
        result.append(pool[-1-n])
    return tuple(result)


######  ~  extension  ~  #######

def pairfold(itr):
    itls = tuple(itr)
    itnx = iter(itls).__next__
    return ((itnx(), itnx()) for i in range(0, len(itls), 2))

def nfold(itr, n=3, default=None, subkey=tuple):
    '''Efficiency vs grouper unknown.  Size maybe smaller.'''
    itls = list(itr)
    if lenmod:=len(itls) % n:
        itls.extend(default for _ in range(n - lenmod))
    itnx = iter(itls).__next__
    return (subkey(itnx() for _ in range(n)) for i in range(0, len(itls), n))

_nf_exit = GeneratorExit("Exit nfold subgenerator")
def _nf_subgenr(itnx, n, default):
    while n:
        try:
            it = itnx()
            False // n
        except (StopIteration, GeneratorExit, ZeroDivisionError): return
        else:
            n -= (n > 0)
            yield it
    return
    
def _g_nf_leng(n, tup, subkey):
    try:
        sub = subkey(tup[:n])
        1 // ((getattr(sub, '__len__', 0) or sub.__length_hint__)() == n)
    except (ZeroDivisionError, AttributeError):
        tuplenseg, tuplenrem = divmod(len(tup), n)
        return lambda o: chain((n,)*tuplenseg, (tuplenrem,)).__next__()
    else: return length_hint
    
def nfold_genr(itr, n=3, subkey=tuple, *, default=_nf_exit):
    "Returns a generator of partitions of len=n from itr.  By default, if len(itr) % n != 0, the final "\
    "partition will have len==remainder; \n"\
    "    list(nfold_genr(range(8), 3)) → [(0, 1, 2), (3, 4, 5), (6, 7)] \n"\
    "Before being yielded, each partition is passed through ‘subkey’, which can be any callable that"\
    " accepts an iterator as input (defaults to tuple); \n"\
    "    list(nfold_genr(range(8), 3, subkey=bytes)) → [b'\x00\x01\x02', b'\x03\x04\x05', b'\x06\x07'] \n"\
    "If len(itr) % n != 0 and ‘default’ is sett, the final partition will be padded with its value. \n"\
    "    list(nfold_genr(range(8), 3, subkey=tuple, default=None)) → [(0, 1, 2), (3, 4, 5), (6, 7, None)]"
    itr = tuple(itr)
    if n % 1:
        itrlen = len(itr)
        n = int(round(itrlen/(itrlen/n)))
        print(n)
    _leng_ = _g_nf_leng(n, itr, subkey)
    itnx = iter(itr).__next__
    while True:
        em = subkey(_nf_subgenr(itnx, n, default))
        if lengem := _leng_(em):
            if ((lengem == n) or (default is _nf_exit)):
                yield em
            else:
                yield subkey(chain(em, repeat(default, int(n-lengem))))
        else: return


def repcycler(it, n=None):
    "Returns cycle(it) if ‘it’ is iterable, otherwise repeat(it, n)."
    try: return cycle(it)
    except TypeError: return repeat(it, int(n)) if n else repeat(it)


def padsome(iterable, pad=...):
    "Returns the sequence elements and then, returns ’pad’ (or next(cycle(pad)), if iterable) indefinitely."
    return chain(iterable, repcycler(pad))


def first_false(iterable, default=True, pred=None):
    "Behaves as the logical inverse of first_true"
    # first_false([a,b,c], x) --> not a and a or not b and b or not c and c or x
    # first_false([a,b], x, f) --> a if not f(a) else b if not f(b) else x
    return next(filterfalse(pred, iterable), default)

def anyfalse(iterable, pred=None):
    return next(filterfalse(map(pred, iterable)), False)
def anytrue(iterable, pred=None):
    return next(filter(map(pred, iterable)), False)
def allfalse(iterable, pred=None):
    return not next(filter(pred, iterable), False)
def alltrue(iterable, pred=None):
    return not next(filterfalse(map(pred, iterable), False))


def xncycles(iterable, xn):
    "Returns the sequence elements approx. xn times, where ‘xn' is a non-negative real.  \n"\
    "    tuple(xncycles('abcdef', 2.4))→ ('a', 'b', 'c', 'd', 'e', 'f', 'a', 'b', 'c', 'd', 'e', 'f', 'a', 'b')"
    tup = tuple(iterable)
    if not xn%1: return flatten(repeat(tup, int(xn)))
    x, n = modf(xn)
    ix = int(len(tup) * x)
    return chain(flatten(repeat(tup, int(n))), tup[:ix])

def xnrepeats(item, xn):
    "Returns ‘item’ approx. xn times, where ‘xn' is a non-negative real number, "\
    "and ‘item’ need not be iterable."
    if not xn%1: return repeat(item, int(xn))
    try:
        tup = tuple(item)
    except TypeError: return repeat(item, int(round(xn)))
    else:
        x, n = modf(xn)
        ix = int(len(tup) * x)
        return chain(repeat(tup, int(n)), (tup[:ix],))

def xnrepcycles(item, xn):
    "Returns ‘item’ approx. xn times, where ‘xn' is a non-negative real, "\
    "and ‘item’ need not be iterable."
    try: return xncycles(item, xn)
    except TypeError: return xnrepeats(item, xn)


_funcmap_call = lambda f, a: f(a)
_funcmap_callstar = lambda f, a: f(*a)
def funcmap(input, *functions):
    "inverted builtins.map.  Calls each function as f(input) or f(*input)."
    try:
        inp = tuple(input)
    except (TypeError, ValueError):
        call = _funcmap_call
    else:
        call = _funcmap_callstar
    return map(call, functions, repeat(input))


def rotate(iterator, n=1):
    "Rotates iterator forward by n steps"
    itnx = iterator.__next__
    return chain(iterable, repeatfunc(itnx, int(n)))

def rotated(sequence, amount=0.5):
    "Returns sequence rotated forward or backwards by amount.  rotated('abcd', 1/2) → 'cdab' "
    try:
        sequence.__getitem__
        ln = len(sequence)
    except (AttributeError, ValueError):
        sequence = tuple(sequence)
        ln = len(sequence)
    s = (amount > 0) - (amount < 0)
    n = int(ln * abs(amount)) % ln
    return sequence[n::s] + sequence[:n:s]


def xljust(iterable, length, pad=None):
    "Like str.ljust, but for any iterable.  If pad is an iterable, its values will be cycled through. "\
    "Uses xnrepcycles, so length can be a float or other real.  Returns an itertools.chain object."
    iterable = tuple(iterable)
    xn = length-len(iterable)
    try:
        pad.__iter__
    except AttributeError: pass
    else:
        pad = tuple(pad)
        xn = xn / len(pad)
    return chain(iterable, xnrepcycles(pad, xn))

def xrjust(iterable, length, pad=None):
    "Like str.rjust, but for any iterable.  If pad is an iterable, its values will be cycled through. "\
    "Uses xnrepcycles, so length can be a float or other real.  Returns an itertools.chain object."
    iterable = tuple(iterable)
    xn = length-len(iterable)
    try:
        pad.__iter__
    except AttributeError: pass
    else:
        pad = tuple(pad)
        xn = xn / len(pad)
    return chain(xnrepcycles(pad, xn), iterable)



extended = ["pairfold", "nfold", "nfold_genr", "repcycler", "padsome", "first_false", 
"anyfalse", "anytrue", "allfalse", "alltrue", "xncycles", "xnrepeats", "xnrepcycles", "funcmap", "rotate", "rotated", "xrjust", "xljust"
]

itertools__all = ['accumulate', 'chain', 'choice', 'combinations', 'combinations_with_replacement', 'compress', 'count', 'cycle', 'deque', 'dropwhile', 'extended', 'filterfalse', 'groupby', 'islice', 'permutations', 'product', 'repeat', 'starmap', 'takewhile', 'tee', 'zip_longest']

__all__ = itertools__all +['take', 'prepend', 'tabulate', 'tail', 'consume', 'nth', 'all_equal', 'quantify', 'padnone', 'ncycles', 'dotproduct', 'flatten', 'repeatfunc', 'pairwise', 'grouper', 'roundrobin', 'partition', 'powerset', 'unique_everseen', 'unique_justseen', 'iter_except', 'first_true', 'random_product', 'random_permutation', 'random_combination', 'random_combination_with_replacement', 'nth_combination'
] + extended


'''
NAME
    itertools - Functional tools for creating and using iterators.

DESCRIPTION
    Infinite iterators:
    count(start=0, step=1) --> start, start+step, start+2*step, ...
    cycle(p) --> p0, p1, ... plast, p0, p1, ...
    repeat(elem [,n]) --> elem, elem, elem, ... endlessly or up to n times

    Iterators terminating on the shortest input sequence:
    accumulate(p[, func]) --> p0, p0+p1, p0+p1+p2
    chain(p, q, ...) --> p0, p1, ... plast, q0, q1, ...
    chain.from_iterable([p, q, ...]) --> p0, p1, ... plast, q0, q1, ...
    compress(data, selectors) --> (d[0] if s[0]), (d[1] if s[1]), ...
    dropwhile(pred, seq) --> seq[n], seq[n+1], starting when pred fails
    groupby(iterable[, keyfunc]) --> sub-iterators grouped by value of keyfunc(v)
    filterfalse(pred, seq) --> elements of seq where pred(elem) is False
    islice(seq, [start,] stop [, step]) --> elements from
           seq[start:stop:step]
    starmap(fun, seq) --> fun(*seq[0]), fun(*seq[1]), ...
    tee(it, n=2) --> (it1, it2 , ... itn) splits one iterator into n
    takewhile(pred, seq) --> seq[0], seq[1], until pred fails
    zip_longest(p, q, ...) --> (p[0], q[0]), (p[1], q[1]), ...

    Combinatoric generators:
    product(p, q, ... [repeat=1]) --> cartesian product
    permutations(p[, r])
    combinations(p, r)
    combinations_with_replacement(p, r)

CLASSES
    builtins.object
        accumulate        chain        combinations>        combinations_with_replacement        compress        count        cycle        dropwhile        filterfalse        groupby        islice        permutations        product        repeat        starmap        takewhile        zip_longest
    class accumulate  |  accumulate(iterable, func=None, *, initial=None)
     |  Return series of accumulated sums (or other binary function results).
     |  Methods defined here:
     |  __getattribute__(self, name, /):    Return getattr(self, name).  |  __iter__  |  __next__  |  __reduce__  |  __setstate__
     
    class chain  |  chain(*iterables) --> chain object
     |  Return a chain object whose .__next__() method returns elements from the
     |  first iterable until it is exhausted, then elements from the next
     |  iterable, until all of the iterables are exhausted.
     |  Methods defined here:  |  __getattribute__  |  __iter__  |  __next__  |  __reduce__  |  __setstate__
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |  __class_getitem__(...) from builtins.type
     |      See PEP 585
     |  from_iterable(iterable, /) from builtins.type
     |      Alternative chain() constructor taking a single iterable argument that evaluates lazily.
     
    class combinations  |  combinations(iterable, r)
     |  Return successive r-length combinations of elements in the iterable.
     |  combinations(range(4), 3) --> (0,1,2), (0,1,3), (0,2,3), (1,2,3)
     |  Methods defined here:  |  __getattribute__  |  __iter__  |  __next__  |  __reduce__  |  __setstate__  |  __sizeof__
     
    class combinations_with_replacemen
nt  |  combinations_with_replacement(iterable, r)
     |  Return successive r-length combinations of elements in the iterable allowing individual elements to have successive repeats.
     |  combinations_with_replacement('ABC', 2) --> AA AB AC BB BC CC"
     |  Methods defined here:  |  __getattribute__  |  __iter__  |  __next__  |  __reduce__  |  __setstate__  |  __sizeof__
     
    class compress  |  compress(data, selectors)
     |  Return data elements corresponding to true selector elements.
     |  Forms a shorter iterator from selected data elements using the selectors to
     |  choose the data elements.
     |  Methods defined here:  |  __getattribute__  |  __iter__  |  __next__  |  __reduce__
     
    class count  |  count(start=0, step=1)
     |  Return a count object whose .__next__() method returns consecutive values.
     |  Equivalent to:
     |      def count(firstval=0, step=1):
     |          x = firstval
     |          while 1:
     |              yield x
     |              x += step
     |  Methods defined here:  |  __getattribute__  |  __iter__  |  __next__  |  __reduce__  |  __repr__
     
    class cycle  |  cycle(iterable, /)
     |  Return elements from the iterable until it is exhausted. Then repeat the sequence indefinitely.
     |  Methods defined here:  |  __getattribute__  |  __iter__  |  __next__  |  __reduce__  |  __setstate__
     
    class dropwhile  |  dropwhile(predicate, iterable, /)
     |  Drop items from the iterable while predicate(item) is true.
     |  Afterwards, return every element until the iterable is exhausted.
     |  Methods defined here:  |  __getattribute__  |  __iter__  |  __next__  |  __reduce__  |  __setstate__
     
    class filterfalse  |  filterfalse(function, iterable, /)
     |  Return those items of iterable for which function(item) is false.
     |  If function is None, return the items that are false.
     |  Methods defined here:  |  __getattribute__  |  __iter__  |  __next__  |  __reduce__
     
    class groupby  |  groupby(iterable, key=None)
     |  make an iterator that returns consecutive keys and groups from the iterable
     |  iterable
     |    Elements to divide into groups according to the key function.
     |  key
     |    A function for computing the group category for each element.
     |    If the key function is not specified or is None, the element itself
     |    is used for grouping.
     |  Methods defined here:  |  __getattribute__  |  __iter__  |  __next__  |  __reduce__  |  __setstate__
     
    class islice  |  islice(iterable, stop) --> islice object
     |  islice(iterable, start, stop[, step]) --> islice object
     |  Return an iterator whose next() method returns selected values from an
     |  iterable.  If start is specified, will skip all preceding elements;
     |  otherwise, start defaults to zero.  Step defaults to one.  If
     |  specified as another value, step determines how many values are
     |  skipped between successive calls.  Works like a slice() on a list
     |  but returns an iterator.
     |  Methods defined here:  |  __getattribute__  |  __iter__  |  __next__  |  __reduce__  |  __setstate__
     
    class permutations  |  permutations(iterable, r=None)
     |  Return successive r-length permutations of elements in the iterable.
     |  permutations(range(3), 2) --> (0,1), (0,2), (1,0), (1,2), (2,0), (2,1)
     |  Methods defined here:  |  __getattribute__  |  __iter__  |  __next__  |  __reduce__  |  __setstate__  |  __sizeof__
     
    class product  |  product(*iterables, repeat=1) --> product object
     |  Cartesian product of input iterables.  Equivalent to nested for-loops.
     |  For example, product(A, B) returns the same as:  ((x,y) for x in A for y in B).
     |  The leftmost iterators are in the outermost for-loop, so the output tuples
     |  cycle in a manner similar to an odometer (with the rightmost element changing
     |  on every iteration).
     |  To compute the product of an iterable with itself, specify the number
     |  of repetitions with the optional repeat keyword argument. For example,
     |  product(A, repeat=4) means the same as product(A, A, A, A).
     |  product('ab', range(3)) --> ('a',0) ('a',1) ('a',2) ('b',0) ('b',1) ('b',2)
     |  product((0,1), (0,1), (0,1)) --> (0,0,0) (0,0,1) (0,1,0) (0,1,1) (1,0,0) ...
     |  Methods defined here:  |  __getattribute__  |  __iter__  |  __next__  |  __reduce__  |  __setstate__  |  __sizeof__
     
    class repeat  |  repeat(object [,times]) -> create an iterator which returns the object
     |  for the specified number of times.  If not specified, returns the object
     |  endlessly.
     |  Methods defined here:  |  __getattribute__  |  __iter__
     |  __length_hint__(...):          Private method returning an estimate of len(list(it)).  |  __next__  |  __reduce__  |  __repr__
     
    class starmap  |  starmap(function, iterable, /): Return an iterator whose values are returned from the function evaluated with an argument tuple taken from the given sequence.
     |  Methods defined here:  |  __getattribute__  |  __iter__  |  __next__  |  __reduce__
     
    class takewhile  |  takewhile(predicate, iterable, /)
     |  Return successive entries from an iterable as long as the predicate evaluates to true for each entry.
     |  Methods defined here:  |  __getattribute__  |  __iter__  |  __next__  |  __reduce__  |  __setstate__
          
    class zip_longest  |  zip_longest(iter1 [,iter2 [...]], [fillvalue=None]) --> zip_longest object
     |  Return a zip_longest object whose .__next__() method returns a tuple where
     |  the i-th element comes from the i-th iterable argument.  The .__next__()
     |  method continues until the longest iterable in the argument sequence
     |  is exhausted and then it raises StopIteration.  When the shorter iterables
     |  are exhausted, the fillvalue is substituted in their place.  The fillvalue
     |  defaults to None or can be specified by a keyword argument.
     |  Methods defined here:  |  __getattribute__  |  __iter__  |  __next__  |  __reduce__  |  __setstate__
     
FUNCTIONS
    tee(iterable, n=2, /)        Returns a tuple of n independent iterators.
'''



