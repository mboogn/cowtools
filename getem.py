
from functools import reduce
from itertools import chain
from collections.abc import Iterable, Mapping, Callable
from types import CodeType


__name__ = "getem"
__doc__ = "        Convenient functions for attribute access and manipulation.  "\
                "Originally for, but not limited to, Function/Code composition.  Many funcs and λ's for data-"\
                "manipulation/visualization/comparison/etc. can be found here.  On the development side, most used internally is ‘getem’ (hence the filename): \n"\
                "functual.getem(obj, *, getter=getattr, dir_=dir, infilters=(notindirobject, ), outfilters=()) →\n"\
                "   →  →  ⟨⟨ Iterator of nak}me-attribute pairs similiar to (--or even directly emulatin--) those "\
                "returned by inspect.getmembers() ⟩⟩ "



#          sequence operations 
__all__ = ['tuprepl', 'zipdictitems', 
#    filter-Functories
'g_notinsq', 'g_insq', 'g_notf', 'g_binary2unary', 'g_vnotinsq', 'g_omitname', 
'notindirobject', 'indir_anyfunc', 'omitglobals', 'anyfunc', 'isnotdunder',
'filter_functions', 
#    attribute getters
'getem', 'get_code', 'get_co_dict', 'code_co_varnames', 
'get_getattr', 'get_getattrs', 'get_getattr_dflt', 'get_getattrs_dflt', 
'get_coco', 'get_code_co_attrs', 
'getemall', 'trycallem', 
'make_code', 'copy_code'
]


def tuprepl(tup, *old, delete=False, by_index=False, **kwg):
    "tuprepl((0, 1, 2, 0), 0, 1, new=3) → (3, 3, 2, 3)"
    if kwg:
        new = kwg['new']
    else:
        *old, new = old
    if by_index:
        old = map(rup.index, old)
    if delete: return tuple(it for it in tup if it not in old)
    return tuple(it if it not in old else new for it in tup)


def zipdictitems(refs, *, keys=None):
    "Visual aid for comparing dictionaries.  "\
    "Takes a sequence of keys (‘keys’) and a sequence of name,dict pairs (‘refs’), "\
    "and returns s tuple of key,value pairs where each value is a list of name,dict[key] pairs from ‘refs’."
    refs = tuple(refs)
    try:
        _, __ = zip(*refs)
    except ValueError:
        refs = [(f'ref_{i}', dict(r)) for i,r in enumerate(refs)]
    else:
        refs = [(n, dict(r)) for n,r in (refs)]
        
    if keys is None:
        try:
            keys = refs[0][1].keys()
        except AttributeError:
            print(refs)
            raise
    return ((name, [(dcnam, dc.get(name, "((N/A))")) for dcnam, dc in refs]) for name in keys)


def anyfunc(x, y=0, /, *, z=None, **kwg): return (x, y, z), ag, kwg
anyfunc.__doc__ = "The only function of this function is to be a function, not to be called.  (See .indir_anyfunc)."


"Filterfunc Factories"
def g_notf(f):
    "return (lambda x: not f(x))"
    return (lambda x: not f(x))
def g_binary2unary(f):
    "return (lambda xy: f(*xy)) -- turns f(x, y) into f(xy); meant for getem’s outfilters."
    return (lambda xy: f(*xy))
def g_notinsq(sq):
    "return (lambda k: (k not in sq))"
    return (g_notf(sq.__contains__))
def g_insq(sq):
    "return (lambda k: (k in sq))"
    return (sq.__contains__)
def g_vnotinsq(sq):
    "return g_binary2unary(lambda k,v: v not in sq)"
    return g_binary2unary(lambda k,v: v not in sq)
def g_omitname(name):
    "return (lambda k: k!=name)"
    return name.__ne__ 

"Filterfuncs"
def isnotdunder(k):
    "returns True if k is not a __dunder__ method."
    return len(k)<6 or not (k[:2]==k[-2:]=='__')
def indir_anyfunc(k):
    "return k not in dir(anyfunc)"
    return k not in dir(anyfunc)
notindirobject = g_notinsq(dir(object))
notindirobject.__name__ = 'notindirobject'
omitglobals = g_omitname('__globals__')


