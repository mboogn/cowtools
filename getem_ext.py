
import sys, os
sys.path.append(__file__.rsplit(os.sep, 1)[0])
from getem import *
from getem import __all__ as _allso
from functools import reduce
from itertools import chain, count
from itertools_recipes import padnone, nfold_genr
from collections.abc import Iterable, Mapping, Callable
from types import FunctionType
from dis import COMPILER_FLAG_NAMES
from addedmanually.StringStuff import joinst

__name__ = "getem_ext"
__doc__ = "Additional functions for getem.  Useful for disecting and manipulating FunctionType objects."


__all__ = _allso + [
'validatename', 'isvalidname', 'lamnam', 
'g_lambdanamer', 'functioncopier', 'nagλ', 'ragλ', 
'porkstarred', 'kwgstarred', 'starred', 'isgenerator', 'iscoroutine', 
'is_iterable_coroutine', 'is_async_generator', 'isnested', 'is_not_iteratorlike', 
'co_flags_map', 'get_flag_dict', 
'copy_function'
]


co_flags_map = {v: k for k, v in COMPILER_FLAG_NAMES.items()}


_g_flagcheck = lambda x: x.__and__
#_g_xorflagcheck = lambda x: x.__xor__
_isoptimized = _g_flagcheck(co_flags_map['OPTIMIZED'])
_has__⃰args = _g_flagcheck(co_flags_map["VARARGS"])
_has__⃰_⃰kwargs = _g_flagcheck(co_flags_map['VARKEYWORDS'])
_isnested = _g_flagcheck(co_flags_map['NESTED'])
_isgenerator = _g_flagcheck(co_flags_map['GENERATOR'])
_iscoroutine = _g_flagcheck(co_flags_map['COROUTINE'])
_is_iterable_coroutine = _g_flagcheck(co_flags_map['ITERABLE_COROUTINE'])
_is_async_generator = _g_flagcheck(co_flags_map['ASYNC_GENERATOR'])


_getcocoflags = lambda f: getattr(get_code(f), 'co_flags', None)
def starred(f):
    flgs = _getcocoflags(f)
    return _has__⃰args(flgs), _has__⃰_⃰kwargs(flgs)
porkstarred = lambda f: _has__⃰args(_getcocoflags(f))
kwgstarred = lambda f: _has__⃰_⃰kwargs(_getcocoflags(f))
isgenerator = lambda f: _isgenerator(_getcocoflags(f))
iscoroutine = lambda f: _iscoroutine(_getcocoflags(f))
is_iterable_coroutine = lambda f: _is_iterable_coroutine(_getcocoflags(f))
is_async_generator = lambda f: _is_async_generator(_getcocoflags(f))
isnested = lambda f: _isnested(_getcocoflags(f))
def is_not_iteratorlike(f):
    flgs = _getcocoflags(f)
    return not (_isgenerator(flgs) or _iscoroutine(flgs) or _is_iterable_coroutine(flgs) \
        or _is_async_generator(flgs))


def get_flag_dict(f, only_iftrue=True):
    "Retuens a dictionary of -or-ed flags assigned to f's code"
    flgs = (isinstance(f, int) and f) or _getcocoflags(f)
    flgchk = flgs.__and__
    bins = str(bin(flgs))[2:]
    bins = '0'*(10-len(bins))+bins
    bins = joinst('_')(nfold_genr(bins[::-1], n=4, subkey=''.join))[::-1]
    if only_iftrue:
        return {'_Flags_': (flgs, bins)} | {k: v for k, v in ((kk, flgchk(vv)) for vv,kk in COMPILER_FLAG_NAMES.items()) if v}
    return {'_Flags_': (flgs, bins)} | {k: flgchk(v) for v,k in COMPILER_FLAG_NAMES.items()}


def nagλ(λ):
    if _getcocoflags(λ) & 8: return (lambda ag, *kg: λ(*ag, **kg))
    return (lambda ag, *kg: λ(*ag))
nagλ.__doc__ = 'Takes a poly-input function and makes it single-input: \n'\
f'    (lambda *x: x[::-2])("abcxyz") → {(lambda *x: x[::-2])("abcxyz")} \n'\
f'    nagλ(lambda *x: x[::-2])("abcxyz") → {nagλ(lambda *x: x[::-2])("abcxyz")}'