filter_functions = {'setup-/keyword-filters f(k)': [isnotdunder, notindirobject, indir_anyfunc, omitglobals], 
                            'return-/key&val-filters f(kv)': [],
                                'filter-getters': [g_notinsq, g_notf, g_binary2unary, g_vnotinsq, g_omitname]
}
filter_functions['k-filters'] = filter_functions['setup-/keyword-filters f(k)']
filter_functions['kv-filters'] = filter_functions['return-/key&val-filters f(kv)']
filter_functions['g-functions'] = filter_functions['filter-getters']

_dirfreducer = (lambda l0, l1: (lambda x: l0(x) and l1(x)))
_outfreducer = (lambda l0, l1: (lambda x: l0(x) or l1(x)))
def getem(obj, *, getter=getattr, dir_=dir, infilters=(omitglobals, ), outfilters=()):
    "    Get attributes/properties/etc. from ‘obj’.  \n"\
    "Callable ‘dir_’ (default=builtins.dir) is called on the object to obtain keys/names which "\
    "are then passed to ‘getter’ in the form «(key, getter(obj, key)) for key in dir_(obj)».  \n"
    "‘infilters’, is an empty iterable or one containing keys to be passed thru builtins.filter with "\
    "dir_(obj) before constructing the output generator.  ‘outfilters’ works the same, except its "\
    "contents are called on the output generator, and will recieve the yielded (key, value) pairs "\
    "as single input tuples.  \n"\
    "    Essentially: «⟨⟨outfilters⟩⟩(key, getter(obj, key)) for key in filter(⟨⟨infilters⟩⟩, dir_(obj))»"
    "There are compatable filter-funcs and filterfunc-factories in the .filter_function mapping object."
    if getter is not getattr:
        nargs, flags = get_code_co_attrs("co_argcount", "co_flags")(getter)
        if not (nargs > 2 or flags & 0x04):
            _get = getter
            def getter(o, n, d):
                try: return _get(o, n)
                except Exception: return d
    
    source = dir_(obj)
    if infilters:
        if len(infilters) == 1:
            dirf = infilters[0]
        else:
            outf = reduce(_dirfreducer, infilters)
        source = filter(dirf, source)
    
    gotem = ((name, getter(obj, name, "((N/A))")) for name in source)
    if outfilters:
        if len(outfilters) == 1:
            outf = outfilters[0]
        else:
            outf = reduce(_outfreducer, outfilters)
        return filter(outf, gotem)
    
    return gotem

def _trycall(kg):
    k, g = kg
    try:
        g = g()
    except (TypeError, ValueError) as exc:
        if 0:
            g = exc
    return k, g
def trycallem(obj, *, getter=getattr, dir_=dir, infilters=(omitglobals, ), outfilters=()):
    gotem = getem(obj, getter=getter, dir_=dir_, infilters=infilters, outfilters=outfilters)
    return map(_trycall, gotem)


def get_code(x):
    "Returns the code attribute of x.  Methodology copied and altered from the dis module."
    if isinstance(x, CodeType): return x
    # Extract functions from methods.
    x = getattr(x, '__func__', x)
    # Extract compiled code objects from...
    #x = getattr(x, '__code__', 0) or getattr(x, 'gi_code', 0) or getattr(x, 'ag_code', 0) or getattr(x, 'cr_code', x)
    # ...lambda || function,  #...or generator object,  #...or asynchronous generator object  #...or coroutine.
    return getattr(x, '__code__', 0) \
           or getattr(x, 'gi_code', 0) \
           or getattr(x, 'ag_code', 0) \
           or getattr(x, 'cr_code', x)


code_co_varnames = ("co_name", "co_code", "co_lnotab", 
    "co_firstlineno", "co_filename", "co_stacksize", "co_flags", 
    "co_nlocals", "co_argcount", "co_posonlyargcount", "co_kwonlyargcount", 
    "co_names", "co_varnames", "co_consts", "co_cellvars", "co_freevars")
def get_co_dict(fcode, as_itemgen=False):
    "returns a dictionary or a key-value-pair generator of the co_-prefixed code attributes of object ‘fcode’"
    fcode = get_code(fcode)
    if as_itemgen: return ((ky, getattr(fcode, ky)) for ky in code_co_varnames)
    return {ky: getattr(fcode, ky) for ky in code_co_varnames}