def ragλ(λ, haskwg=False):
    if _getcocoflags(λ) & 8: return (lambda *ag, **kg: λ(ag,**kg))
    return (lambda *ag, **kg: λ(ag))
ragλ.__doc__ = 'Takes a single-input function and makes it poly-input: \n'\
f'    (lambda x: x[::-2])("abcxyz") → {(lambda x: x[::-2])("abcxyz")} \n'\
f'    ragλ(lambda x: x[::-2])("abcxyz") → {ragλ(lambda x: x[::-2])("abcxyz")}'


isvalidname = lambda ss: (getattr(type(ss), 'isidentifier', 0) or (0).__mul__)(ss)
filter_functions['k-filters'].append(isvalidname)
lamnam = (lambda: None).__name__
def validatename(n, d='λ'): return (isvalidname(n) and n) or d


def g_lambdanamer(default='λ'):
    default = validatename(default)
    λnx = count().__next__
    def lambdanamer(name):
        nonlocal default, λnx
        return name if isvalidname(name) else f'{default}{λnx()}'
    return lambdanamer


def functioncopier(names: Iterable[str]=None, globals_=None, *, argdefs=None, closure=None, **dkwg):
    "Creates a decorative < copyfunc(func) >.  Function <copyfunc> accepts a function, chops it up, clones it with new attributes defined by the original call to functioncopier and returns the clone.  This setup is for decorators, i.e. if you want several different funcs with the same globals or defaults.  ‘names’, if provided, should be a seqence of strings.  A generator function is good if the number of funcs to be created is unknown, otherwise a list [name] or whatever is fine. Just don‘t use a string unless you want single-character names. \n"\
    "    †‘globals_’, if empty or otherwise untruthy, defaults to globals() wherever the copy is created. \n    † unlisted optional kwargs: \n        ‘name’: str→ defines a default prefix for autonamer function. \n        ‘attributes’:dict→ additional attributes to assign.  Read-only attrs, etc. will be ignored."
    attrkys = ('__annotations__', '__kwdefaults__', '__closure__', '__defaults__')
    def locfunc(): return
    loco = locfunc.__code__
    nxtname = padnone(names or []).__next__
    vnamer = g_lambdanamer(dkwg.pop('name', 'func'))
    def copyfunc(func: FunctionType, *, co_replacements: dict=None, name=dkwg.pop('name', None), **kwg):
        nonlocal nxtname, globals_, argdefs, closure, dkwg, loco, attrkys, vnamer
        
        name = vnamer(name or (nxtname() or func.__name__))
        
        code = get_code(func).replace(**{'co_filename': loco.co_filename, \
            'co_name': name}|(co_replacements or {}))
            
        newfunc = FunctionType(code=code, globals=globals_ or globals(), \
            name=name, argdefs=kwg.get('argdefs', argdefs) or getattr(func, '__defaults__', None), \
            closure=kwg.get('closure', closure) or getattr(func, '__closure__', None))
            
        for ky in attrkys:
            try:
                setattr(newfunc, ky, kwg.pop(ky, 0) or getattr(func, ky))
            except AttributeError:
                continue
        addatts = (dkwg|kwg).get('attributes', {})
        for ky in addatts:
            try:
                getattr(newfunc, ky)
            except AttributeError:
                setattr(newfunc, ky, addatts[ky])
            else:
                continue
        return newfunc
    copyfunc.__doc__ = f"names={names}, globals_={None if not globals_ else '*see below*'}, *, argdefs={argdefs}, closure={closure}, **{dkwg} \n globals_={globals_}"
    return copyfunc


def copy_function(func: FunctionType, globals=None, name=None, argdefs=None, kwdefs=None, closure=None, annotations=None, **co_replacements):
    "Non-decorator version of functioncopier.  Returns a copy of 'func' with the given replacements.  "\
    "Parameters set to None will not be altered."
    if globals is None:
        globals = func.__globals__
    if name is None:
        name = func.__name__
    if argdefs is None:
        argdefs = func.__defaults__ or ()
    _co = func.__code__
    if co_replacements:
        _co = _co.replace(**{'co_name': name} | co_replacements)
    newfunc = FunctionType(code=_co, globals=globals, name=name, argdefs=argdefs, closure=closure)
    newfunc.__kwdefaults__ = kwdefs or func.__kwdefaults__ or {}
    newfunc.__annotations__ = annotations or func.__annotations__ or {}
    return newfunc

    