def getemall(obj, /, *, getter=getattr, dir_=dir, infilters=(notindirobject, ), outfilters=()):
    "returns concatenated calls to .getem on ‘obj’ and its code attribute."
    return chain(getem(obj, dir_=dir_, getter=getter, infilters=infilters, outfilters=outfilters), 
                      getem(get_code(obj), dir_=dir_, getter=getter, infilters=infilters, outfilters=outfilters))


_gtd = lambda obj, g, d: g if g is not d else d(obj)
def get_getattr(name: str):
    "get_getattr('_someattribute_')(obj) will return obj._someattribute_ if it exists, otherwise it returns obj."
    return lambda obj: getattr(obj, name, obj)
def get_getattrs(*names: [str], include_names=False):
    "get_getattr for multiple attributes."
    if include_names: return lambda obj: ((name, getattr(obj, name, obj)) for name in names)
    return lambda obj: (getattr(obj, name, obj) for name in names)

def get_getattrs_dflt(*names: [str], default=None, include_names=False):
    "Like get_getattrs, but allows default arg. as with builtins.getattr.  If default is callable, it will use obj as its argument."
    if not callable(default):
        if include_names:
            return lambda obj, d=default: ((name, getattr(x, name, d)) for name in names)
        return lambda obj, d=default: (getattr(x, name, d) for name in names)
    if include_names:
        return lambda obj, d=default: ((name, _gtd(obj, getattr(x, name, obj), d)) for name in names)
    return lambda obj, d=default: (_gtd(obj, getattr(x, name, obj), d) for name in names)
def get_getattr_dflt(name: str, default=None):
    "Like get_getattr, but allows default arg. as with builtins.getattr.  If default is callable, it will use obj as its argument."
    if not callable(default): return lambda obj, d=default: getattr(obj, name, d)
    return lambda obj, d=default: _gtd(obj, getattr(x, name, obj), d)


def get_coco(co='co_code'): return lambda f: getattr(get_code(f), co, None)
get_coco.__doc__ = "Works a bit like operator.attrgetter, but accesses attributes of the code*¹ "\
"attribute of a function, as in operator.attrgetter('__code__/gi_code/.../.{co}').  \n *¹(unless applied to a code object or object without a code attribute, in which case it accesses the instance directly)"

def get_code_co_attrs(*names: [str], include_names=False, outkey: Callable=None):
    "Generator version of get_coco.  If no names are provided, defaults to all co_-prefixed attrs, and ‘include_names’ defaults to True."
    if not names:
        names = code_co_varnames
        include_names = True
    if include_names or outkey and isinstance(outkey([('a', 0)]), Mapping):
        if outkey:
            if outkey is dict:
                def getco(f):
                    fco = get_code(f)
                    return {co: getattr(fco, co) for co in names}
            else:
                def getco(f):
                    fco = get_code(f)
                    return outkey(iter((co, getattr(fco, co)) for co in names))
        else:
            def getco(f):
                fco = get_code(f)
                return ((co, getattr(get_code(f), co)) for co in names)
    elif outkey:
        def getco(f):
            fco = get_code(f)
            return outkey(iter(getattr(fco, co) for co in names))
    else:
        def getco(f):
            fco = get_code(f)
            return (getattr(fco, co) for co in names)
    getco.__doc__ = "returns «f.co for co in {names}»"
    return getco


def make_code(co_argcount, co_posonlyargcount, co_kwonlyargcount, co_nlocals, co_stacksize,
         co_flags, co_code, co_consts, co_names, co_varnames, co_filename, co_name,
         co_firstlineno, coln_otab, co_freevars, co_cellvars):
    return CodeType(co_argcount, co_posonlyargcount, co_kwonlyargcount, co_nlocals, co_stacksize,
         co_flags, co_code, co_consts, co_names, co_varnames, co_filename, co_name,
         co_firstlineno, coln_otab, co_freevars, co_cellvars)


def copy_code(code: CodeType, *, co_argcount=..., co_posonlyargcount=..., co_kwonlyargcount=..., co_nlocals=..., co_stacksize=..., co_flags=..., co_code=..., co_consts=..., co_names=..., co_varnames=..., co_filename=..., co_name=..., co_firstlineno=..., coln_otab=..., co_freevars=..., co_cellvars=..., **kwg):
    "Copies a code object with the given replacements."
    return code.replace(**dict(filter(g_binary2unary(lambda k, v: k in code_co_varnames and v is not ...), locals())))

